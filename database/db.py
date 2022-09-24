import os
import logging

import psycopg2


class DataBase:
    def __int__(self):
        self.conn = psycopg2.connect(
            user=os.getenv('USER_DB'),
            host=os.getenv('HOST_DB'),
            database=os.getenv('DATABASE_DB'),
            password=os.getenv('PASSWORD_DB'),
            port=5432
        )
        self.cursor = self.conn.cursor()
        logging.info('Connected to database')

    def __del__(self):
        self.conn.commit()
        if self.conn:
            self.cursor.close()
            self.conn.close()
            logging.info('Database connection closed.')


class User(DataBase):
    def __init__(self):
        super().__init__()

    def get_user_by_id(self, user_id: int) -> tuple:
        logging.info(os.getenv('USER_DB'))
        logging.info(os.getenv('HOST_DB'))
        logging.info(os.getenv('DATABASE_DB'))
        logging.info(os.getenv('PASSWORD_DB'))
        self.cursor.execute(f'SELECT id FROM user_info WHERE id = {user_id};')
        return self.cursor.fetchone()

    def add_new_user(self, user_id: int, username: str, first_name: str, last_name: str) -> None:
        self.cursor.execute(
            f'INSERT INTO user_info (id, username, first_name, last_name) '
            f'VALUES ({user_id}, \'{username}\', '
            f'\'{first_name}\', \'{last_name}\');'
        )
        self.conn.commit()

    def get_all_users(self) -> list[tuple]:
        self.cursor.execute(f'SELECT id FROM user_info')
        return self.cursor.fetchall()

    def delete_user(self, user_id) -> None:
        self.cursor.execute(f'DELETE FROM user_info WHERE id = {user_id}')


class Orders(DataBase):
    def __int__(self):
        super().__init__()

    def create_english_order(self, id_order, id_customer, name_object, user_group, file_id, task) -> None:
        self.cursor.execute(
            'INSERT INTO public.order_info_english(id_order, id_customer, name_object, user_group, file_id, task) '
            f'VALUES ('
            f'{id_order}, '
            f'{id_customer}, '
            f'\'{name_object}\', '
            f'\'{user_group}\', '
            f'\'{file_id}\', '
            f'\'{task}\''
            f');'
        )

    def create_order_it(self,
                        id_order,
                        id_customer: int,
                        name_object: str,
                        number_lab: str,
                        first_name_and_last_name: str,
                        user_group: str):
        self.cursor.execute(
            'INSERT INTO public.order_info_it('
            'id_order, id_customer, name_object, number_lab, first_name_and_last_name, user_group'
            ') '
            f'VALUES ('
            f'{id_order}, '
            f'{id_customer}, '
            f'\'{name_object}\', '
            f'\'{number_lab}\', '
            f'\'{first_name_and_last_name}\', '
            f'\'{user_group}\''
            f');'
        )

    def create_order_math(self, id_order, id_customer, name_object, number_idz, user_group, number_in_list):
        self.cursor.execute(
            f'INSERT INTO public.order_info_hight_math('
            f'id_order, id_customer, name_object, '
            f'number_idz, user_group, number_in_list) '
            f'VALUES ('
            f'{id_order}, '
            f'{id_customer}, '
            f'\'{name_object}\', '
            f'\'{number_idz}\', '
            f'\'{user_group}\', '
            f'\'{number_in_list}\''
            f');'
        )

    def create_order_programming(self, id_order, id_customer, name_object, number_lab, variant_lab, tasks, zvit):
        self.cursor.execute(
            f'INSERT INTO public.order_info_programming('
            f'id_order, id_customer, name_object, '
            f'number_lab, variant_lab, tasks, zvit) '
            f'VALUES ('
            f'{id_order}, '
            f'{id_customer}, '
            f'\'{name_object}\', '
            f'\'{number_lab}\', '
            f'{variant_lab}, '
            f'\'{tasks}\', '
            f'\'{zvit}\''
            f');'
        )
