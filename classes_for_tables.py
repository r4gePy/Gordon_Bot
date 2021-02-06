from peewee import *

db_info = SqliteDatabase("USERS.db")
db_hw = SqliteDatabase("HOMEWORK.db")


class MONDAY(Model):
    Lesson = TextField()
    HW = TextField()

    class Meta:
        database = db_hw


class TUESDAY(Model):
    Lesson = TextField()
    HW = TextField()

    class Meta:
        database = db_hw


class WEDNESDAY(Model):
    Lesson = TextField()
    HW = TextField()

    class Meta:
        database = db_hw


class THURSDAY(Model):
    Lesson = TextField()
    HW = TextField()

    class Meta:
        database = db_hw


class FRIDAY(Model):
    Lesson = TextField()
    HW = TextField()

    class Meta:
        database = db_hw


class INFO(Model):
    ID_VK = IntegerField()
    F_NAME = TextField()
    S_NAME = TextField()

    class Meta:
        database = db_info
