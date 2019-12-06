import logging
import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')


def calculation(text):
    arithmetic_pattern = '\/calc\s?\d+\.?\d?\s*[-+*\/]\s*\d+\.?\d?\s*$'
    if not re.match(arithmetic_pattern, text):
        return('Неверное арифметичесикое выражение')
    else:
        text = re.sub('^/calc', '', text).strip()
        number_regexp = '\d+\.?\d?'
        operation_regexp = '[-+*\/]'
        numbers = list(map(float, re.findall(number_regexp, text)))
        operation = re.findall(operation_regexp, text)[0]
        if operation == '-':
            return numbers[0] - numbers[1]
        if operation == '+':
            return numbers[0] + numbers[1]
        if operation == '*':
            return numbers[0] * numbers[1]
        if operation == '/':
            try:
                return numbers[0] / numbers[1]
            except ZeroDivisionError:
                return 'На ноль нельзя делить!'


def calculation_bot(bot, update, user_data):
    text = update.message.text
    result = calculation(text)
    update.message.reply_text(result)


def main():
    mybot = Updater(settings.key)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("calc", calculation_bot, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()

  
if __name__ == "__main__":
    main()