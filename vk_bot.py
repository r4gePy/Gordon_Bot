import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def write_msg(user_id, message):
    vk.method('message.send', {'user_id':user_id, 'message':message,
                               'random_id':0})

token = "5a1c5dd1b0b83ec50812fd33576df54ffcfb916d2386d9771d879b54de9dd126a0a078fc346a023fd98a2"

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
