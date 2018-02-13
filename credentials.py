import requests
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication



firebase_site = 'https://bball2018-9c679.firebaseio.com/'
firebase_db = firebase.FirebaseApplication(firebase_site, authentication=None)
conn = http.client.HTTPSConnection("api.sportradar.us")


def get_firebasedb():
    return firebase_db


def get_firebase_site():
    return firebase_site

def get_conn():
    return conn
