import telebot
from telebot import types
import logging as log
import threading
import db
import re
import utils
import schedule
import time
from datetime import date
from config import API_TOKEN

log.basicConfig(
    filename="../data/bot.log",
    level=log.INFO,
    format='%(asctime)s [ %(levelname)s ] %(message)s',
    datefmt='[ %d-%m-%y %H:%M:%S ] ')

dbase = db.guzDB()

bot = telebot.TeleBot(API_TOKEN)


MY_VERSION = '2_alpha'


def check_registration(id):
    user = dbase.get_user(id)

    return user is not None


def get_user_group(id):
    user = dbase.get_user(id)

    if user is None:
        return None

    return user[3] - 1


@bot.message_handler(commands=['help', 'start'])
def help_handler(message):
    help_msg = '''Привет!\nЭтот бот будет присылать тебе расписание.
    Комманды:
    /help вывести это сообщение.
    /today (или можешь просто написать сегодня) покажет тебе сегодняшнее расписание.
    /date выведет тебе расписание по дате (или можешь просто написать дату вроде 03.03.2021)
    /change комманда, нужная чтобы изменить расписание какого-то числа (TODO)
    /register регистрация пользователя
    /unregister удаление аккаунта пользователя
    /info информация о создателе бота

    Также бот будет присылать тебе каждый будний день расписание на сегодня. (TODO: возможность отписаться от этого)
    '''
    bot.reply_to(message, help_msg)


@bot.message_handler(commands=['today'])
@bot.message_handler(func=lambda msg: msg.text.lower() == 'сегодня')
def get_today_schedule_handler(message):
    group = get_user_group(message.from_user.id)

    if group is None:
        bot.reply_to(
            message,
            'Вы не зарегестрированы. Напишите /register, чтобы зарегестрироваться')
        return

    today = dbase.get_today_schedule(group)

    if today is None:
        bot.reply_to(message, 'Не получилось.')
        return

    bot.reply_to(message, today)


@bot.message_handler(commands=['date'])
def get_schedule_by_date_handler(message):
    sent = bot.reply_to(message, 'Напишите дату, пожалуйста')
    bot.register_next_step_handler(sent, input_date_get_sch)


@bot.message_handler(commands=['change'])
def set_schedule_by_date_handler(message):
    bot.send_message(message.chat.id, 'TODO_CHANGE')


@bot.message_handler(regexp=r'\d+\.\d+\.\d+')
def handle_message(message):
    bot.reply_to(message, "Сейчас отправлю расписание.")

    req = utils.format_time(message.text)

    sch = dbase.get_group_schedule_by_date(req)

    if sch is None:
        sch = "Не получилось."

    bot.send_message(message.chat.id, sch)


def input_date_get_sch(message):
    text = message.text

    if re.match(r'\d+\.\d+\.\d+', text):
        req = utils.format_time(message.text)
        group = get_user_group(message.from_user.id)

        if (group is None):
            bot.reply_to(
                message,
                'Вы не зарегестрированы. Напишите /register, чтобы зарегестрироваться')
            return

        msg = dbase.get_group_schedule_by_date(req, group)

    else:
        msg = 'Неправильно указана дата, попробуйте еще раз'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['register'])
def register_user(message):
    user = dbase.get_user(message.from_user.id)

    if user is not None:
        bot.send_message(message.chat.id, 'Вы уже зарегестрированы')
        return

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('1')
    itembtn2 = types.KeyboardButton('2')
    markup.row(itembtn1, itembtn2)

    sent = bot.send_message(
        message.chat.id,
        'Выберите вашу группу: ',
        reply_markup=markup)
    bot.register_next_step_handler(sent, insert_user_into_base)


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(
        message.chat.id,
        f"Бот, написанный для вуза гуз, архитектурный факультет. Создатель: telegram: @pangolierchick (https://github.com/Pangolierchick/GUZ-Schedule-bot). Версия: {MY_VERSION}")


def insert_user_into_base(message):
    dbase.set_user(
        message.from_user.id,
        message.from_user.username,
        message.text)
    bot.send_message(message.chat.id, 'Вы зарегестрированы')


@bot.message_handler(commands=['unregister'])
def un_register_user(message):
    user = dbase.get_user(message.from_user.id)

    if user is None:
        bot.send_message(message.chat.id, 'Вы не зарегестрированы')
        return

    dbase.delete_user(message.from_user.id)
    bot.send_message(message.chat.id, 'Ваш аккаунт успешно удален.')


@bot.message_handler(commands=['force'])
def force_morning(message):
    morning_send_schedule()


def morning_send_schedule():
    if date.today().weekday() > 4:
        log.info("It is holiday. We dont send schedule on its day.")
        return

    users = dbase.get_all_users()
    log.info(f'Sending morning schedule for {len(users)} users ...')

    for i in users:
        sch = dbase.get_today_schedule(i[3] - 1)
        name = ', ' + i[2] + ','

        if i[2] is None:
            name = ', '

        bot.send_message(
            i[1], f'Доброе утро{name}твое расписание на сегодня:\n {sch}')
        time.sleep(2)

    log.info('Done morning schedule')


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(2)


schedule.every().day.at("07:30").do(morning_send_schedule)
schedule.every().monday.at("05:30").do(db.updateEveryWeek, dbase=dbase)

threading.Thread(target=schedule_checker).start()

bot.polling()
