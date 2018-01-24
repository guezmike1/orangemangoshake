import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication


## Parse games summarys to Teams/ID/playername/Game# -> posts stats of each player per game
firebase_db = firebase.FirebaseApplication('https://bball2018-9c679.firebaseio.com/', authentication=None)
#result = firebase_db.delete("/Teams",None)

#Ran up to 680
for gameNo in range(600,680):
    get_string = '/Games/Game'+str(gameNo)
    print gameNo

    result = firebase_db.get(get_string,None)
    data_str = json.dumps(result)
    current_game = json.loads(data_str)

    ##Fix indexing into problem
    data_game = current_game[current_game.keys()[0]]

    away_team_data = data_game["away"]
    home_team_data = data_game["home"]

    away_team_id = away_team_data["id"]
    home_team_id = home_team_data["id"]


    away_team_players = away_team_data["players"]
    home_team_players = home_team_data["players"]


    for player in home_team_players:
        post_string = '/Teams/'+home_team_id+'/'+player["id"]+'/Game'+str(gameNo)
        result = firebase_db.post(post_string,player["statistics"])


        post_string = '/Teams/'+home_team_id+'/'+player["id"]+'/fullname'
        result = firebase_db.post(post_string,player["full_name"])

        #pprint(player["statistics"])

    for player in away_team_players:
        post_string = '/Teams/'+away_team_id+'/'+player["id"]+'/Game'+str(gameNo)

        #print post_string
        result = firebase_db.post(post_string,player["statistics"])








    




