# encoding=utf8
import time

import schedule
from firebase_admin.db import reference

from FacebookAPI import send_message, MEAL_TIMES_ONCE_DAY, MEAL_FIREBASE_KEY, MEAL_TIMES_TWO_DAY, MEAL_TIMES_THREE_DAY
from config import get_page_access_token
from firebase_util import default_app


def one_time_day_meal_job():
    users = reference('bot_users', default_app).order_by_child(MEAL_FIREBASE_KEY).equal_to(MEAL_TIMES_ONCE_DAY).get()
    for u_fb_id in users:
        send_message(get_page_access_token(), u_fb_id, 'ماذا اكلت اليوم')


def two_times_day_meal_job():
    users = reference('bot_users', default_app).order_by_child(MEAL_FIREBASE_KEY).equal_to(MEAL_TIMES_TWO_DAY).get()
    for u_fb_id in users:
        send_message(get_page_access_token(), u_fb_id, 'ماذا اكلت اليوم')


def three_times_day_meal_job():
    users = reference('bot_users', default_app).order_by_child(MEAL_FIREBASE_KEY).equal_to(MEAL_TIMES_THREE_DAY).get()
    for u_fb_id in users:
        send_message(get_page_access_token(), u_fb_id, 'ماذا اكلت اليوم')


schedule.every().day.at("1:47").do(one_time_day_meal_job)
schedule.every(12).hours.do(two_times_day_meal_job)
schedule.every(8).hours.do(three_times_day_meal_job)

# schedule.every(8).hours.do(job)
# schedule.every(1).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
