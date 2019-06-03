import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime as dt
import time
import json
from peewee import *

db = SqliteDatabase("USERS.db")


class INFO(Model):
    ID = IntegerField()
    FNAME = TextField()
    SNAME = TextField()
    ST = IntegerField()

    class Meta:
        database = db


KEYBOARD_START = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Урок",
            },
            "color": "negative"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Расписание"
                },
                "color": "positive"
            },

            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"3\"}",
                    "label": "Комманды",
                },
                "color": "default"
            }
        ],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"4\"}",
                "label": "Default",
            },
            "color": "primary"
        }]
    ]
}


def get_info(user_id):
    return vk.method("users.get", {"user_ids": user_id})


def add_in_table(id, first_name, second_name):
    st = True
    for usr_id in INFO.select():
        if usr_id.ID == id:
            st = False
            break
    if st:
        INFO.create(ID=id, FNAME=first_name, SNAME=second_name,
                    ST=0)


def check_status(id):
    rez = False
    for status in INFO.select():
        if status.STATUS == 0 and status.ID == id:
            rez = True
    if rez:
        return "+"


def write_msg(user_id, message):
    vk.method("messages.send", {"user_id": user_id, "message": message,
                                "random_id": 0})


def send_schedule(user_id):
    filename = "schedule.txt"
    message = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            message += "    " + line
    write_msg(user_id, message)


token = "0d32f1db60514159733d06bddc33fac80a6636d535994801ac8c9d45cf361f66e8a8caa9180889b8e02f9"

vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
            user_info = get_info(event.user_id)
            add_in_table(event.user_id, user_info[0]["first_name"],
                         user_info[0]["last_name"])
            hi = check_status(event.user_id)
            if hi == "+":
                write_msg(event.user_id, "Привет " + user_info[0]["first_name"])

            if event.text.lower() == "расписание":
                send_schedule(event.user_id)
            if event.text.lower() == "урок":
                if dt.datetime.today().isoweekday() in (6, 7):
                    write_msg(event.user_id, "Сегодня уроков нет :)")
                # Высчитывание кол-ва минут до начала/конца урока
                else:
                    time_local = time.localtime()
                    minutes = (60 * time_local.tm_hour) + time_local.tm_min
                    if minutes < 510:
                        write_msg(event.user_id,
                                  "До начала первого урока(мин.): " +
                                  str(510 - minutes))
                    elif 510 < minutes < 550:
                        write_msg(event.user_id,
                                  "До конца первого урока(мин.): " +
                                  str(550 - minutes))
                    elif 550 < minutes < 560:
                        write_msg(event.user_id,
                                  "До начала второго урока(мин.): " +
                                  str(560 - minutes))
                    elif 560 < minutes < 600:
                        write_msg(event.user_id,
                                  "До конца второго урока(мин.): " +
                                  str(600 - minutes))
                    elif 600 < minutes < 615:
                        write_msg(event.user_id,
                                  "До начала третьего урока(мин.): " +
                                  str(615 - minutes))
                    elif 615 < minutes < 655:
                        write_msg(event.user_id,
                                  "До конца третьего урока(мин.): " +
                                  str(655 - minutes))
                    elif 655 < minutes < 670:
                        write_msg(event.user_id,
                                  "До начала четвертого урока(мин.): " +
                                  str(670 - minutes))
                    elif 670 < minutes < 710:
                        write_msg(event.user_id,
                                  "До конца четвертого урока(мин.): " +
                                  str(710 - minutes))
                    elif 710 < minutes < 725:
                        write_msg(event.user_id,
                                  "До начала пятого урока(мин.): " +
                                  str(725 - minutes))
                    elif 725 < minutes < 765:
                        write_msg(event.user_id,
                                  "До конца пятого урока(мин.): " +
                                  str(765 - minutes))
                    elif 765 < minutes < 775:
                        write_msg(event.user_id,
                                  "До начала шестого урока(мин.): " +
                                  str(775 - minutes))
                    elif 775 < minutes < 815:
                        write_msg(event.user_id,
                                  "До конца шестого урока(мин.): " +
                                  str(815 - minutes))
                    elif 815 < minutes < 825:
                        write_msg(event.user_id,
                                  "До начала седьмого урока(мин.): " +
                                  str(825 - minutes))
                    elif 825 < minutes < 865:
                        write_msg(event.user_id,
                                  "До конца седьмого урока(мин.): " +
                                  str(865 - minutes))
                    else:
                        write_msg(event.user_id, "Уроки закончились.")
