import re

from calendar import Calendar
from datetime import date

def getCurrentWeek():
    calendar = Calendar(0)

    today = date.today()
    week_day = today.weekday()
    today = today.replace(day=today.day - week_day)

    today = str(today.isoformat()).split('-')
    year  = int(today[0])
    month = int(today[1])
    day   = int(today[2])

    month_list = [i for i in calendar.itermonthdays3(year, month)]

    week = []

    for i, v in enumerate(month_list):
        if (v[0] == year and v[1] == month and v[2] == day):
            for k in range(5):
                week.append(month_list[i + k])

            return week

def get_week_type():
    _, week_num, __ = date.today().isocalendar()

    return week_num % 2 == 0


def format_time(time: str):
    if not re.match(r'\d+.\d+.\d+', time):
        return time

    new_time = ''

    for i, v in enumerate(time.split('.')):
        new_time += str(int(v))
        if (i < 2):
            new_time += '-'

    return new_time
