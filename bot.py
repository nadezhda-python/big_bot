import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup

from calculator_bot import calculation_bot
from cat_bot import send_cat_picture
from cities_bot import play_cities_bot
from common_bot import change_avatar, get_user_emo, talk_to_me
import settings
from space_bot import get_next_full_moon_bot, get_planet_constellation_bot


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    text = f'Привет {emo}'
    print(text)
    my_keyboard = ReplyKeyboardMarkup([
        ['Прислать котика', 'Сменить аватар']])
    update.message.reply_text(text, reply_markup=my_keyboard)


def main():
    mybot = Updater(settings.key)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('next_full_moon', get_next_full_moon_bot, pass_user_data=True))
    dp.add_handler(CommandHandler('planet', get_planet_constellation_bot, pass_user_data=True))
    dp.add_handler(CommandHandler('cities', play_cities_bot, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватар)$', change_avatar, pass_user_data=True))
    dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("calc", calculation_bot, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()
    

if __name__ == '__main__':
    main()
