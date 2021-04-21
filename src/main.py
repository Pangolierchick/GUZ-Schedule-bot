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
from schedule_pool import SchedulePool
import myschedule
import transliterate

log.basicConfig(
    filename="../data/bot.log",
    level=log.DEBUG,
    format='%(asctime)s [ %(levelname)s ] %(message)s',
    datefmt='[ %d-%m-%y %H:%M:%S ] ')

dbase = db.guzDB()
sched_pool = SchedulePool(utils.get_week_type())

bot = telebot.AsyncTeleBot(API_TOKEN, threaded=False)

lock = threading.Lock()


MY_VERSION = '1_beta'


@bot.message_handler(commands=['help', 'start'])
def help_handler(message):
    help_msg = '''Привет!\nЭтот бот будет присылать тебе расписание.
    Комманды:
    /help вывести это сообщение.
    /today (или можешь просто написать сегодня) покажет тебе сегодняшнее расписание.
    Также ты можешь просто написать день недели и бот вышлет тебе расписание на этот день. Или ты можешь написать завтра.
    /register регистрация пользователя
    /unregister удаление аккаунта пользователя
    /info информация о создателе бота


    Также бот будет присылать тебе каждый будний день расписание на сегодня. (TODO: возможность отписаться от этого)
    '''
    bot.reply_to(message, help_msg)


@bot.message_handler(commands=['today'])
@bot.message_handler(func=lambda msg: msg.text.lower() == 'сегодня')
def get_today_schedule_handler(message):
    log.debug('Got <today> request.')

    with lock:
        group = dbase.get_user(message.from_user.id)

    if group is None:
        bot.reply_to(
            message,
            'Вы не зарегестрированы. Напишите /register, чтобы зарегестрироваться')
        return

    try:
        schedule = sched_pool.get_schedule(group[3], group[4])
        bot.reply_to(message, str(schedule.get_today()))
        dbase.update_time(message.chat.id)
    except Exception as e:
        log.error(f"Failed get schedule: {str(e)}")
        bot.reply_to(message, 'Не получилось.')


@bot.message_handler(commands=['change'])
def set_schedule_by_date_handler(message):
    log.debug('Got <change> request')

    bot.send_message(message.chat.id, 'TODO_CHANGE')


@bot.message_handler(func=lambda msg: msg.text.capitalize() == 'Завтра')
def tomorrow_handler(message):
    log.debug('Got <tomorrow> request')
    with lock:
        user = dbase.get_user(message.from_user.id)

    if user is None:
        bot.send_message(
            message.chat.id,
            'Вы не зарегестрированы. Напишите /register, чтобы зарегестрироваться')

    tomorrow_weekday = (date.today().weekday() + 1) % 7

    try:
        schedule = sched_pool.get_schedule(user[3], user[4])
        bot.reply_to(message, str(schedule.get_day_at(tomorrow_weekday)))
        dbase.update_time(message.chat.id)
    except Exception as e:
        log.error(f"Failed get schedule: {str(e)}")
        bot.reply_to(message, 'Не получилось.')


@bot.message_handler(commands=['register'])
def register_user(message):
    log.debug('Got <register> request')
    with lock:
        user = dbase.get_user(message.from_user.id)

    if user is not None:
        bot.send_message(message.chat.id, 'Вы уже зарегестрированы')
        return

    sent = bot.send_message(
        message.chat.id,
        'Напишите вашу группу с подгруппой через _ (Пример: 21A_1 или 21A_2)')
    bot.register_next_step_handler(sent, insert_user_into_base)


@bot.message_handler(commands=['info'])
def send_info(message):
    log.debug('Got <info> request')
    bot.send_message(
        message.chat.id,
        f"Бот, написанный для вуза гуз, архитектурный факультет. \nСоздатель: telegram: @pangolierchick (https://github.com/Pangolierchick/GUZ-Schedule-bot). Версия: {MY_VERSION}")


def insert_user_into_base(message):
    msg = message.text
    try:
        msg = transliterate.translit(message.text.upper(), reversed=True)
    except BaseException:
        pass

    if not re.match(r'\d\d[A-Z]_\d', msg):
        bot.send_message(message.chat.id, 'Неправильно указана группа.')
        return

    group, subgroup = msg.split('_')

    try:
        sched_pool.load_schedule(group, subgroup)
    except Exception as e:
        bot.send_message(
            message.chat.id,
            'К сожалению, расписание для вашей группы отсутствует.')
        return
    with lock:
        dbase.set_user(
            message.from_user.id,
            message.from_user.username,
            group,
            subgroup)
    bot.send_message(message.chat.id, 'Вы были успешно зарегестрированы')


@bot.message_handler(commands=['unregister'])
def un_register_user(message):
    log.debug('Got <unregister> request')
    with lock:
        user = dbase.get_user(message.from_user.id)

    if user is None:
        bot.send_message(
            message.chat.id,
            'Вы не зарегестрированы. Напишите /register, чтобы зарегестрироваться')
        return

    dbase.delete_user(message.from_user.id)
    bot.send_message(message.chat.id, 'Ваш аккаунт успешно удален.')


@bot.message_handler(commands=['force'])
def force_morning(message):
    log.debug('Got <force> request')
    morning_send_schedule()


@bot.message_handler(func=lambda msg: msg.text.capitalize()
                     in myschedule.WEEK_DAY_LOCALE)
def schedule_at_week_day_handler(message):
    log.debug('Got <schedule at dat> request')
    with lock:
        user = dbase.get_user(message.chat.id)

    if user is None:
        bot.send_message(
            message.chat.id,
            'Вы не зарегестрированы. Напишите /register, чтобы зарегестрироваться')
        return

    sch = sched_pool.get_schedule(user[3], user[4])
    msg = sch.get_day_at(
        myschedule.STRING_NUM_WEEKDAY[message.text.capitalize()])
    # dbase.update_time(message.chat.id)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['clean'])
def clean_handler(message):
    log.debug('Got <clean> request')
    sched_pool.clean_pool()
    bot.send_message(message.chat.id, 'Pool has been cleaned')


def morning_send_schedule():
    if date.today().weekday() > 4:
        log.info("It is holiday. We dont send schedule on its day.")
        return

    with lock:
        users = dbase.get_all_users()

    log.info(f'Sending morning schedule for {len(users)} users ...')

    for i in users:
        try:
            schedule = sched_pool.get_schedule(i[3], i[4])
        except Exception as e:
            log.error(f"Failed get schedule: {str(e)}")

        sch = str(schedule.get_today())

        if i[2] is None:
            name = ', '
        else:
            name = ', ' + i[2] + ','

        bot.send_message(
            i[1], f'Доброе утро{name}твое расписание на сегодня:\n\n {sch}')
        time.sleep(2)

    log.info('Done morning schedule')


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(10)


schedule.every().day.at("07:30").do(morning_send_schedule)
schedule.every().monday.at("05:30").do(sched_pool.clean_pool)

threading.Thread(target=schedule_checker).start()

bot.polling(none_stop=True, interval=0, timeout=5)
