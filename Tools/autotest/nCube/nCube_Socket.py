import socket

BUFFER_SIZE = 1024

class NCubeSocket:
    sock = None
    msgInfo = None
    host = ""
    port = 0

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)    # SHUT_RDWP shutdown Read and Write both Buffers
        except socket.error as err:
            print(err)
        # self.sock.close() # shutdown will close socket

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