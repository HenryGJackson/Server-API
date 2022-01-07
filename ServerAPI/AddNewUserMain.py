import getpass
import hashlib
import irrigation.IrrigationArguments as IrrigationArguments
import json
import os
from ServerAPI.ArgumentParser import ArgumentParser, ArgumentParserExceptionBase
import ServerAPI.DefualtArguments as default
import sys

# prompt the user to enter their password and hash that so that we do not store readable or insecure passwords
def getPassword() :
    password = getpass.getpass('Password:')

    hash = hashlib.sha256();
    hash.update(password.encode('utf-8'))
    return hash.hexdigest()

def getUsername() :
    return input("Username: ")

def createFileIfNotExists(credsFolder : str, filePath : str) :
    if not os.path.exists(credsFolder) :
        os.mkdir(credsFolder)

    contents : dict = {}

    if not os.path.exists(filePath) :
        with open(filePath, "w+") as file :
            toWrite = json.dumps(contents)
            file.write(toWrite)


# Add a new user to the credentials file
def addUser(parsedArgs : ArgumentParser) :
    username = getUsername()

    filePath = IrrigationArguments.getLoginInfoFilePath(parsedArgs)
    credsFolder = IrrigationArguments.getCredentialsFolder(parsedArgs)
    
    parsedArgs.getValue(credentialsArg)
    contents : dict = {}

    createFileIfNotExists(credsFolder, filePath)

    with open(filePath, "r") as file :
        asString = file.read()
        contents = json.loads(asString)

    if username in contents :
        print(f"Updating password for user: {username}.")
    else :
        print(f"Creating user: {username}.")

    contents[username] = getPassword()

    with open(filePath, "w") as file :
        asString = json.dumps(contents)
        file.write(asString)

    print("Done.")


def main() :
    try :
        parser = IrrigationArguments.parseArgs()
        addUser(parser)

    except ArgumentParserExceptionBase as e :
        print(f"Exception: {e.getErrorString()}")
        print(parser.argsHelp())

if __name__ == "__main__" :
        main()
    

