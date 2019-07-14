import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime as dt
import time
import json
from classes_for_tables import *

usr_m = "Для общения с ботом используй цветные блоки(клавиатуру):\n " \
        "'Урок' - ответом бота будет количество минут, оставшееся до конца " \
        "или начала урока\n" \
        "'Расписание' - ты получишь расписание уроков на всю неделю"

KEYBOARD_START = {
    "one_time": None,
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
        ]

    ]
}

dict_days = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday"
}


def get_info(user_id):
    return vk.method("users.get", {"user_ids": user_id})


def add_in_table(id):
    st = True
    for usr_id in INFO.select():
        if usr_id.ID == id:
            st = False
            break
    if st:
        INFO.create(ID=id,
                    FNAME=user_info[0]["first_name"],
                    SNAME=user_info[0]["last_name"],
                    ST=0)


def write_msg(user_id, message):
    vk.method("messages.send",
              {"user_id": user_id,
               "message": message,
               "random_id": 0,
               "keyboard": json.dumps(KEYBOARD_START,
                                      ensure_ascii=False)})


def send_schedule(user_id):
    filename = "schedule.txt"
    message = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            message += "    " + line
    write_msg(user_id, message)


token = "[your_token]"

vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
            user_info = get_info(event.user_id)
            add_in_table(event.user_id)
            if event.text.lower() in ("привет", "здорова", "ку", "хай", "прив",
                                      "йоу"):
                write_msg(event.user_id, "Здравствуй "
                          + user_info[0]['first_name'])
                write_msg(event.user_id, "Хочешь узнать как пользоваться ботом?"
                                         " Напиши !help")
            if event.text.lower() == "!help":
                write_msg(event.user_id, usr_m)
            if event.text.lower() == "расписание":
                write_msg(event.user_id, "*здесь должно быть расписание, "
                                         "но сейчас лето*")
            if event.text.lower() == "урок":
                if dt.datetime.today().month in (6, 7, 8):
                    write_msg(event.user_id, "Сейчас лето, отдыхай :D")
                elif dt.datetime.today().isoweekday() in (6, 7):
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
            if (event.user_id == 194674349 or event.user_id == 213696138) \
                    and event.text.lower() == "дз+":
                write_msg(event.user_id,
                          "На какой день будет дано дз?")
                msg_schedule = ""
                for numb, day in dict_days.items():
                    msg_schedule += f'{str(numb)}. {day}\n'
                write_msg(event.user_id, msg_schedule)
                for event_dz in longpoll.listen():
                    if event_dz.type == VkEventType.MESSAGE_NEW and \
                            not event_dz.from_me:
                                pass
