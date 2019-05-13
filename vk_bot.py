import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime as dt
import time

filename = "ID_Users.txt"


def add_id(user_id):
    status = 1
    with open(filename, "r+") as f:
        for x in f.readlines():
            if x.strip() in str(user_id):
                status = 0
                break
        if status == 1:
            f.write(str(user_id))


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,
                                'random_id': 0})


def send_schedule(user_id):
    filename = "schedule.txt"
    message = ''
    with open(filename, "r") as f:
        for line in f.readlines():
            message += "    "+line
    write_msg(user_id, message)

token = "0d32f1db60514159733d06bddc33fac80a6636d535994801ac8c9d45cf361f66e8a8caa9180889b8e02f9"

vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
            add_id(str(event.user_id))
            if event.text.lower() == "расписание":
                send_schedule(event.user_id)
            if event.text.lower() == "урок":
                if dt.datetime.today().isoweekday() in (6, 7):
                    write_msg(event.user_id, "Сегодня уроков нет :)")
                else:
                    time_local = time.localtime()
                    minutes = (60*time_local.tm_hour) + time_local.tm_min
                    if minutes < 510:
                        write_msg(event.user_id,
                                  "До начала первого урока(мин.) :" +
                                  str(510-minutes))
                    elif 510 < minutes < 550:
                        write_msg(event.user_id,
                                  "До конца первого урока(мин.) :" +
                                  str(550-minutes))
                    elif 550 < minutes < 560:
                        write_msg(event.user_id,
                                  "До начала второго урока(мин.) :" +
                                  str(560-minutes))
                    elif 560 < minutes < 600:
                        write_msg(event.user_id,
                                  "До конца второго урока(мин.) :" +
                                  str(600-minutes))
                    elif 600 < minutes < 615:
                        write_msg(event.user_id,
                                  "До начала третьего урока(мин.) :" +
                                  str(615-minutes))
                    elif 615 < minutes < 655:
                        write_msg(event.user_id,
                                  "До конца третьего урока(мин.) :" +
                                  str(655-minutes))
                    elif 500:
                        pass