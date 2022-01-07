import Tests.TestArgumentParser.ArgumentParserUtils as TestableArgumentParser

class Test() :
    def run(self) :
        optional = { "optional0" : 5.6, "optional1" : "a value" }

        parser = TestableArgumentParser.TestableArgumentParser([], optional.keys())

        # Set default values for optional args
        for arg, value in optional.items() : 
            parser.setDefaultValue(arg, value)

        args = []
        parser.setGivenArguments(args)
        parser.parse()

        msg = ""
        result = True

        for arg, value in optional.items() : 
            parsedValue = parser.getValue(arg)
            if value != parsedValue :
                result = False
                msg += f"Argument \"{arg}\" Expected value: {str(value)} Got value: {str(parsedValue)}\n"

        return (result, msg)