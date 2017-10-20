# coding=utf8
import json
import sys
import traceback
from time import time

import time
from firebase_admin.db import reference
from flask_login import LoginManager
from flask_login import logout_user, current_user

import FacebookAPI as FB
from config import *
from firebase_util import update_record, get_record, add_new_record, set_record_value

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, request, render_template, redirect, flash, url_for

app = Flask(__name__)
token = get_page_access_token()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super-secret'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == get_verify_token():
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return render_template('index.html')
    # return "Welcome In Mazboot world", 200


@app.route('/', methods=['POST'])
def handle_messages():
    payload = request.get_data()

    # Handle messages
    for sender_id, message in messaging_events(payload):
        # Start processing valid requests
        try:
            response = processIncoming(sender_id, message)

            if response == 'postback':
                pass


            elif response is not None:
                FB.send_message(token, sender_id, response)

            else:
                FB.send_message(token, sender_id, "Sorry I don't understand that")
        except Exception, e:
            print e
            traceback.print_exc()
    return "ok"


def processIncoming(user_id, message):
    message_text = message['data']
    message_text = message_text.decode('utf-8', 'ignore')

    if message['type'] == 'text':
        last_msg = get_record(reference('bot_users').child(user_id).path, 'last_msg')
        uid = get_record(reference('bot_users').child(user_id).path, 'uid')

        if (last_msg == SUGAR_MSG_KEY):
            return 'sugarrrrrr'
        elif (last_msg == MEAL_MSG_KEY):
            add_new_record(reference('meals').child(uid).path, {
                'meal': message_text,
                'timeInMillisecond': int(round(time.time() * 1000))
            })
            set_record_value(reference('bot_users').child(user_id).child('last_msg').path, '')

            return 'بالهناء والشفاء'

        return message_text

    elif message['type'] == 'postback':
        message_payload = message['payload']
        payload_response = payloadProcessing(user_id, message_payload)
        return payload_response

    elif message['type'] == 'quick_reply':
        quick_reply_payload = message['data']
        quick_reply_response = quickReplyProcessing(user_id, quick_reply_payload)
        return quick_reply_response

    elif message['type'] == 'location':
        response = "I've received location (%s,%s) (y)" % (message['data'][0], message['data'][1])
        return response

    elif message['type'] == 'audio':
        audio_url = message['data']
        return "I've received audio %s" % (audio_url)

    # Unrecognizable incoming, remove context and reset all data to start afresh
    else:
        return "*scratch my head*"


def messaging_events(payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]

    for event in messaging_events:
        sender_id = event["sender"]["id"]

        # Postback Message
        if "postback" in event:
            print event
            yield sender_id, {'type': 'postback', 'payload': event['postback']['payload'],
                              'message_id': event["sender"]["id"]}


        # Pure text message
        elif "message" in event and "text" in event["message"] and "quick_reply" not in event["message"]:
            data = event["message"]["text"].encode('unicode_escape')
            yield sender_id, {'type': 'text', 'data': data, 'message_id': event['message']['mid']}

        # Message with attachment (location, audio, photo, file, etc)
        elif "message" in event and "attachments" in event["message"]:

            # Location
            if "location" == event['message']['attachments'][0]["type"]:
                coordinates = event['message']['attachments'][
                    0]['payload']['coordinates']
                latitude = coordinates['lat']
                longitude = coordinates['long']

                yield sender_id, {'type': 'location', 'data': [latitude, longitude],
                                  'message_id': event['message']['mid']}

            # Audio
            elif "audio" == event['message']['attachments'][0]["type"]:
                audio_url = event['message'][
                    'attachments'][0]['payload']['url']
                yield sender_id, {'type': 'audio', 'data': audio_url, 'message_id': event['message']['mid']}

            else:
                yield sender_id, {'type': 'text', 'data': "I don't understand this",
                                  'message_id': event['message']['mid']}

        # Quick reply message type
        elif "message" in event and "quick_reply" in event["message"]:
            data = event["message"]["quick_reply"]["payload"]
            yield sender_id, {'type': 'quick_reply', 'data': data, 'message_id': event['message']['mid']}

        else:
            yield sender_id, {'type': 'text', 'data': "I don't understand this", 'message_id': event['message']['mid']}


def payloadProcessing(user_id, message_payload):
    if message_payload == 'Get_Started_Button':
        FBuser = FB.get_user_fb(token, user_id)
        msg = u" مرحبا بك يا "
        FB.send_message(token, user_id, FBuser.get('first_name') + msg)
        FB.show_typing(token, user_id, 'typing_on')
        intro = u"تعرف على ما يقدمه مظبوط من القائمه"
        FB.send_message(token, user_id, intro)


    elif message_payload == MENUE_QUESTION:
        FB.show_typing(token, user_id, 'typing_on')
        intro = u"يسعدنى الاجابه على اسئلتك :D تفضل بالسؤال"
        FB.send_message(token, user_id, intro)

    elif message_payload == MENUE_SUGAR:
        FB.show_typing(token, user_id, 'typing_on')
        intro = u"من فضلك ادخل قياس السكر"
        FB.send_message(token, user_id, intro)

    elif message_payload == MENUE_MEAL:
        FB.show_typing(token, user_id, 'typing_on')
        FB.send_meal_quick_replies(token, user_id)

    return 'postback'


def quickReplyProcessing(user_id, quick_reply_payload):
    if SUGAR_TIMES_KEY in quick_reply_payload:
        FB.show_typing(token, user_id, 'typing_on')
        FB.send_message(token, user_id, 'Thanks :)')
        payload_id = quick_reply_payload.replace(SUGAR_TIMES_KEY, '')
        # add_new_record('bot_users', {user_id: {'sugar_times': payload_id}})
        update_record('bot_users', user_id,
                      {SUGAR_FIREBASE_KEY: payload_id})  # use of update to be able to insert custom ids

    elif MEAL_TIMES_KEY in quick_reply_payload:
        FB.show_typing(token, user_id, 'typing_on')
        FB.send_message(token, user_id, 'Thanks :)')
        payload_id = quick_reply_payload.replace(MEAL_TIMES_KEY, '')
        # add_new_record('bot_users', {user_id: {'sugar_times': payload_id}})
        update_record('bot_users', user_id,
                      {MEAL_FIREBASE_KEY: payload_id})  # use of update to be able to insert custom ids

    return 'postback'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('new_question'))
    if request.method == 'GET':
        return render_template('login.html')

    flash('Logged in successfully')
    return redirect(url_for('new_question'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(id):
    return ''


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
