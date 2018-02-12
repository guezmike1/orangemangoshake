import requests
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication



global firebase_site
firebase_site = 'https://bball2018-9c679.firebaseio.com/'
global firebase_db
firebase_db = firebase.FirebaseApplication('https://bball2018-9c679.firebaseio.com/', authentication=None)
global conn
conn = http.client.HTTPSConnection("api.sportradar.us")
