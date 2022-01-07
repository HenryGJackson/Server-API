from ServerAPI import ArgumentParser

class TestableArgumentParser(ArgumentParser.ArgumentParser) :
    def setGivenArguments(self, args) :
        self._args = args

    def getGivenArguments(self) :
        return self._args


