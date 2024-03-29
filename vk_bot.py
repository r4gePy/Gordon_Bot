import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime as dt
import time
import json
from classes_for_tables import *
from keyboards import *

# "help" message
usr_m = "Для общения с ботом используй цветные блоки(клавиатуру) находящуюся слева от кнопки отправки сообщения"

# Dict with days
dict_days = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница"
}

# Dict with tables
dict_tables = {
    1: MONDAY,
    2: TUESDAY,
    3: WEDNESDAY,
    4: THURSDAY,
    5: FRIDAY
}

# !!!TOKEN!!!!
token = "2ea22b0432d68245816992228cb95135729f1724e2b2b1cd3be8b038cd97d854df7af3a2c9244f18c2493"

# Connecting token with lib
vk = vk_api.VkApi(token=token)

# Connecting poll with vk
longpoll = VkLongPoll(vk)


def send_weekdays(st='add'):

    """ Function for sending schedule """

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

    """ Function for collect and send lesson schedules per day """

    msg_lessons = ""
    day_lsn = dict_tables.get(numb_of_day)
    for day in day_lsn.select():
        msg_lessons += str(day.id) + '. ' + day.Lesson + '\n'
    write_msg(event.user_id, msg_lessons)


def get_info(user_id):

    """ Function, that return user information into a variable  """

    return vk.method("users.get", {"user_ids": user_id})


def add_in_table(id_for_info):

    """  Function, that add user in a data base  """

    st = True
    for usr_id in INFO.select():
        if usr_id.ID_VK == id_for_info:
            st = False
            break
    if st:
        INFO.create(ID_VK=id_for_info,
                    F_NAME=user_info[0]["first_name"],
                    S_NAME=user_info[0]["last_name"],
                    )


def write_msg(user_id, message):

    """  Function, that allows a bot to write messages  """

    vk.method("messages.send",
              {"user_id": user_id,
               "message": message,
               "random_id": 0,
               "keyboard": json.dumps(KEYBOARD_START,
                                      ensure_ascii=False)})


def add_homework(number_of_day, homework_message, numb_of_lesson):

    """  Function for adding homework in data base  """

    day = dict_tables.get(number_of_day)
    for data in day.select():
        if data.id == numb_of_lesson:
            data.HW = homework_message
            data.save()


def show_lessons(day, id_user, status=True):

    """  Function, that send homework  """

    lesson = dict_tables.get(day)
    schedule = ''
    for hw in lesson.select():
        if status:
            schedule += f"{hw.Lesson} - {hw.HW}\n"
        else:
            schedule += f"{hw.id}.{hw.Lesson}\n"
    write_msg(id_user, schedule)


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
            user_info = get_info(event.user_id)
            add_in_table(event.user_id)
            if event.text.lower() in ("привет", "здорова", "ку", "хай", "прив",
                                      "йоу", "начать", "hi"):
                write_msg(event.user_id, f"Здравствуй, {user_info[0]['first_name']}\n {usr_m}")
            # if event.text.lower() == "шпора":
            #    attachments = []
            #    upload_image = upload.photo_messages(photos=image)[0]
            #    attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
            #    send_image(event.user_id, attachments)
            if event.text.lower() == "расписание":
                user_schedule = event.user_id
                write_msg(event.user_id, "На какой день нужно расписание?")
                send_weekdays(st="show")
                for event_send_schedule in longpoll.listen():
                    try:
                        if event_send_schedule.type == VkEventType.MESSAGE_NEW and \
                                event_send_schedule.user_id == user_schedule and \
                                not event_send_schedule.from_me:
                            show_lessons(int(event_send_schedule.text), user_schedule, status=False)
                            break
                    except (AttributeError, ValueError):
                        write_msg(user_schedule.user_id, "Недопустимая цифра")
                        break
            if event.text.lower() == "урок":
                if dt.datetime.today().month in (6, 7, 8):
                    write_msg(event.user_id, "Сейчас лето, отдыхай :D")
                elif dt.datetime.today().isoweekday() in (6, 7):
                    write_msg(event.user_id, "Сегодня выходной :)")

                    """ 
                    Высчитывание кол-во минут    до конца урока 
                    """

                else:
                    time_local = time.localtime()
                    minutes = (60 * time_local.tm_hour) + time_local.tm_min + 180
                    if 360 <= minutes <= 510:
                        write_msg(event.user_id,
                                  "До начала первого урока(мин.): " +
                                  str(510 - minutes))
                    elif 510 <= minutes <= 550:
                        write_msg(event.user_id,
                                  "До конца первого урока(мин.): " +
                                  str(550 - minutes))
                    elif 550 <= minutes <= 560:
                        write_msg(event.user_id,
                                  "До начала второго урока(мин.): " +
                                  str(560 - minutes))
                    elif 560 <= minutes <= 600:
                        write_msg(event.user_id,
                                  "До конца второго урока(мин.): " +
                                  str(600 - minutes))
                    elif 600 <= minutes <= 615:
                        write_msg(event.user_id,
                                  "До начала третьего урока(мин.): " +
                                  str(615 - minutes))
                    elif 615 <= minutes <= 655:
                        write_msg(event.user_id,
                                  "До конца третьего урока(мин.): " +
                                  str(655 - minutes))
                    elif 655 <= minutes <= 670:
                        write_msg(event.user_id,
                                  "До начала четвертого урока(мин.): " +
                                  str(670 - minutes))
                    elif 670 <= minutes <= 710:
                        write_msg(event.user_id,
                                  "До конца четвертого урока(мин.): " +
                                  str(710 - minutes))
                    elif 710 <= minutes <= 725:
                        write_msg(event.user_id,
                                  "До начала пятого урока(мин.): " +
                                  str(725 - minutes))
                    elif 725 <= minutes <= 765:
                        write_msg(event.user_id,
                                  "До конца пятого урока(мин.): " +
                                  str(765 - minutes))
                    elif 765 <= minutes <= 775:
                        write_msg(event.user_id,
                                  "До начала шестого урока(мин.): " +
                                  str(775 - minutes))
                    elif 775 <= minutes <= 815:
                        write_msg(event.user_id,
                                  "До конца шестого урока(мин.): " +
                                  str(815 - minutes))
                    elif 815 <= minutes <= 825:
                        write_msg(event.user_id,
                                  "До начала седьмого урока(мин.): " +
                                  str(825 - minutes))
                    elif 825 <= minutes <= 865:
                        write_msg(event.user_id,
                                  "До конца седьмого урока(мин.): " +
                                  str(865 - minutes))
                    else:
                        write_msg(event.user_id, "Уроки закончились.")
            if event.text.lower() == "узнать дз":
                user_homework = event.user_id
                write_msg(event.user_id, "На какой день ты хочешь узнать ДЗ?")
                send_weekdays(st="show")
                for event_show_hw in longpoll.listen():
                    if event_show_hw.type == VkEventType.MESSAGE_NEW and event_show_hw.user_id == user_homework and \
                            not event_show_hw.from_me:
                        try:
                            show_lessons(int(event_show_hw.text), user_homework)
                            break
                        except (AttributeError, ValueError):
                            write_msg(user_homework, "Я ожидал цифру в диапазоне 1-5")
                            break

            if (event.user_id == 194674349 or event.user_id == 183461346 or event.user_id == 213696138) \
                    and event.text.lower() == "дз+":
                counter = 1
                numb_day = ""
                numb_lesson = 1
                send_weekdays()
                for dz_msg in longpoll.listen():
                    if dz_msg.type == VkEventType.MESSAGE_NEW and \
                            not dz_msg.from_me:
                        try:
                            if counter == 1 and int(dz_msg.text) in range(1, 6):
                                numb_day = int(dz_msg.text)
                                send_current_lsn(numb_day)

                            elif counter == 2 and int(dz_msg.text) in range(1, 8):

                                numb_lesson = dz_msg.text
                                write_msg(dz_msg.user_id, f"Следующее сообщение "
                                                          f"будет записано как дз:")

                            elif counter == 3:

                                add_homework(number_of_day=numb_day,
                                             homework_message=dz_msg.text,
                                             numb_of_lesson=int(numb_lesson))
                                write_msg(event.user_id, "Домашнее задание успешно "
                                                         "добавлено.")
                                break
                            elif len(dz_msg.text) > 1:
                                write_msg(dz_msg.user_id, "Неверный ответ.")
                            counter += 1
                        except (ValueError, AttributeError):
                            write_msg(dz_msg.user_id, "Получен неверный ответ, попробуй снова написать команду")
                            break
