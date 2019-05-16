import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlite3

token = "0d32f1db60514159733d06bddc33fac80a6636d535994801ac8c9d45cf361f66e8a8caa9180889b8e02f9"

vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)
conn = sqlite3.connect("users_id.db")
cursor = conn.cursor()


sql = "SELECT ID FROM USERS_INFO"
cursor.execute(sql)
ids = cursor.fetchall()
for usr in ids:
    print(usr[0])
