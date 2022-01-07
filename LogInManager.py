import json

class LogInManager(object):
    """Loads all valid usernames and passwords from the given file
       The file should be in json format.
       The values like username and password should be encrypted and then stored in the file
       So we can treat it as a JSON without decryption and only encrypt the data on the client
    """
    def __init__(self, filename):
        with open(filename, "rt") as f :
            contents = f.read()

        self._credentials : dict = json.loads(contents)

        return super().__init__()

    def loginSuccessful(self, username, password) -> bool :
        return (self._credentials.get(username) == password) if (username in self._credentials) else False

