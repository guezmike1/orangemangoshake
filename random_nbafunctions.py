import requests
import math
import http.client
import json
from firebase import firebase,FirebaseAuthentication
from nba_functions import *
import matplotlib.pyplot as plt

plt.plot([1,2,3,4])

plt.plot([4,3,2,1])
plt.show()


##firebase_db = firebase.FirebaseApplication('https://nbasort.firebaseio.com/', authentication=None)
##
##
##delete_string = '/Output/Game500/-Kn_fSIrdnz2pFWOLU4J/-Kna1ldg-ecGGUz3k-w-'
##firebase_db.delete(delete_string,None)
##delete_string = '/Output/Game500/-Kn_fSIrdnz2pFWOLU4J/-Kna29_ksiCRr0OGV76m'
##firebase_db.delete(delete_string,None)
##delete_string = '/Output/Game500/-Kn_fSIrdnz2pFWOLU4J/-Kna2yUJdCvmS0AgHlyf'
##firebase_db.delete(delete_string,None)


##get_string = '/Output/Game'+str(500)+'/'
##result = firebase_db.get(get_string,None)
##data_str = json.dumps(result)
##current_game = json.loads(data_str)
##
##game_key = current_game.keys()[0]
##
##post_string = get_string+game_key
##
##
##
