from datetime import datetime
import logging

import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')


def get_next_full_moon(user_date):
    try:
        formatted_user_date = datetime.strptime(user_date, '%Y-%m-%d')
        return ephem.next_full_moon(formatted_user_date)
    except ValueError:
        try:
            formatted_user_date = datetime.strptime(user_date, '%Y/%m/%d')
            return ephem.next_full_moon(formatted_user_date)
        except:
            return 'Wrong date, try again please in format 1970-01-01 or 1970/01/01'


def get_next_full_moon_bot(bot, update, user_data):
    user_date = update.message.text.split()[-1]
    print(user_date)
    result = get_next_full_moon(user_date)
    print(result)
    update.message.reply_text(result)


def get_planet_constellation(planet):
    try:
        return ephem.constellation(getattr(ephem, planet)(datetime.today()))
    except AttributeError:
        return 'Incorrect planet name, try again please'


def get_planet_constellation_bot(bot, update, user_data):
    planet = update.message.text.split()[-1].capitalize()
    print(planet)
    result = get_planet_constellation(planet)
    print(result)
    update.message.reply_text(result)


def main():
    mybot = Updater(settings.key)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("next_full_moon", get_next_full_moon_bot, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", get_planet_constellation_bot, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()
       
if __name__ == "__main__":
    main()
