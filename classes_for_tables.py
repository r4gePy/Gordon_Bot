from peewee import *

db = SqliteDatabase("USERS.db")
db_hw = SqliteDatabase("HOMEWORK.db")


class MONDAY(Model):
    Lesson = TextField()
    HW = TextField()

    class Meta:
        database = db_hw


class INFO(Model):
    ID = IntegerField()
    FNAME = TextField()
    SNAME = TextField()
    ST = IntegerField()

    class Meta:
        database = db

