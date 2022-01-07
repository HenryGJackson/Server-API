from os import getcwd
import ServerAPI.IpUtils as IpUtils
from ServerAPI.PathUtils import convertPath

credentialsArg : str = "-credPath"
configArg : str = "-configPath"
hostNameArg : str = "-host"
configFileArg : str = "-config"

credentialsPath = getcwd() + convertPath("\\Credentials\\")
configPath = getcwd() + convertPath("\\Config\\")
host = IpUtils.getLocalIp()
configFile = "config.json"
