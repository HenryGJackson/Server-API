import json
import server.LogInManager as lm
from server.PostOnlyServer import ServerCommand, ServerCommandHandler, ServerException
import server.TokenManagement as tm

class LogInCommand(ServerCommand) :
    class LoginFormatInvalidException(ServerException) :
        def getErrorString(self):
            return "The content for the log in request should be the username and passwork in json format"

    class LoginFailedException(ServerException) :
        def getErrorString(self):
            return "The username and/or password were not correct"

    def __init__(self, loginManager : lm.LogInManager, tokenManager : tm.OwnedTokenManager):
        self._manager : lm.LogInManager = loginManager
        self._tokenManager : tm.OwnedTokenManager = tokenManager
        return super().__init__("LogIn")

    def execute(self, data) :
        loginData = json.loads(data)
        if not ("username" in loginData) or not ("password" in loginData) :
            raise LogInCommand.LoginFormatInvalidException()

        username : str = loginData["username"]
        if not self._manager.loginSuccessful(username, loginData["password"]) : 
            raise LogInCommand.LoginFailedException()

        return self._tokenManager.generateToken(username)

class ValidateTokenCommand(ServerCommand) :
    def __init__(self, tokenManager : tm.OwnedTokenManager) :
        self._tokenManager : tm.OwnedTokenManager = tokenManager
        return super().__init__("ValidateToken")

    def execute(self, data):
        return self._tokenManager.isValidToken(str(data))


def create(commandHandler : ServerCommandHandler, localTokens : tm.OwnedTokenManager, passwordManager : lm.LogInManager) :
    authorizeTokenCommand = ValidateTokenCommand(localTokens)
    commandHandler.addPostCommand(authorizeTokenCommand)

    loginCommand = LogInCommand(passwordManager, localTokens)
    commandHandler.addPostCommand(loginCommand)