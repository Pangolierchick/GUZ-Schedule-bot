import telebot
import logging as log

API_TOKEN = '1716037279:AAEg3jW-K9bY_Hsd7nRSwRevhLE1l8Bs8Xc'

log.basicConfig(filename="../data/guz.log", level=log.INFO, format='%(asctime)s [ %(levelname)s ] %(message)s', datefmt='[ %d-%m-%y %H:%M:%S ] ')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(command='help')
def help_handler(message):
    help_msg = 'Привет!'
    bot.reply_to(message, help_msg)

@bot.message_handler(command='today')
def get_today_schedule_handler(message):
    pass

@bot.message_handler(command='date')
def get_schedule_by_date_handler(message):
    pass

@bot.message_handler(command='change')
def set_schedule_by_date_handler(message):
    pass

bot.polling()
