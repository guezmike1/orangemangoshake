import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication



firebase_db = firebase.FirebaseApplication('https://nbasort.firebaseio.com/', authentication=None)

result = firebase_db.delete("/Names",None)


for gameNo in range(0,40):
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
    away_team_name = away_team_data["name"]
    home_team_name = home_team_data["name"]


    away_team_players = away_team_data["players"]
    home_team_players = home_team_data["players"]


    team_post_string = '/Names/Teams/'+away_team_id
    result = firebase_db.post(team_post_string,away_team_name)

    team_post_string = '/Names/Teams/'+home_team_id
    result = firebase_db.post(team_post_string,home_team_name)

    for player in home_team_players:
        post_string = '/Names/Players/'+player["id"]

        #print post_string
        result = firebase_db.post(post_string, player["full_name"])
        #print post_string + " ---- " + player["full_name"]
        #pprint(player["statistics"])

    for player in away_team_players:
        post_string = '/Names/Players/'+player["id"]

        #print post_string
        result = firebase_db.post(post_string,player["full_name"])
        







    




