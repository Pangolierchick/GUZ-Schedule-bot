import sqlite3
import logging as log
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


class guzDB:
    instance = None

    def __init__(self):
        if self.instance is None:
            self.connect_to_db()
            self.get_cur()

            self.create_users_table()

            guzDB.instance = self
        else:
            print("Error: this class is singleton")

    def getInstance(self):
        return guzDB.instance

    def connect_to_db(self):
        log.info('Connecting to base ...')
        try:
            self.dbase = sqlite3.connect(
                '../data/guz_arch_schedule.db',
                check_same_thread=False)
        except Exception as e:
            log.exception(f'Connection to data base failed {str(e)}')

    def get_cur(self):
        self.cur = self.dbase.cursor()
        return self.cur

    def get_all_users(self):
        sql = f'SELECT * FROM users'

        try:
            self.cur.execute(sql)
        except Exception as e:
            log.exception(f"Get all users failed {str(e)}")

        return self.cur.fetchall()

    def delete_user(self, id):
        log.info(f"Deleting user {id}")

        sql = f'DELETE FROM users WHERE id = {id}'

        try:
            self.cur.execute(sql)
            self.dbase.commit()
        except BaseException:
            log.exception("Inserting failed")

    def set_user(self, id, name, group, subgroup):
        log.info(f"Inserting user {id}")

        sql = 'INSERT INTO users(id, name, group, subgroup, last_message_time) VALUES(?, ?, ?, ?, ?)'


        try:
            self.cur.execute(sql, (id, name, group, subgroup, date.today().isoformat()))
            self.dbase.commit()
        except BaseException:
            log.exception("Inserting failed")

    def get_user(self, id):
        sql = f'SELECT * FROM users WHERE id = {id};'

        try:
            self.cur.execute(sql)
            return self.cur.fetchone()
        except Exception as e:
            log.exception(f"Get user failed {str(e)}.")


    def create_users_table(self):
        log.info("Creating users table.")
        sql = '''
            CREATE TABLE IF NOT EXISTS users (
            rowid INTEGER PRIMARY KEY,
            id INTEGER,
            name TEXT,
            group TEXT NOT NULL,
            subgroup INTEGER,
            last_message_time TEXT NOT NULL);
            '''

        try:
            self.cur.executescript(sql)
        except Exception as e:
            log.exception("Creating table failed.")

        self.dbase.commit()
