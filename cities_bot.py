import logging
from random import shuffle
import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')


def define_cities_user_data(user_data):
    if 'virgin_city_list' not in user_data:
        virgin_city_list = []
        with open('city.txt', encoding='utf-8') as file:
            for city in file:
                virgin_city_list.append(city.strip())
        user_data['virgin_city_list'] = virgin_city_list
    if 'city_list' not in user_data:
        city_list = user_data['virgin_city_list'].copy()
        shuffle(city_list)
        user_data['city_list'] = city_list
    if 'last_output_city' not in user_data:
        user_data['last_output_city'] = ''


def normalize_city_name(city):
    return city.replace('ё', 'е').replace('й', 'и').replace('ь', '').replace('ы', '').lower()


def validate_city_for_game_step(input_city, last_output_city):
    """проверяем что новый город начинается с последней буквы последнего"""
    input_first_letter = normalize_city_name(input_city)[0]
    last_output_last_letter = normalize_city_name(last_output_city)[-1]
    if input_first_letter == last_output_last_letter:
        return True
    else:
        return False

def validate_input_city(input_city, user_data):
    message = ''
    if input_city == '':
        message = 'Дайте мне город!'
    elif input_city.capitalize() not in user_data['virgin_city_list']:
        message = 'Я не знаю такого города, попробуйте еще :)'
    elif input_city.capitalize() not in user_data['city_list']:
        message = 'У нас уже был этот город! Давай что-то другое'
    elif user_data['last_output_city'] != '' and not validate_city_for_game_step(input_city, user_data['last_output_city']):
        message  = f'Первая буква не {normalize_city_name(user_data["last_output_city"])[-1]}, давай что-то другое.'
    return message

def play_cities(input_city, user_data):
    if validate_input_city(input_city, user_data) != '':
        return validate_input_city(input_city, user_data)
    else:
        user_data['city_list'].remove(input_city.capitalize())
        for city in user_data['city_list']:
            if validate_city_for_game_step(city, input_city):
                user_data['last_output_city'] = city
                break 
            else:
                user_data['last_output_city'] = 'Я не могу больше ничего придумать, ты победил!'
        user_data['city_list'].remove(user_data['last_output_city'])
        return user_data['last_output_city']


def play_cities_bot(bot, update, user_data):
    define_cities_user_data(user_data)
    text = update.message.text
    input_city = re.sub('^/cities', '', text).strip()
    if input_city == 'стоп':
        message = 'Ок, конец так конец.'
        print (message)
        update.message.reply_text(message)
        user_data['last_output_city'] = ''
        user_data['city_list'] = shuffle(user_data['virgin_city_list'].copy())    
    else:
        print(input_city)
        output_city = play_cities(input_city, user_data)
        print (output_city)
        update.message.reply_text(output_city)


def main():
    mybot = Updater(settings.key)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("cities", play_cities_bot, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()
       
if __name__ == "__main__":
    main()
