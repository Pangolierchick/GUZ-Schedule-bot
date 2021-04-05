import sqlite3
import logging as log

class guzDB:
    instance = None
    def __init__(self):
        if self.instance is None:
            self.connect_to_db()
            self.get_cur()

            self.create_table()
            return self
        
        print("Error: this class is singleton")
    
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
    
    def set_schedule_by_date(self, date:str, schedule:str) -> None:
        log.info(f'Setting schedule at {date}')

        sql = f'UPDATE arch SET schedule = ? WHERE date = {date}'

        try:
            self.cur.execute(sql, tuple(schedule))
            self.dbase.commit()

            log.info("Inserting done.")
        except Exception as e:
            log.exception('Inserting failed')

    def get_schedule_by_date(self, date:str) -> str:
        log.info(f'Getting schedule at {date}')

        sql = f"SELECT * FROM arch WHERE date = {date}"

        try:
            self.cur.execute(sql, tuple(date))
            self.dbase.commit()
            log.info("Getting done.")

            return self.cur.fetchone()
        except Exception as e:
            log.exception('Getting failed')

    def load_default_schedule(self, filename:str):
        try:
            f = open(filename, 'r')
        except OSError:
            log.exception("Failed loading default schedule.")
        
        
        f.close()
