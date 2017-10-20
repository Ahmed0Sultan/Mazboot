# encoding=utf8
import json

import requests

from config import *


def get_user_fb(token, user_id):
    r = requests.get("https://graph.facebook.com/v2.6/" + user_id,
                     params={"fields": "first_name,last_name,profile_pic,locale,timezone,gender"
                         , "access_token": token
                             })
    if r.status_code != requests.codes.ok:
        print r.text
        return
    user = json.loads(r.content)
    return user


def show_typing(token, user_id, action='typing_on'):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "sender_action": action
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_message(token, user_id, text):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "message": {"text": text.decode('utf-8')}
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_picture(token, user_id, imageUrl, title="", subtitle=""):
    if title != "":
        data = {"recipient": {"id": user_id},
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": [{
                                "title": title,
                                "subtitle": subtitle,
                                "image_url": imageUrl
                            }]
                        }
                    }
                }
                }
    else:
        data = {"recipient": {"id": user_id},
                "message": {
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": imageUrl
                        }
                    }
                }
                }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps(data),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_url(token, user_id, text, title, url):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "message": {
                              "attachment": {
                                  "type": "template",
                                  "payload": {
                                      "template_type": "button",
                                      "text": text,
                                      "buttons": [
                                          {
                                              "type": "web_url",
                                              "url": url,
                                              "title": title
                                          }
                                      ]
                                  }
                              }
                          }
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def set_menu(token):
    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile",
                      params={"access_token": token},
                      data=json.dumps({
                          "persistent_menu": [
                              {

                                  "locale": "default",
                                  "composer_input_disabled": False,
                                  "call_to_actions": [
                                      {
                                          "type": "postback",
                                          "title": "اسالنى",
                                          "payload": MENUE_QUESTION
                                      },
                                      {
                                          "type": "postback",
                                          "title": "ابلاغ قياس السكر",
                                          "payload": MENUE_SUGAR
                                      },
                                      {
                                          "type": "postback",
                                          "title": "ابلاغ الوجبات اليوميه",
                                          "payload": MENUE_MEAL
                                      }
                                  ]
                              }
                          ]

                      }),
                      headers={'Content-type': 'application/json'})
    print r.content
    if r.status_code != requests.codes.ok:
        print r.text


def set_greeting_text(token):
    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile",
                      params={"access_token": token},
                      data=json.dumps({
                          "greeting": [
                              {
                                  "locale": "default",
                                  "text": "مرحبا بك فى مساعدك الطبى"
                              }
                          ]
                      }),
                      headers={'Content-type': 'application/json'})
    print r.content
    if r.status_code != requests.codes.ok:
        print r.text


def set_get_started_button(token):
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings",
                      params={"access_token": token},
                      data=json.dumps({
                          "setting_type": "call_to_actions",
                          "thread_state": "new_thread",
                          "call_to_actions": [
                              {
                                  "payload": "Get_Started_Button"
                              }
                          ]
                      }),
                      headers={'Content-type': 'application/json'})
    print r.content
    if r.status_code != requests.codes.ok:
        print r.text

        # set_menu()
        # set_get_started_button()


def send_account_status_quick_replies(token, user_id):
    quickRepliesOptions = [
        {"content_type": "text",
         "title": u"نعم",
         "payload": ACCOUNT_STATUS_KEY + '1'
         },
        {"content_type": "text",
         "title": u"لا",
         "payload": ACCOUNT_STATUS_KEY + '0'
         }
    ]

    data = json.dumps({
        "recipient": {"id": user_id},
        "message": {
            "text": "هل لديك حساب على تطبيق مظبوط",
            "quick_replies": quickRepliesOptions
        }
    })
    data = data.encode('utf-8')
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=data,
                      headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        print r.text


def send_meal_quick_replies(token, user_id):
    key = '_MEAL'

    quickRepliesOptions = [
        {
            "content_type": "text",
            "title": u"العشاء",
            "payload": 'DINNER' + key
        },
        {
            "content_type": "text",
            "title": u"الغداء",
            "payload": 'LUNCH' + key
        },
        {
            "content_type": "text",
            "title": u"الافطار",
            "payload": 'BREAKFAST' + key
        }
    ]

    data = json.dumps({
        "recipient": {"id": user_id},
        "message": {
            "text": "من فضلك اختر الوجبة",
            "quick_replies": quickRepliesOptions
        }
    })
    data = data.encode('utf-8')
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=data,
                      headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        print r.text


def send_meal_times_quick_replies(token, user_id):
    quickRepliesOptions = [
        {
            "content_type": "text",
            "title": u"لا تسال ",
            "payload": MEAL_TIMES_NONE + MEAL_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u"مرة واحدة ",
            "payload": MEAL_TIMES_ONCE_DAY + MEAL_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u"مرتين",
            "payload": MEAL_TIMES_TWO_DAY + MEAL_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u"ثلاث مرات",
            "payload": MEAL_TIMES_THREE_DAY + MEAL_TIMES_KEY
        }
    ]

    data = json.dumps({
        "recipient": {"id": user_id},
        "message": {
            "text": "من فضلك اختر عدد مرات السوال اليوميه عن الطعام :)",
            "quick_replies": quickRepliesOptions
        }
    })
    data = data.encode('utf-8')
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=data,
                      headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        print r.text


def send_sugar_times_quick_replies(token, user_id):
    quickRepliesOptions = [
        {
            "content_type": "text",
            "title": u"لا تسال ",
            "payload": SUGAR_TIMES_NONE + SUGAR_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u" مرة واحدة باليوم ",
            "payload": SUGAR_TIMES_ONCE_DAY + SUGAR_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u"مرتين باليوم",
            "payload": SUGAR_TIMES_TWO_DAY + SUGAR_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u" ثلاث مرات باليوم",
            "payload": SUGAR_TIMES_THREE_DAY + SUGAR_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u" مرة واحدة بالاسبوع ",
            "payload": SUGAR_TIMES_ONCE_WEEK + SUGAR_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u"مرتين بالاسبوع",
            "payload": SUGAR_TIMES_TWO_WEEK + SUGAR_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u" ثلاث مرات بالاسبوع",
            "payload": SUGAR_TIMES_THREE_WEEK + SUGAR_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u" مرة واحدة بالشهر ",
            "payload": SUGAR_TIMES_ONCE_MONTH + SUGAR_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u"مرتين بالشهر",
            "payload": SUGAR_TIMES_TWO_MONTH + SUGAR_TIMES_KEY
        },
        {
            "content_type": "text",
            "title": u" ثلاث مرات بالشهر",
            "payload": SUGAR_TIMES_THREE_MONTH + SUGAR_TIMES_KEY
        }

    ]

    data = json.dumps({
        "recipient": {"id": user_id},
        "message": {
            "text": "من فضلك اختر عدد مرات السوال عن قياس السكر :)",
            "quick_replies": quickRepliesOptions
        }
    })
    data = data.encode('utf-8')
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=data,
                      headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        print r.text

# set_menu(token)
# set_greeting_text(token)
# send_meal_times_quick_replies(get_page_access_token(), '1558695490860776')
