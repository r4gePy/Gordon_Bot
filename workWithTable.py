from peewee import *
from classes_for_tables import *

db_hw = SqliteDatabase("HOMEWORK.db")


class MONDAY(Model):
    Lesson = TextField()
    HW = TextField()

    class Meta:
        database = db_hw

dict_tables = {
    1: MONDAY,
    2: TUESDAY,
    3: WEDNESDAY,
    4: THURSDAY,
    5: FRIDAY
}

def add_homework(number_of_day, homework, numb_of_lesson=1):
    for day in MONDAY.select():
        if day.id == 1:
            day.HW = homework
            day.save()
            break


mhb = "1231"

mhb = dict_tables.get(1)

for mh in mhb.select():
    if mh.id == 1:
        mh.HW = "homework"
        mh.save()
        break

