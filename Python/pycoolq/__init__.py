# coding: UTF-8
import threading
import socket
from urllib import quote, unquote
from circuits import handler
from circuits.net.sockets import TCPServer
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

sock = socket.socket(type=socket.SOCK_DGRAM)


class receivedMessage():
    def __init__(self, sourceType, fromGroupID, fromID, content):
        self.sourceType = sourceType
        self.fromGroupID = fromGroupID
        self.fromID = fromID
        self.content = content


class sendMessage():
    def __init__(self, destinationType, destinationID, content):
        self.destinationType = destinationType
        self.destinationID = destinationID
        self.content = content


class messagePreprocessor(TCPServer):
    @handler("read")
    def on_read(self, sock, data):
        qqMessageHandlerExecutor(data)
        return 0


messageHandlers = []


class coolqBot():
    def __init__(self, py2cqPort, cq2pyPort):
        global sendPort
        global receivePort
        sendPort = py2cqPort
        receivePort = cq2pyPort

        sock.connect(("127.0.0.1", sendPort))
        self.listener = messagePreprocessor(("0.0.0.0", receivePort))

    def send(self, sendMessage):
        sock.send(sendMessage.destinationType + " " + str(sendMessage.destinationID) + " " + quote(sendMessage.content))
        return 0

    def listenerStarter(self):
        self.listener.start()

    def startListen(self):
        poll = threading.Thread(target=self.listenerStarter)
        poll.setDaemon(True)
        poll.run()

    def qqMessageHandler(self):
        def decorator(handler):
            messageHandlers.append(handler)
            return handler

        return decorator


def qqMessageHandlerExecutor(data):
    string = str(data)
    dataParts = string.split(" ")
    if dataParts[0] == "group" or "discuss":
        msg = unquote(dataParts[3]).decode("gbk")
        sender = int(dataParts[2])
        sendGroup = int(dataParts[1])
        message = receivedMessage(sourceType=dataParts[0], fromGroupID=sendGroup, fromID=sender, content=msg)
    elif dataParts[0] == 'personal':
        msg = unquote(dataParts[2]).decode("gbk")
        sender = int(dataParts[1])
        message = receivedMessage(sourceType=dataParts[0], fromGroupID=0, fromID=sender, content=msg)
    for i in messageHandlers:
        i(message)
