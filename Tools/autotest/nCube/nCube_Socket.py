import socket

BUFFER_SIZE = 128


class NCubeSocket:
    sock = None
    msgInfo = None
    host = ""
    port = 0

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))

    def __del__(self):
        self.sock.close()

    def recvMsg(self):

        data, msgInfo = self.sock.recvfrom(BUFFER_SIZE)
        if((self.msgInfo is None) or (self.msgInfo != msgInfo)):
            self.msgInfo = msgInfo
        return data

    def sendMsg(self, msg):
        if(not (self.msgInfo is None)):
            self.sock.sendto(msg, self.msgInfo)
