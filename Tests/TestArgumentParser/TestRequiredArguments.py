from Tests.TestArgumentParser.ArgumentParserUtils import TestableArgumentParser
from ServerAPI import ArgumentParser

class Test() :
    def run(self) :
        required = { "required0" : 5.6, "required1" : "a value" }

        parser = TestableArgumentParser(required.keys(), [])

        args = []
        # Set default values for optional args
        for arg, value in required.items() : 
            args.append(arg)
            args.append(value)

        parser.setGivenArguments(args)
        parser.parse()

        msg = ""
        result = True

        for arg, value in required.items() : 
            parsedValue = parser.getValue(arg)

            if value != parsedValue :
                result = False
                msg += f"Argument \"{arg}\" Expected value: {str(value)} Got value: {str(parsedValue)}\n"

        # Try giving too few arguments considering how many required args there are.
        # Expect that we get a NotEnoughArgumentsProvidedException raised
        args.remove("required0")
        args.remove(required["required0"])
        parser.setGivenArguments(args)

        try :
            parser.parse()

            result = False
            msg += f"Expected exception of type: NotEnoughArgumentsProvidedException but none was raised\n"
        except ArgumentParser.NotEnoughArgumentsProvidedException :
            pass
        except Exception as e :
            result = False
            msg += f"Expected exception of type: NotEnoughArgumentsProvidedException but got: {type(e).__name__}\n"

        # Try giving enough arguments but not providing a value for one of the required arguments
        # Expect that we get a RequiredArgumentNotSetException
        args.append("someOtherArg")
        args.append("someOtherArgValue")
        parser.setGivenArguments(args)

        try :
            parser.parse()

            result = False
            msg += f"Expected exception of type: RequiredArgumentNotSetException but none was raised\n"
        except ArgumentParser.RequiredArgumentNotSetException :
            pass
        except Exception as e :
            result = False
            msg += f"Expected exception of type: RequiredArgumentNotSetException but got: {type(e).__name__}\n"

        # Try giving no value for one of the arguments and expect we get a ArgumentValueNotSetException
        args.append("required0")
        parser.setGivenArguments(args)

        try :
            parser.parse()

            result = False
            msg += f"Expected exception of type: ArgumentValueNotSetException but none was raised\n"
        except ArgumentParser.ArgumentValueNotSetException :
            pass
        except Exception as e :
            result = False
            msg += f"Expected exception of type: ArgumentValueNotSetException but got: {type(e).__name__}\n"

        # Try having the missing value for an argument followed by another argument
        args.remove(required["required1"])
        args.remove("someOtherArg")
        args.remove("someOtherArgValue")
        args.append("required0Value")

        # Add a random arg at the end so we bypass the length of arguments check
        args.append("someOtherArg")

        parser.setGivenArguments(args)

        try :
            parser.parse()

            result = False
            msg += f"Expected exception of type: ArgumentValueNotSetException but none was raised\n"
        except ArgumentParser.ArgumentValueNotSetException :
            pass
        except Exception as e :
            result = False
            msg += f"Expected exception of type: ArgumentValueNotSetException but got: {type(e).__name__}\n"

        if result :
            msg = "Success"

        return (result, msg)
