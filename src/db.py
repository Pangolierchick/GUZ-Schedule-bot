import sqlite3
import logging as log
from calendar import Calendar
from schedule import Schedule 
from datetime import date
import time

def getCurrentWeek():
    calendar = Calendar(0)

    today = str(date.today()).split('-')
    year  = int(today[0])
    month = int(today[1])
    day   = int(today[2])

    month_list = [i for i in calendar.itermonthdays3(year, month)]

    week = []
    
    for i, v in enumerate(month_list):
        if (v[0] == year and v[1] == month and v[2] == day):
            for k in range(7):
                week.append(month_list[i + k])
            
            return week


class guzDB:
    instance = None
    def __init__(self):
        if self.instance is None:
            self.connect_to_db()
            self.get_cur()

            self.create_table()

            guzDB.instance = self
        else:
            print("Error: this class is singleton")
    
    def getInstance(self):
        return guzDB.instance
        
    
    def connect_to_db(self):
        log.info('Connecting to base ...')
        try:
            self.dbase = sqlite3.connect('../data/guz_arch_schedule.db')
        except Exception as e:
            log.exception(f'Connection to data base failed {str(e)}')

    def get_cur(self):
        self.cur = self.dbase.cursor()
        return self.cur
    
    def create_table(self):
        log.info("Creating table.")
        sql = '''
            CREATE TABLE IF NOT EXISTS arch (
            rowid INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            schedule TEXT)
              '''

        try:
            self.cur.executescript(sql)
        except Exception as e:
            log.exception("Creating table failed.")
    
    def update_schedule_by_date(self, date:str, schedule:str) -> None:
        log.info(f'Updatting schedule at {date}')

        sql = f'UPDATE arch SET schedule = ? WHERE date = "{date}";'

        try:
            self.cur.execute(sql, (schedule, ))
            self.dbase.commit()

            log.info("Updating done.")
        except Exception as e:
            log.exception('Updating failed')

    def set_schedule_by_date(self, date:str, schedule:str) -> None:
        log.info(f'Setting schedule at {date}')

        sql = "INSERT INTO arch(date, schedule) VALUES(?, ?)"

        try:
            self.cur.execute(sql, (date, schedule))
            self.dbase.commit()

            log.info("Setting done.")
        except Exception as e:
            log.exception('Setting failed')

    def get_schedule_by_date(self, date:str) -> str:
        log.info(f'Getting schedule at {date}')

        sql = f"SELECT * FROM arch WHERE date = ?;"

        try:
            self.cur.execute(sql, (date,))
            self.dbase.commit()
            log.info("Getting done.")

            return self.cur.fetchone()
        except Exception as e:
            log.exception('Getting failed')

    def load_default_schedule(self, filename:str):
        schedule = Schedule()
        schedule.parse_schedule_file(filename)

        week = getCurrentWeek()

        for w, i in enumerate(week):
            year, month, day = i[0], i[1], i[2]
            self.set_schedule_by_date(f'{day}-{month}-{year}', schedule.getByDay(w))

def updateEveryWeek(dbase:guzDB):
    while True:
        log.info("Reloading the base")
        dbase.load_default_schedule('../data/default.csv')
        time.sleep(604800)
