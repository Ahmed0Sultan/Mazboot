# encoding=utf8
import time

import schedule
from firebase_admin.db import reference

from FacebookAPI import *
from config import get_page_access_token
from firebase_util import default_app, update_record

###### MEALS ######

MEAL_MSG_KEY = 'meal'


def one_time_day_meal_job():
    users = reference('bot_users', default_app).order_by_child(MEAL_FIREBASE_KEY).equal_to(MEAL_TIMES_ONCE_DAY).get()
    for u_fb_id in users:
        send_message(get_page_access_token(), u_fb_id, 'ماذا اكلت اليوم')
        update_record('bot_users', u_fb_id, {'last_msg': MEAL_MSG_KEY})


def two_times_day_meal_job(meal=''):
    users = reference('bot_users', default_app).order_by_child(MEAL_FIREBASE_KEY).equal_to(MEAL_TIMES_TWO_DAY).get()
    for u_fb_id in users:
        send_message(get_page_access_token(), u_fb_id, 'ماذا اكلت اليوم' + meal)
        update_record('bot_users', u_fb_id, {'last_msg': MEAL_MSG_KEY})


def three_times_day_meal_job(meal=''):
    users = reference('bot_users', default_app).order_by_child(MEAL_FIREBASE_KEY).equal_to(MEAL_TIMES_THREE_DAY).get()
    for u_fb_id in users:
        send_message(get_page_access_token(), u_fb_id, 'ماذا اكلت اليوم' + meal)
        update_record('bot_users', u_fb_id, {'last_msg': MEAL_MSG_KEY})


schedule.every().day.at("10:45").do(one_time_day_meal_job)

schedule.every().day.at("13:00").do(two_times_day_meal_job, ' فى الغداء ')
schedule.every().day.at("22:00").do(two_times_day_meal_job, ' فى العشاء ')

schedule.every().day.at("10:00").do(three_times_day_meal_job, ' فى الافطار ')
schedule.every().day.at("15:00").do(three_times_day_meal_job, ' فى الغداء ')
schedule.every().day.at("22:00").do(three_times_day_meal_job, ' فى العشاء ')

###### SUGAR #######

SUGAR_MSG_KEY = 'sugar'


def sugar_job(value):
    users = reference('bot_users', default_app).order_by_child(SUGAR_FIREBASE_KEY).equal_to(value).get()
    for u_fb_id in users:
        send_message(get_page_access_token(), u_fb_id, 'رجاء ادخال قياس السكر')
        update_record('bot_users', u_fb_id, {'last_msg': SUGAR_MSG_KEY})


#### day
schedule.every().day.at("15:00").do(sugar_job, SUGAR_TIMES_ONCE_DAY)

schedule.every().day.at("3:30").do(sugar_job, SUGAR_TIMES_TWO_DAY)
schedule.every().day.at("3:31").do(sugar_job, SUGAR_TIMES_TWO_DAY)

schedule.every().day.at("11:00").do(sugar_job, SUGAR_TIMES_THREE_DAY)
schedule.every().day.at("16:00").do(sugar_job, SUGAR_TIMES_THREE_DAY)
schedule.every().day.at("23:00").do(sugar_job, SUGAR_TIMES_THREE_DAY)

#### week

schedule.every().tuesday.at("16:00").do(sugar_job, SUGAR_TIMES_ONCE_WEEK)

schedule.every().monday.at("16:00").do(sugar_job, SUGAR_TIMES_TWO_WEEK)
schedule.every().thursday.at("16:00").do(sugar_job, SUGAR_TIMES_TWO_WEEK)

schedule.every().saturday.at("16:00").do(sugar_job, SUGAR_TIMES_THREE_WEEK)
schedule.every().thursday.at("16:00").do(sugar_job, SUGAR_TIMES_THREE_WEEK)
schedule.every().friday.at("16:00").do(sugar_job, SUGAR_TIMES_THREE_WEEK)

#### month


schedule.every(30).days.at("16:00").do(sugar_job, SUGAR_TIMES_ONCE_MONTH)
schedule.every(15).days.at("16:00").do(sugar_job, SUGAR_TIMES_TWO_MONTH)
schedule.every(10).days.at("16:00").do(sugar_job, SUGAR_TIMES_THREE_MONTH)

# schedule.every(8).hours.do(job)
# schedule.every(1).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
