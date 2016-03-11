# coding: UTF-8
import re
import sys
import threading
import socket
import collections
from urllib import quote, unquote
from circuits import handler
from circuits.net.sockets import TCPServer

reload(sys)
sys.setdefaultencoding('utf-8')

receivedMessage = collections.namedtuple('receivedMessage',
                                         ('sourceType', 'fromGroupID', 'fromID', 'content'))

sendMessage = collections.namedtuple('sendMessage',
                                     ('destinationType', 'destinationID', 'content'))

re_cq_special = re.compile(r'\[CQ:(face|emoji|at|shake|music|anonymous|image|record)(,\w+=[^]]+)?\]')

class messagePreprocessor(TCPServer):
    @handler("read")
    def on_read(self, sock, data):
        self.qqMessageHandlerExecutor(data)
        return 0

    def setMessageHandlers(self, handlers):
        self.messageHandlers = handlers

    def qqMessageHandlerExecutor(self, data):
        string = str(data)
        dataParts = string.split(" ")
        if dataParts[0] in ("group", "discuss"):
            msg = unquote(dataParts[3]).decode("gbk")
            sender = int(dataParts[2])
            sendGroup = int(dataParts[1])
            message = receivedMessage(sourceType=dataParts[0], fromGroupID=sendGroup, fromID=sender, content=msg)
        elif dataParts[0] == 'personal':
            msg = unquote(dataParts[2]).decode("gbk")
            sender = int(dataParts[1])
            message = receivedMessage(sourceType=dataParts[0], fromGroupID=0, fromID=sender, content=msg)
        for i in self.messageHandlers:
            i(message)

class coolqBot():
    def __init__(self, py2cqPort, cq2pyPort):
        self.sendPort = py2cqPort
        self.receivePort = cq2pyPort
        self.messageHandlers = []

        self.sock = socket.socket(type=socket.SOCK_DGRAM)
        self.sock.connect(("127.0.0.1", self.sendPort))
        self.listener = messagePreprocessor(("0.0.0.0", self.receivePort))
        self.listener.setMessageHandlers(self.messageHandlers)

    def send(self, sendMessage):
        self.sock.send(sendMessage.destinationType + " " + str(sendMessage.destinationID) + " " + quote(
            sendMessage.content.encode('utf-8')))
        return 0

    def listenerStarter(self):
        self.listener.start()

    def startListen(self):
        poll = threading.Thread(target=self.listenerStarter)
        poll.setDaemon(True)
        poll.start()

    def qqMessageHandler(self):
        def decorator(handler):
            self.messageHandlers.append(handler)
            return handler

        return decorator
