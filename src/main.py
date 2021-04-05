import telebot
import logging as log
import threading
import db
import re
import utils

API_TOKEN = '1716037279:AAEg3jW-K9bY_Hsd7nRSwRevhLE1l8Bs8Xc'
log.basicConfig(filename="../data/guz.log", format='%(asctime)s [ %(levelname)s ] %(message)s', datefmt='[ %d-%m-%y %H:%M:%S ] ')

dbase = db.guzDB()

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help'])
def help_handler(message):
    help_msg = 'Привет!' # TODO help message
    bot.reply_to(message, help_msg)

@bot.message_handler(commands=['today'])
def get_today_schedule_handler(message):
    today = dbase.get_today_schedule()[2]
    today = today.replace(' ; ', '\n')
    bot.reply_to(message, today)

@bot.message_handler(commands=['date'])
def get_schedule_by_date_handler(message):
    sent = bot.reply_to(message, 'Напишите дату, пожалуйста')
    bot.register_next_step_handler(sent, input_date_get_sch)

@bot.message_handler(commands=['change'])
def set_schedule_by_date_handler(message):
    pass

@bot.message_handler(regexp='\d+.\d+.\d+')
def handle_message(message):
    bot.reply_to(message, "Сейчас отправлю расписание.")

    req = utils.format_time(message.text)
    print(req)

    sch = dbase.get_schedule_by_date(req)
    
    if sch is None:
        sch = "Не получилось."
    else:
        sch = sch[2]
        sch = sch.replace(' ; ', '\n')

    bot.send_message(message.chat.id, sch)


def input_date_get_sch(message):
    text = message.text

    if re.match('\d+.\d+.\d+', text):
        req = utils.format_time(message.text)
        sch = dbase.get_schedule_by_date(req)[2]
        msg = sch.replace(' ; ', '\n')
        
    else:
        msg = 'Неправильно указана дата, попробуйте еще раз'
    bot.send_message(message.chat.id, msg)

update_db = threading.Thread(target=db.updateEveryWeek, args=(dbase, ), daemon=True, name='WeekUpdater')

update_db.start()
bot.polling()
