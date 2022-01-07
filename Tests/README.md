# PythonUnitTestFramework
 A unit test framework for testing python modules

# How to use
 To use this framework, place your test modules within the same directory as RunTests.py. 
 
 The expected structure is as follows:
 
 - PythonUnitTestFramework
   - RunTests.py
   - TestModule0
     - TestFile0
     - TestFile1
   - TestModule1
     - TestFile2 

Tests that are included within the above structure will be automatically detected by the framework.

# Example Test

The file should include one class named "Test" and that class must have a function run() which returns a tuple of a bool which determines the success of the test and a string which describes the result of the test.

An example is as follows:

test.py:

    class Test :
        def doSomeCheck() :
            return True
        
        def run() :
            success : bool = True
            msg : str = ""

            if not doSomeCheck() :
                success = False
                msg += "Failed some check"

            return (success, msg)
        
        
    
