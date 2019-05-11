import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime as dt
filename = "ID_Users.txt"


def add_id(user_id):
    status = True
    with open(filename, "r+") as f:
        for x in f.readlines():
            if x.strip() in str(user_id):
                status = False
                break
        if status:
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
