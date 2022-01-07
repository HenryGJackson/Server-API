from os import getcwd
import server.IpUtils as IpUtils
from server.PathUtils import convertPath

credentialsArg : str = "-credPath"
configArg : str = "-configPath"
hostNameArg : str = "-host"
configFileArg : str = "-config"

credentialsPath = getcwd() + convertPath("\\Credentials\\")
configPath = getcwd() + convertPath("\\Config\\")
host = IpUtils.getLocalIp()
configFile = "config.json"
