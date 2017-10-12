import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin.db import reference

from config import get_firebase_url

cred = credentials.Certificate(os.path.dirname(__file__) + '/firebase_secret.json')
default_app = firebase_admin.initialize_app(cred, {'databaseURL': get_firebase_url()})

dbRef = reference(path='/users', app=default_app)

first1userbymail = dbRef.order_by_child('email').equal_to('madkourt48@gmail.com').limit_to_first(1).get()
first10users = dbRef.order_by_child('email').limit_to_first(10).get()
users = dbRef.child('01bM8zwz7WgxoI2JUcf1Tk9Ypl73')

print first1userbymail
print first10users
print users.get().get('age')
