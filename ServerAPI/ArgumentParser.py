import sys

########################################################################
# Exceptions
########################################################################

class ArgumentParserExceptionBase(Exception) :
    def __init__(self):
        return super().__init__()

class NotEnoughArgumentsProvidedException(ArgumentParserExceptionBase) :
    def __init__(self, providedArgsCount : int, requiredArgsCount : int) :
        self._providedArgsCount = providedArgsCount
        self._requiredArgsCount = requiredArgsCount
        return super().__init__()

    def getErrorString(self) :
        return f"Not enough arguments provided. Expected at least {str(self._requiredArgsCount)} but got {str(self._providedArgsCount)}."

class ArgumentException(ArgumentParserExceptionBase) :
    def __init__(self, argumentName : str):
        self._argumentName = argumentName
        return super().__init__()

    def getErrorString(self) :
        return f"ArgumentException with argument {self._argumentName}";

class RequiredArgumentNotSetException(ArgumentException) :
    def __init__(self, argumentName : str):
        return super().__init__(argumentName)

    def getErrorString(self) :
        return f"Required Argument \"{self._argumentName}\" is not set"

class ArgumentValueNotSetException(ArgumentException) :
    def __init__(self, argumentName : str):
        self.argumentName = argumentName
        return super().__init__(argumentName)

    def getErrorString(self) :
        return f"Value for argument \"{self._argumentName}\" is not set"

########################################################################
# ArgumentParser
########################################################################

class ArgumentParser(object):
    """Parses the arguments given by the script according to the configuration setup in init()"""
    def __init__(self, requiredArguments : list, optionalArguments : list):
        self._required : list = requiredArguments
        self._optional : list = optionalArguments
        self._defaults : dict = {}
        self._argValues : dict = {}

    def setDefaultValue(self, argName : str, value) :
        self._defaults[argName] = value

    def getGivenArguments(self) :
        return sys.argv[1:]

    def getValue(self, argName : str) :
        if argName in self._argValues :
            return self._argValues[argName]

        if argName in self._defaults :
            return self._defaults[argName]

        return None

    def argsHelp(self) -> str :
        return f"The required arguments are: \n{str(self._required)}\nThe optional arguments are:\n{str(self._optional)}"

    def getArgs(self, argList : list, allRequired : bool = False) :
        # Don't consider the file name as an argument
        scriptArguments = self.getGivenArguments()

        for arg in argList :
            argFromGivenArgs = next((x for x in scriptArguments if x == arg), None)

            if argFromGivenArgs is None :
                if allRequired :
                    raise RequiredArgumentNotSetException(arg)

                continue

            valueIndex = scriptArguments.index(argFromGivenArgs) + 1
            if valueIndex > len(scriptArguments) - 1 :
                raise ArgumentValueNotSetException(arg)

            value = scriptArguments[valueIndex]

            if value in self._required or value in self._optional :
                raise ArgumentValueNotSetException(arg)

            self._argValues[arg] = value

    def parse(self) : 
        # If there are no arguments given, check whether we have any required arguments
        # if so then raise an exception otherwise simply return an empty list
        args = self.getGivenArguments()
        if len(args) < len(self._required) * 2 :
            raise NotEnoughArgumentsProvidedException(len(args), len(self._required))

        self._argValues : dict = {}
        self.getArgs(self._required, True)
        self.getArgs(self._optional, False)



