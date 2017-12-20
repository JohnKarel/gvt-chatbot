from telegram.ext import Updater, MessageHandler,  Filters
import logging
import time
import threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token= '')

dispatcher = updater.dispatcher

updater.start_polling()

recently_joined = {}

def handleMessage(bot, update):
    if("https://t.me" in update.message.text):
        if (update.message.from_user.username in recently_joined):
            bot.kickChatMember(update.message.chat.id, update.message.from_user.id)
        bot.deleteMessage(update.message.chat.id, update.message.message_id)

def handleGroupJoin(bot, update):
    if(update.message.new_chat_member != None):
        recently_joined[update.message.new_chat_member.username] = int(time.time())

message_handler = MessageHandler(Filters.text, handleMessage)
groupjoin_handler = MessageHandler(Filters.group, handleGroupJoin)

dispatcher.add_handler(message_handler)
dispatcher.add_handler(groupjoin_handler)


# Delete the user from the recently_joined group after 10 minutes
def clean_joined():
    while(True):
        for key in recently_joined.keys():
            value = recently_joined[key]
            if(int(time.time()) - value > 30):
                del recently_joined[key]
        time.sleep(10)

threading.Thread(target=clean_joined()).start()
