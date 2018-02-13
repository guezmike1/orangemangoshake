import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication
from nba_functions import *
from credentials import *

trainedNo = get_trainedNo()
firebase_db = get_firebasedb()

#Fix 730
start = 796
howmany = 631

get_string = '/Outputv6'
result = firebase_db.get(get_string,None)
data_str = json.dumps(result)
game_list = json.loads(data_str)


#845 done
for i in range(start,846):
    current_game = game_list[i]
    game_data = current_game[current_game.keys()[0]]

    away_team = game_data["awayname"]
    home_team = game_data["homename"]

    print i
    line = input(away_team + " @ " + home_team + ": ")
    game_data["homeline"] = line
    game_data["awayline"] = -1*line

    total = input("total: ")
    game_data["total"] = total

    
    post_string = '/Outputv7/'+str(i)
    #print post_string
    #print game_data
    firebase_db.post(post_string, game_data)






    
                          
        
    
