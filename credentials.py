import requests
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication

trainedNo = 736
firebase_site = 'https://bball2018-9c679.firebaseio.com/'
firebase_db = firebase.FirebaseApplication(firebase_site, authentication=None)
conn = http.client.HTTPSConnection("api.sportradar.us")
api_key = "9ced6hbudhabvug4jdhqsew3"

def get_firebasedb():
    return firebase_db


def get_firebase_site():
    return firebase_site

def get_conn():
    return conn


def get_trainedNo():
    return trainedNo

def get_apikey():
    return api_key
