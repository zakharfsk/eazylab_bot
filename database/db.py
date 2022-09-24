import os

import psycopg2


class DataBase:
    def __int__(self):
        self.conn = psycopg2.connect(
            user=os.getenv('USER'),
            host=os.getenv('HOST'),
            database=os.getenv('DATABASE'),
            password=os.getenv('PASSWORD'),
            port=5432
        )
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        if self.conn:
            self.cursor.close()
            self.conn.close()


class User(DataBase):
    def __init__(self):
        super().__init__()

    def get_user_by_id(self, user_id):
        self.cursor.execute(f'SELECT id FROM user_info WHERE id = {user_id};')
        return self.cursor.fetchone()

    def add_new_user(self, user_id, username, first_name, last_name):
        self.cursor.execute(
            f'INSERT INTO user_info (id, username, first_name, last_name) '
            f'VALUES ({user_id}, \'{username}\', '
            f'\'{first_name}\', \'{last_name}\');'
        )
        self.conn.commit()
