from Tests.TestArgumentParser.ArgumentParserUtils import TestableArgumentParser

class Test() :
    def run(self) :
        optional = { "optional0" : 5.6, "optional1" : "a value" }

        parser = TestableArgumentParser([], optional.keys())

        # Set default values for optional args
        for arg, value in optional.items() : 
            parser.setDefaultValue(arg, value)

        overridenArgs = { "optional1": "a different value" }
        args = ["optional1", overridenArgs["optional1"]]

        parser.setGivenArguments(args)
        parser.parse()

        msg = ""
        result = True

        for arg, value in optional.items() : 
            parsedValue = parser.getValue(arg)
            expectedValue = optional[arg] if arg not in overridenArgs else overridenArgs[arg]

            if expectedValue != parsedValue :
                result = False
                msg += f"Argument \"{arg}\" Expected value: {str(value)} Got value: {str(parsedValue)}\n"

        return (result, msg)