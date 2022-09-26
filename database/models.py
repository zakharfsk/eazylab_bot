import os

from peewee import *

db = MySQLDatabase(
    os.getenv('DATABASE_DB'),
    user=os.getenv('USER_DB'),
    password=os.getenv('PASSWORD_DB'),
    host=os.getenv('HOST_DB'),
    port=3306
)


class BaseModelOrder(Model):
    id_order = IntegerField()
    id_customer = IntegerField()
    name_object = CharField()


class Users(Model):
    user_id = BigIntegerField()
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    username = CharField()

    class Meta:
        database = db


class OrderProgramming(BaseModelOrder):
    number_lab = CharField()
    tasks = CharField()
    variant_lab = CharField()
    zvit = CharField()

    class Meta:
        database = db


class OrderHigherMath(BaseModelOrder):
    number_idz = CharField()
    number_in_list = CharField()
    user_group = CharField()

    class Meta:
        database = db


class OrderIt(BaseModelOrder):
    number_lab = CharField()
    first_name_and_last_name = CharField()
    user_group = CharField()

    class Meta:
        database = db


class OrderEnglish(BaseModelOrder):
    file_id = CharField()
    task = CharField()
    user_group = CharField()

    class Meta:
        database = db


__all__ = [Users, OrderProgramming, OrderHigherMath, OrderIt, OrderEnglish]
