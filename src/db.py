import sqlite3
import logging as log
from datetime import date


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
                '../data/schedule_users.db',
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

        sql = f'DELETE FROM users WHERE chat_id = {id}'

        try:
            self.cur.execute(sql)
            self.dbase.commit()
        except BaseException:
            log.exception("Inserting failed")

    def set_user(self, id, name, group_name, subgroup):
        log.info(f"Inserting user {id}")

        sql = 'INSERT INTO users(chat_id, name, group_name, subgroup, last_message_time) VALUES(?, ?, ?, ?, ?)'

        try:
            self.cur.execute(
                sql, (id, name, group_name, subgroup, date.today().isoformat()))
            self.dbase.commit()
        except BaseException:
            log.exception("Inserting failed")

    def get_user(self, id):
        sql = f'SELECT * FROM users WHERE chat_id = {id};'

        try:
            self.cur.execute(sql)
            return self.cur.fetchone()
        except Exception as e:
            log.exception(f"Get user failed {str(e)}.")

    def update_time(self, id):
        sql = f'UPDATE users SET last_message_time = {date.today().isoformat()} where id = {id}'

        try:
            self.cur.execute(sql)
        except Exception as e:
            log.exception("Time updating failed")

        self.dbase.commit()

    def create_users_table(self):
        log.info("Creating users table.")
        sql = '''
            CREATE TABLE IF NOT EXISTS users (
            rowid INTEGER PRIMARY KEY,
            chat_id INTEGER,
            name TEXT,
            group_name TEXT NOT NULL,
            subgroup INTEGER,
            last_message_time TEXT NOT NULL);
            '''

        try:
            self.cur.executescript(sql)
        except Exception as e:
            log.exception(f"Creating table failed. {str(e)}")

        self.dbase.commit()
