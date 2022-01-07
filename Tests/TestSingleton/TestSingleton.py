
from ServerAPI.Singleton import Singleton

class A(Singleton) :
    def __init__(self):
        return super().__init__(A)

class B(Singleton) :
    def __init__(self):
        return super().__init__(B)

class Test() :
    def run(self) :
        a = A()
        b = B()

        if A.getInstance(A) == B.getInstance(B) :
            return (False, "Get instance returns same thing for different classes")
        if A.getInstance(A) is B.getInstance(B) :
            return (False, "Get instance is same thing for different classes")
        if not B.getInstance(B) is Singleton.getInstance(B) :
            return (False, "Calling get instance on Singleton or overriden object should yield same result")
        if not B.getInstance(B) == Singleton.getInstance(B) :
            return (False, "Calling get instance on Singleton or overriden object should yield same result")

        return (True, "Success")

