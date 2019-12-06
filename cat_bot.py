from glob import glob
import logging
from random import choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/*')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))


def main():
    mybot = Updater(settings.key)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()

  
if __name__ == "__main__":
    main()