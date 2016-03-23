# coding : UTF-8
from __future__ import division
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
import sys
import logging
import pycoolq

listenPort = int(sys.argv[1])
sendPort = int(sys.argv[2])


qqbot = pycoolq.coolqBot(py2cqPort=sendPort, cq2pyPort=listenPort)


@qqbot.qqMessageHandler()
def pass2TG(message):
    logging.warning(message.sourceType + " " + str(message.fromGroupID) + " " + message.content)
    if message.sourceType == "group" and message.fromGroupID == botconfig.qqGroupID:
        msg = message.content
        sender = message.fromID
    if sentChat == botconfig.telegramGroupID:
        sendMessage = pycoolq.sendMessage("group", botconfig.qqGroupID, "[%s] %s" % (senderName, textContent))
        qqbot.send(sendMessage)



qqbot.startListen()