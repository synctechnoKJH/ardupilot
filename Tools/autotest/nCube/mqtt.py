
import paho.mqtt.client as mqtt
from nCube_Socket import NCubeSocket
import json


class OPTIONS:
    host = "203.253.128.177"
    port = 1883
    protocol = "mqtt"
    keepalive = 10
    cb = "/Mobius"


class MqttClient:
    option = OPTIONS
    client = None # type: mqtt.Client

    socket = None # type: NCubeSocket
    gcs = ""
    name = ""
    sortie = ""
    pubTopic = ""
    subTopic = ""

    def __init__(self, socket, gcs, name, sortie):
        # type: (MqttClient, NCubeSocket, str, str) -> None
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnected
        self.client.on_message = self.on_message
        self.socket = socket
        self.gcs = gcs
        self.name = name
        self.sortie = sortie

        self.pubTopic = self.option.cb + "/" + gcs + "/Drone_Data/" + self.name + "/disarm"# + "#sortie
        self.subTopic = self.option.cb + "/" + self.gcs + "/GCS_Data/" + self.name + "/#"

    def close(self):
        self.client.disconnect()

    def connect(self):
        self.client.connect(host=OPTIONS.host, port=OPTIONS.port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("=====mqtt connected=====")
            self.subscribe()
        else:
            print("Bad Connection Returned Code=", rc)
            exit(1)

    def on_disconnected(self, client, userdasta, flags, rc=0):
        self.client.loop_stop(True)

    def publish(self, data):
        if self.client.is_connected():
            self.client.publish(self.pubTopic, data, 1)            

    def subscribe(self):
        self.client.subscribe(self.subTopic)

    def on_message(self, client, userdata, message):
        print("mqttRecv : ", client, userdata, message)

        if not (self.socket is None):
            try:
                payload = message.payload
                self.socket.sendMsg(payload)
            except BaseException as err:
                print(err)
                self.close()
