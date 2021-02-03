# coding=utf-8
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import socket
import threading
import datetime
import numpy as np
from mqtt import MqttClient
from nCube_Socket import NCubeSocket
import onem2m

MOBIUS_URL = "http://203.253.128.177:7579"

sock = None  # type: NCubeSocket
connected = False
mqtt = None  # type: MqttClient

mavStr = ""
mavStrPacket = ""

pre_seq = 0


class nCube:
    id = None
    port = 0
    t_list = []

    def __init__(self, id, port):
        if not id is None:
            self.id = id
        if not port is None and port > 1:
            self.port = port

        if self.id is None or self.port is None or self.port <= 1:
            print("Vehicle ID or SITL Port is not available!!!")
            exit(1)
        else:
            print("nCUBE : ", self.id, ", port : ", self.port);

        gcs, drone, sortie = self.requestDroneInfo()
        self.connect(gcs, drone, sortie)

    def close(self):
        global connected
        connected = False
        mqtt.close()
        sock.close()
        for t in self.t_list:
            t.join(timeout=5000)
        print("=========================nCube is Closed=========================")

    def socketRecvMessage(self):
        global connected, sock, mavStr, mavStrPacket
        print("SITL Message Reciever is Running...")
        while connected:
            try:
                msg = sock.recvMsg()
                if msg[0] == '\xfe' or msg[0] == '\xfd':
                    mavStr += msg.encode('hex')
                    mavStrArr = []

                    str = ''
                    split_idx = 0

                    mavStrArr.append(str)

                    i = 0
                    while i < len(mavStr):
                        str = mavStr[i:i + 2]

                        # 임의로 Mav 버전을 2로 설정
                        if str == 'fe' or str == 'fd':
                            mavStrArr.append('')
                            split_idx += 1
                        mavStrArr[split_idx] += str

                        i += 2
                    del mavStrArr[0]

                    idx = 0
                    while idx < len(mavStrArr):
                        mavPacket = mavStrPacket + mavStrArr[idx]

                        refLen = (int(mavPacket[2:4], 16) + 12) * 2

                        if refLen == len(mavPacket):
                            mqtt.publish(mavPacket.decode('hex'))
                            #  parseMav(mavPacket)
                            mavStrPacket = ''

                        elif refLen < len(mavPacket):
                            mavStrPacket = ''
                        else:
                            mavStrPacket = mavPacket
                        idx += 1

                    if (mavStrPacket != ''):
                        mavStr = mavStrPacket
                        mavStrPacket = ''
                    else:
                        mavStr = ''
            except Exception as err:
                print(err)
        print("SITL Message Receiver closed...")
        return 1

    def openThread(self, callback):
        t = threading.Thread(target=callback)
        print("open subscribe thread")
        t.start()

        self.t_list.append(t)

    def createSortie(self, gcs, drone):
        now = datetime.datetime.now()
        formattedDate = now.strftime("%Y_%m_%d_T_%H_%M")
        uri = MOBIUS_URL + "/Mobius/" + gcs + "/Drone_Data/" + drone
        res = onem2m.createCNT(uri, formattedDate)
        if (res.get('m2m:dbg') and (not (res.get('m2m:dbg') == "resource is already exist"))):
            print("Failed create sortie", res)
            exit(1)

        return formattedDate

    def socketReady(self, gcs, drone, sortie):
        global sock, connected, mqtt

        if not (sock is None):
            exit(1)

        sock = NCubeSocket("127.0.0.1", self.port)

        print("socket created... waiting accept")
        connected = True
        mqtt = MqttClient(sock, gcs, drone, sortie)


    def requestDroneInfo(self):
        response = onem2m.getResource(MOBIUS_URL + "/Mobius/UTM/approval/" + self.id + "/latest")
        vehicleInfo = onem2m.getConOnResponse(response)
        gcs = vehicleInfo['gcs']
        drone = vehicleInfo['drone']

        sortie = self.createSortie(gcs, drone)

        return gcs, drone, sortie

    def connect(self, gcs, drone, sortie):
        self.socketReady(gcs, drone, sortie)

    def run(self):
        self.openThread(self.socketRecvMessage)
        mqtt.connect()
