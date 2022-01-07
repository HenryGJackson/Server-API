import socket

def getLocalIp() :
    return socket.gethostbyname(f"{socket.gethostname()}.local")