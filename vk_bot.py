import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id':user_id, 'message':message,
                               'random_id':0})

token = "..."

vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print("Text message: " + str(event.text))
            response = event.text.lower()
            if event.from_user and not event.from_me:
                user_id = event.user_id
                write_msg(user_id, 'Твой ID: ' + str(user_id))
