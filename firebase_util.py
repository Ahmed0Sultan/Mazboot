import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin.auth import get_user
from firebase_admin.db import reference

from config import get_firebase_url

cred = credentials.Certificate(os.path.dirname(__file__) + '/firebase_secret.json')
default_app = firebase_admin.initialize_app(cred, {'databaseURL': get_firebase_url()})


def add_new_record(node, value):
    return reference(node).push(value)


# new_record_reference = add_new_record('test', {'name': 'mohamed'})
# print new_record_reference.key

def get_record(node, key):
    return reference(node).child(key).get()


# print get_record('test', '-KwESxac5YUeZQ53Yu19')

def update_record(node, key, value):
    return reference(node).child(key).update(value)


# print update_record('test', '-KwEoSnmM9pY35WnBRbP', {'key': [1, 2, 3]})


def delete_node(node):
    return reference(node).delete()  # return None


# print delete_node(reference('test').child('-KwEoSnmM9pY35WnBRbP').child('name').path)
# print delete_node('test')


def delete_record(node, key):
    return reference(node).child(key).delete()  # return None


# print delete_record('test', '-KwESxac5YUeZQ53Yu19cc')

# this function uses firebase auth not users node
def get_user_details(uid):
    return get_user(uid, default_app)


def set_record_value(node, value):
    return reference(node).set(value)

# print get_user_details('pHWdFQSjJ0PXtbtBvbpvown2UmF3').email
