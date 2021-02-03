import socket

BUFFER_SIZE = 1024


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

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def recvMsg(self):
        try:
            data, msgInfo = self.sock.recvfrom(BUFFER_SIZE)
            if((self.msgInfo is None) or (self.msgInfo != msgInfo)):
                self.msgInfo = msgInfo
            return data
        except BaseException as err:
            print(err)
            return ""

    def sendMsg(self, msg):
        if(not (self.msgInfo is None)):
            self.sock.sendto(msg, self.msgInfo)
