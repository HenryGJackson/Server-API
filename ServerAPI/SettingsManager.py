import json
import os

##################################################################
# Exceptions
##################################################################

class SettingsException(Exception) :
    def __init__(self, setting : str) :
        self._setting = setting
        return super().__init__()

    def getErrorString(self) -> str :
        return f"Setting error with setting: {self._setting}"

class SettingNotSetException(SettingsException) : 
    def getErrorString(self) -> str :
        return f"Setting \"{self._setting}\" has not been set"

##################################################################
# Manager
##################################################################

class SettingsManager(object) :
    """ Manages settings that are stored on disc """
    def __init__(self, settingsFilePath : str) :
        self._settingsFile : str = settingsFilePath
        self._settings : dict = {}

        self._createFileIfNotExisting()
        self._loadSettings()

        return super().__init__()

    def _createFileIfNotExisting(self) :
        """ If the file does not exist then write empty settings into the given file """
        if os.path.exists(self._settingsFile) :
            return 

        self._writeSettings()

    def _loadSettings(self) :
        """ Loads the settings into a dictionary from the file """
        with open(self._settingsFile, 'r') as file :
            self._settings = json.loads(file.read())

    def _writeSettings(self) :
        """ Writes the settings from the dictionary to the file """
        content : str = json.dumps(self._settings)

        with open(self._settingsFile, 'w') as file :
            file.write(content)

    def set(self, settingName : str, value) :
        """ Sets the value of a setting """
        self._settings[settingName] = value

        # Write after changing a setting so we always have the updated values on disc
        self._writeSettings()

    def setFromDict(self, settings : dict) :
        """ Sets the value of multiple settings based on the given dictionary """
        self._settings.update(settings)

        # Write after changing a setting so we always have the updated values on disc
        self._writeSettings()

    def isSettingSet(self, settingName) -> bool :
        """ Returns true if a value has been set for the given setting """
        return settingName in self._settings 

    def get(self, settingName : str) :
        """ Gets the value of the given setting or raises a SettingNotSetException if it has not been sepcified """
        if not self.isSettingSet(settingName) :
            raise SettingNotSetException(settingName)

        return self._settings[settingName]




