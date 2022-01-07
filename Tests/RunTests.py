import os
import logging
import colorama

def extractTestModules(directory : str, depth : int = 0) :
    directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and "Test" in d]

    modules = [d for d in directories if "__init__.py" in os.listdir(os.path.join(directory, d))]
    nonModules = [os.path.join(directory, d) for d in directories if not d in modules]

    # Look through directorie for other tests
    for dir in nonModules :
        files.extend(extractTestModules(dir, depth + 1))

    if depth > 0 :
        for module in modules :
            relativePath = str.join(d + "." for d in directory.split(os.sep)[-depth:])
            module = relativePath + module

    return modules

def main() :
    testsPath = os.path.dirname(os.path.realpath(__file__))
    modules = extractTestModules(testsPath)
    logger = logging.getLogger(__name__)
    colorama.init(convert=True)

    for moduleName in modules :
        
        modulePath = testsPath + os.sep + moduleName.replace(".", os.sep)
        testFiles = [f for f in os.listdir(modulePath) if not "__init__" in f and os.path.isfile(os.path.join(modulePath, f))]
        testModuleNames = [f.replace(".py", "") for f in testFiles]

        module = __import__(moduleName, fromlist=testModuleNames)

        for testModuleName in testModuleNames:
            testInnerModule = getattr(module, testModuleName)

            if not hasattr(testInnerModule, "Test") : 
                continue

            testable = testInnerModule.Test()
            result, msg = testable.run()
            if not result :
                print(colorama.Fore.RED + f"*** Failure: Test \"{testInnerModule}\" Failed with reuslt: {msg}")
            else :
                print(colorama.Fore.GREEN + f"Test \"{testInnerModule}\" Passed with result: {msg}")

            print(colorama.Style.RESET_ALL)

if __name__ == "__main__" :
    main()