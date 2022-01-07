import server.SettingsManager as SettingsManager

configSettings : SettingsManager.SettingsManager = None

def init(configPath : str) :
    global configSettings
    configSettings = SettingsManager.SettingsManager(configPath)