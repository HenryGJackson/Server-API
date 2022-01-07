from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus
import logging
from ServerAPI.Singleton import Singleton
import threading

########################################################################
# Ecxeptions
########################################################################

class ServerException(Exception) :
    def getErrorString(self) :
        raise NotImplementedError()

class ServerCommandException(ServerException) :
    def __init__(self, commandName : str):
        self._commandName = commandName
        return super().__init__()

class CommandNotImplementedException(ServerCommandException) :
    def getErrorString(self) :
        return f"Server command \"{self._commandName}\" uses base type. Override this to get custom behaviours"

class ServerCommandHandlerNotInitializedException(ServerException) :
    def getErrorString(self) :
        return f"Server command handler has not been initialized"

class ServerUnrecognizedCommandException(ServerCommandException) :
    def getErrorString(self) :
        return f"Server command \"{self._commandName}\" is not recognized"

class ServerInvalidCommandFunctionException(ServerCommandException) :
    def getErrorString(self) :
        return f"Server command \"{self._commandName}\" is recognized but does not have a valid command bound"

class ServerNoCommandSpecifiedException(ServerException) :
    def getErrorString(self):
        return "No command was sent in the POST request"

class ServerContentLengthNotSetException(ServerException) :
    def getErrorString(self):
        return "Content length was not specified in the request"

class ServerTokenInvalidException(ServerException) :
    def getErrorString(self):
        return "The given token was not valid. "

########################################################################
# Commands
########################################################################

class ServerCommand :
    def __init__(self, commandName : str) :
        self.name = commandName

    def execute(self, data : str) :
        raise CommandNotImplementedException(self.name)

class ServerCommandHandler(Singleton) :
    _instance = None

    def __init__(self) :
        self._commands : dict = {}
        return super().__init__(ServerCommandHandler)

    def getInstance() :
        return Singleton.getInstance(ServerCommandHandler)

    def addPostCommand(self, command : ServerCommand) :
        self._commands[command.name] = command

    def executeCommand(self, commandName : str, data : str) :
        if not commandName in self._commands :
            raise ServerUnrecognizedCommandException(commandName)

        command = self._commands.get(commandName, None) 
        if command is None :
            raise ServerInvalidCommandFunctionException(commandName)

        return command.execute(data)

########################################################################
# Server
########################################################################

class PostOnlyServer(BaseHTTPRequestHandler):
    """ HTTP POST handler, 
      = Accesses the static instance of ServerCommandHandler to execute commands.

      = Only serves POST requests so acts as an API to be called over the network.

      = Required Commands:
      - LogIn: The body of the request will be passed to the command directly.
        It's up to the command to parse that data and verify that the token should be provided
        Should return the valid token
      - AuthorizeToken: Given a token from the client, this verifies that the given token
        is valid and if so permits the call to the API.
        If the token is not valid, a ServerTokenInvalidException should be raised.

      = If the required commands are not implemented, a ServerUnrecognizedCommandException will be reaised.
    """
    def __init__(self, request, client_address, server):
        self._commands : dict = {}
        return super().__init__(request, client_address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Automated Irrigation</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This server should not be accessed in the web</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    # Send an error response with the given message
    def sendPostCommandNotRecognized(self, msg : str) :
       self.send_error(HTTPStatus.NOT_IMPLEMENTED, msg)

    # Get the name of the command that has been requested to execute
    def getCommand(self) -> str :
        command = self.headers.get("command")
        if command is None :
            raise ServerNoCommandSpecifiedException()

        return command

    # Get the token header and verify that it is valid
    def getAndAuthorizeToken(self) -> str :
        token = self.headers.get("token")
        if token is None :
            raise ServerTokenInvalidException();

        if not ServerCommandHandler.getInstance().executeCommand("ValidateToken", token) :
            raise ServerTokenInvalidException()


    # Get the length of the content in the request as an integer
    def getContentLength(self) -> int :
        contentLengthAsString = self.headers.get('Content-Length')
        if contentLengthAsString is None :
            raise ServerContentLengthNotSetException()

        return int(contentLengthAsString)

    # Get the content in the request
    def getContent(self) -> str :
        return self.rfile.read(self.getContentLength()).decode("utf-8")

    # returns true if the request is a log in request
    def isLogInRequest(self, command : str) -> bool :
        return command == "LogIn"

    # Handles a log in request, this is a special request that will not come with a valid token
    # a valid token will be returned to the user for them to use in future API calls
    def serveLogInRequest(self, command) :
        token = ServerCommandHandler.getInstance().executeCommand(command, self.getContent())

        # Return the generated token to the client so they can use this in subsequent API calls
        self.send_response(HTTPStatus.ACCEPTED)
        self.send_header("Token", token)
        self.send_header("result", "OK")
        self.end_headers()

    # Handles all requests that are not log in requests.
    # First validates that a valid token has been provided
    # If a valid token was provided then the command will be executed and a success response returned
    def serveNonLogInRequest(self, command) :
        # If the client has explicitly asked to validate the token then we do want to send a successful result
        # So we don't validate it here since that would result in a failure response
        if command != "ValidateToken" :
            self.getAndAuthorizeToken()

        result = ServerCommandHandler.getInstance().executeCommand(command, self.getContent())
        self.send_response(HTTPStatus.ACCEPTED)
        self.send_header("result", "OK")
        self.end_headers()
        self.wfile.write(bytes(str(result), "utf-8"))
        
    # Serves all post requests
    def do_POST(self) :
        try :
            command = self.getCommand()
            if self.isLogInRequest(command) :
                self.serveLogInRequest(command)
            else :
                self.serveNonLogInRequest(command)

        except ServerException as e :
            self.sendPostCommandNotRecognized(e.getErrorString())
        
########################################################################
# Utils
########################################################################

def runServer(port : int, hostName : str) :
    """ Runs the server until a keyboard interrupt. If an exception is thrown within the server, 
        it is restarted so that it doesn't go down. However the exception will be 
    """
    webServer = HTTPServer((hostName, int(port)), PostOnlyServer)
    print("Server started http://%s:%s" % (hostName, port))

    while True :
        try:
            webServer.serve_forever()

        except KeyboardInterrupt:
            webServer.server_close()
            logging.debug("Server stopped.")
            break

        except Exception as e :
            webServer.server_close()
            logging.debug("Server stopped. Starting again")
            logging.debug(e.getErrorString())
            pass

    webServer.shutdown()


class AsyncServerThread(Singleton) :
    def __init__(self, thread : threading.Thread, webServer : HTTPServer) :
        self.thread = thread
        self.server = webServer
        return super().__init__()

def runServerAsync(port : int, hostName : str) :
    webServer = HTTPServer((hostName, port), PostOnlyServer)
    logging.debug("Server started http://%s:%s" % (hostName, port))

    thread = threading.Thread(target = webServer.serve_forever)
    thread.start()

    return AsyncServerThread(thread, webServer)

def killServerAsync() :
    AsyncServerThread.getInstance().server.shutdown()


