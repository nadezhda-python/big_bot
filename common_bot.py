import logging
from random import choice

from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        emoji_list = []
        with open ('emoji_list.txt', 'r', encoding='utf-8') as file:
            for emoji in file:
                emoji_list.append(emoji.replace('\n', ''))
        user_data['emo'] = emojize(choice(emoji_list), use_aliases=True)
        return user_data['emo']


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
            del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Окей, держи другую {}'.format(emo))


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = 'Привет {} {}! Ты написал: {}'.format(update.message.chat.first_name, emo, update.message.text)
    print(user_text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(settings.key)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()