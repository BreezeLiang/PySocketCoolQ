# coding: UTF-8

import logging
import sys

from botconfig import botconfig

reload(sys)
sys.setdefaultencoding('utf-8')
import telebot
from Python.pypi import pycoolq

telegramToken = botconfig.telegramToken

tgbot = telebot.TeleBot(token=telegramToken)

listenPort = int(sys.argv[1])
sendPort = int(sys.argv[2])

qqbot = pycoolq.coolqBot(py2cqPort=sendPort, cq2pyPort=listenPort)


@tgbot.message_handler()
def groupPassQQ(message):
    textContent = message.text.encode('utf8')
    sentChat = message.chat.id
    logging.warning("Telegram Message Received")
    senderName = str(message.from_user.first_name) + " " + str(message.from_user.last_name)

    if str(sentChat) == str(botconfig.telegramGroupID):
        sendMessage = pycoolq.sendMessage("group", botconfig.qqGroupID, "[" + senderName + "]" + textContent)
        qqbot.send(sendMessage)


@qqbot.qqMessageHandler()
def pass2TG(message):
    logging.warning(message.sourceType + " " + str(message.fromGroupID) + " " + message.content)
    if message.sourceType == "group":
        sendGroup = message.fromGroupID
        if int(sendGroup) == botconfig.qqGroupID:
            msg = message.content
            sender = message.fromID
            tgbot.send_message(chat_id=botconfig.telegramGroupID, text="[" + str(sender) + "] " + msg)


qqbot.startListen()
tgbot.polling(none_stop=True)
