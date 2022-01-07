# Server-API
A framework to easily create a remote hosted API.

Commands can be added to the API which will be called automatically when a post request is made to the server with a header which specifies the command to run and a security token which grants access to the API. 
The body of the request should include the command parameters. 
The server will then return a response with the body being the result of the command.
Some commands are required for security purposes, one to login using a username and password which issues a token to the user and one to validate the token when a command request is received.
    
# Setting up the server
## Creating the server
Creating the server and making it run is quite simple, simply import PostOnlyServer and execute the runServer function.

```python
from ServerAPI import PostOnlyServer as pos

host = "localhost"
port = 8080
pos.runServer(port, host)
```

The server can also be run async so that the main thread is reserved to do other work using

```python
from ServerAPI import PostOnlyServer as pos

host = "localhost"
port = 8080
pos.runServerAsync(port, host)
```

## Adding Commands
Commands can be created by creating a class that inherits from PostOnlyServer.ServerCommand. 
The command should then specify its command name when it calls the constructor for ServerCommand. 
The command should also implement an execute function which is what gets called when a request is received. 
The execute function should then return the result of the command.

### Command Example
```python
from ServerAPI.PostOnlyServer import ServerCommand

class ExampleCommand(ServerCommand) :
  def __init__() :
    super().__init__("ExampleCommand")

  def doSomeWork(self, data) :
    pass

  def execute(self, data) :
    return doSomeWork(data)
```
      
### Registering the command with the server
Once the command has been implemented, it must be registered with the server so that it knows what to run when the request is received.
To do this, first we need to create a ServerCommandHandler, then we register the command with the handler.

```python
from ServerAPI.PostOnlyServer import ServerCommandHandler

commandHandler = pos.ServerCommandHandler()

exampleCommand = ExampleCommand()
commandHandler.addPostCommand(exampleCommand)
```

 # Security
All commands must be validated with a token which are issued by the server.
Before a token can be issued however, the user must log in.

Some commands are included to aid with this process, these are "LogIn" and "ValidateToken".

In order to register these commands we need to setup some additional objects.

## LoginManager
The LoginManager must be created and given the path to a credentials file which contains the usernames and hashed passwords for all registered users.
AddNewUserMain.py should be run on the server to register these users.
All passwords are hashed using the sha-256 hashing algorithm. The reason to store hashed passwords is to make it more difficult for brute force attacks to find a valid password.
Hashing the passwords also prevents us from storing in plain text the password of the user which (shouldn't but) may be used elsewhere.
Care should still be taken to ensure that the login credentials file is not easily accessible to attackers.
 
### Creating the LoginManager

```python
from ServerAPI import LoginManager

loginDetailsFilePath = "<insert path here>"
loginManager = LoginManager(loginDetailsFilePath)
```

## TokenManager
The TokenManager must be created and given the path to a credentials file which contains the valid token issued by the LogIn command for each user.
After successfully posting a LogIn request, the response will contain the token in the body.
All requests other than the login request must include the valid token in the header so the TokenManager must be created to validate those tokens.

### Creating the TokenManager

```python
from ServerAPI.TokenManagement import OwnedTokenManager

tokenFilePath = "<insert path here>"
tokenManager = OwnedTokenManager(tokenFilePath)
```

## Setting up the Security Commands
Once the TokenManager and the LoginManager have been created, we need to register these with the security commands and the command manager so that the server can validate logins and commands.

The commands are already implemented along with a helper function to create the commands. This can be done as follows:
    
```python
from ServerAPI import SecurityCommands

# Access the command handler (which should have alredy been created in a previous step)
commandHandler = pos.ServerCommandHandler.getInstance()

SecurityCommands.create(commandHandler, tokenManager, loginManager)
```

# Example Post Requests to Execute Commands
Once the commands have been implementated and added to the server along with the security commands then when the server receives a post request with the command specified in its headers, the command will be executed.
The body of the request is passed straight to the command's execute function.

## Plain Text Example

    POST HTTP/1.1
    command: ExampleCommand
    token: <user-token>
    Content-Type: text/plain
    Content-Length: <content-length>

    field1=value1&field2=value2
    
## Json Example

    POST HTTP/1.1
    command: ExampleCommand
    token: <user-token>
    Content-Type: text/json
    Content-Length: <content-length>
    
    {"field1": value1, "field2": value2}
    
## Login Command Example

    POST HTTP/1.1
    command: LogIn
    Content-Type: text/json
    Content-Length: <content-length>
    
    {"username": "<username>", "password": "<password hashed using sha-256>"}

