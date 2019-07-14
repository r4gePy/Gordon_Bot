from vk_bot import vk, event
from keyboards import KEYBOARD_START
import json
from classes_for_tables import *

dict_days = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница"
}
dict_tables = {
    1: MONDAY,
    2: TUESDAY,
    3: WEDNESDAY,
    4: THURSDAY,
    5: FRIDAY
}


def send_weekdays(st = 'add'):
    msg_schedule = ""
    for numb, day in dict_days.items():
        msg_schedule += f'{str(numb)}. {day}\n'
    if st == "add":
        write_msg(event.user_id,
                  f"На какой день будет дано дз?\n{msg_schedule}")
    else:
        write_msg(event.user_id,
                  msg_schedule)


def send_current_lsn(numb_of_day):
    msg_lsns = ""
    if numb_of_day == 1:
        for lsn in MONDAY.select():
            msg_lsns += str(lsn.id) + '. ' + lsn.Lesson + '\n'
    write_msg(event.user_id, msg_lsns)


def get_info(user_id):
    return vk.method("users.get", {"user_ids": user_id})


def add_in_table(id_for_info):
    st = True
    for usr_id in INFO.select():
        if usr_id.ID_VK == id_for_info:
            st = False
            break
    if st:
        INFO.create(ID_VK = id_for_info,
                    F_NAME = user_info[0]["first_name"],
                    S_NAME = user_info[0]["last_name"],
                    )


def write_msg(user_id, message):
    vk.method("messages.send",
              {"user_id": user_id,
               "message": message,
               "random_id": 0,
               "keyboard": json.dumps(KEYBOARD_START,
                                      ensure_ascii = False)})


def send_schedule(user_id):
    filename = "schedule.txt"
    message = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            message += "    " + line
    write_msg(user_id, message)


def add_homework(number_of_day, homework, numb_of_lesson = 1):
    if number_of_day == 1:
        lesson = dict_monday.get(numb_of_lesson)
        for lsn in MONDAY.select():
            if lsn.Lesson == lesson:
                lsn.HW = homework
                lsn.save()


def show_homework(day):
    lesson = dict_tables.get(day)
    schedule = ''
    for hw in lesson.select():
        schedule += f"{hw.Lesson} - {hw.HW}\n"
    write_msg(event.user_id, schedule)