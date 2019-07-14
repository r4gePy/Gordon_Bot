import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime as dt
import time
import json
from classes_for_tables import *
from keyboards import KEYBOARD_START

usr_m = "Для общения с ботом используй цветные блоки(клавиатуру):\n " \
        "'Урок' - ответом бота будет количество минут, оставшееся до конца " \
        "или начала урока\n" \
        "'Расписание' - ты получишь расписание уроков на всю неделю\n" \
        "'Узнать ДЗ' - узнаешь домашнее задание на любой день"

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

token = "0d32f1db60514159733d06bddc33fac80a6636d5359" \
        "94801ac8c9d45cf361f66e8a8caa9180889b8e02f9"

vk = vk_api.VkApi(token = token)

longpoll = VkLongPoll(vk)


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


<<<<<<< HEAD
def add_homework(number_of_day, homework, numb_of_lesson = 1):
    if number_of_day == 1:
        lesson = dict_monday.get(numb_of_lesson)
        for lsn in MONDAY.select():
            if lsn.Lesson == lesson:
                lsn.HW = homework
                lsn.save()
=======
token = "[your_token]"
>>>>>>> 512a961b225da4d17b71293ab8d1bc81aa586838


def show_homework(day):
    lesson = dict_tables.get(day)
    schedule = ''
    for hw in lesson.select():
        schedule += f"{hw.Lesson} - {hw.HW}\n"
    write_msg(event.user_id, schedule)


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
            if event.text.lower() == "узнать дз":
                write_msg(event.user_id, f"На какой день ты хочешь узнать ДЗ?")
                send_weekdays(st = "show")
                for event_show_hw in longpoll.listen():
                    if event_show_hw.type == VkEventType.MESSAGE_NEW and not \
                            event_show_hw.from_me:
                        show_homework(int(event_show_hw.text))
                        break
            if (event.user_id == 194674349 or event.user_id == 213696138 or
                event.user_id == 214280089) \
                    and event.text.lower() == "дз+":
                counter = 1
                numb_day = ""
                numb_lesson = 1
                send_weekdays()
                for dz_msg in longpoll.listen():
                    if dz_msg.type == VkEventType.MESSAGE_NEW and \
                            not dz_msg.from_me:
                        if counter == 1 and len(dz_msg.text) == 1:
                            numb_day = int(dz_msg.text)
                            send_current_lsn(numb_day)
                            print(f"first if {dz_msg.text}")
                        elif counter == 2 and len(dz_msg.text) == 1:
                            print(f"second if {dz_msg.text}")
                            numb_lesson = dz_msg.text
                            write_msg(dz_msg.user_id, f"Следующее сообщение "
                                                      f"будет записано как дз:")
                        elif counter == 3:
                            print(f"third if {dz_msg.text}")
                            add_homework(number_of_day = numb_day,
                                         homework = dz_msg.text,
                                         numb_of_lesson = int(numb_lesson))
                            write_msg(event.user_id, "Домашнее задание успешно "
                                                     "добавлено.")
                            break
                        else:   
                            break
                        counter += 1
