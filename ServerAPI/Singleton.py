class SingletonNotInitializedException(Exception) :
    def getErrorString() :
        return "Singleton has not been initialized."

class Singleton(object):
    """Basic implementation of a singleton.
        Derive from this to get singleton behaviour.
    """
    def __init__(self, type):
        type._instance = self

    def getInstance(type) :
        if type._instance == None :
            raise SingletonNotInitializedException()

        return type._instance


