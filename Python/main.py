# coding: UTF-8

import sys
import logging

from botconfig import botconfig

reload(sys)
sys.setdefaultencoding('utf-8')
import telebot
import pycoolq

telegramToken = botconfig.telegramToken

tgbot = telebot.TeleBot(token=telegramToken)

listenPort = int(sys.argv[1])
sendPort = int(sys.argv[2])

qqbot = pycoolq.coolqBot(py2cqPort=sendPort, cq2pyPort=listenPort)


@tgbot.message_handler()
def groupPassQQ(message):
    textContent = message.text.encode('utf-8')
    sentChat = message.chat.id
    logging.warning("Telegram Message Received")
    senderName = message.from_user.first_name
    if message.from_user.last_name:
        senderName += " " + message.from_user.last_name

    if sentChat == botconfig.telegramGroupID:
        sendMessage = pycoolq.sendMessage("group", botconfig.qqGroupID, "[%s] %s" % (senderName, textContent))
        qqbot.send(sendMessage)


@qqbot.qqMessageHandler()
def pass2TG(message):
    logging.warning(message.sourceType + " " + str(message.fromGroupID) + " " + message.content)
    if message.sourceType == "group" and message.fromGroupID == botconfig.qqGroupID:
        msg = message.content
        sender = message.fromID
        tgbot.send_message(chat_id=botconfig.telegramGroupID, text="[%s] %s" % (sender, msg))


qqbot.startListen()
tgbot.polling(none_stop=True)
