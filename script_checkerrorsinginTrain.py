import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication
from nba_functions import *



firebase_db = firebase.FirebaseApplication('https://bball2018-9c679.firebaseio.com/', authentication=None)


games_tocheck = [44,94,136,246,380,502,573]


for i in range(1,7):
    index = games_tocheck[i]
    
    [away_team_id, home_team_id,away_team_name, home_team_name] = get_team_ids(index)
    print "GameNo: "+str(index)+"------------- "+ away_team_name + " @ " + home_team_name + "-----"

    #post_string = '/Teams/583ec825-fb46-11e1-82cb-f4ce4684ea4c/9484b30a-4e6e-4307-8b42-12fa141dee17'+'/Game'+str(index)+"/-L3_C_g60gDHtDNItfBv/"
    #result = firebase_db.post(post_string,"13456")
    #result = firebase_db.delete(post_string,None)





    get_string = '/Teams/'+away_team_id+"/"

    result = firebase_db.get(get_string,None)
    data_str = json.dumps(result)
    current_team = json.loads(data_str)

    for player in current_team:
        player_data = current_team[player]

        gameString = "Game"+str(index)

        #print "Gamestring: " + gameString
        #print "Keys: " +str(player_data.keys())
        player_outername = player_data["fullname"]
        player_name = player_outername[player_outername.keys()[0]]
        
        if gameString in player_data.keys():
            game_data = player_data[gameString]

            if len(game_data.keys()) > 2:
                delete_game = game_data.keys()[2]
                delete_string = "/Teams/"+away_team_id+"/"+player+'/Game'+str(index)+"/"+delete_game+"/"
                print delete_string
                result = firebase_db.delete(delete_string,None)
                
                #print "Team: "+home_team_name + " " + home_team_id
                #print "Player: "+player_name+" " + player + " keys: "+str(game_data.keys())

            if len(game_data.keys()) > 1:
                delete_game = game_data.keys()[1]
                delete_string = "/Teams/"+away_team_id+"/"+player+'/Game'+str(index)+"/"+delete_game+"/"
                print delete_string
                result = firebase_db.delete(delete_string,None)
                
                #print "Team: "+home_team_name + " " + home_team_id
                #print "Player: "+player_name+" " + player + " keys: "+str(game_data.keys())




    get_string = '/Teams/'+home_team_id+"/"

    result = firebase_db.get(get_string,None)
    data_str = json.dumps(result)
    current_team = json.loads(data_str)

    for player in current_team:
        player_data = current_team[player]

        gameString = "Game"+str(index)

        #print "Gamestring: " + gameString
        #print "Keys: " +str(player_data.keys())
        #player_outername = player_data["fullname"]
        #player_name = player_outername[player_outername.keys()[0]]
        
        if gameString in player_data.keys():
            game_data = player_data[gameString]

            if len(game_data.keys()) > 2:
                delete_game = game_data.keys()[2]
                delete_string = "/Teams/"+home_team_id+"/"+player+'/Game'+str(index)+"/"+delete_game+"/"
                print delete_string
                result = firebase_db.delete(delete_string,None)
                
                #print "Team: "+home_team_name + " " + home_team_id
                #print "Player: "+player_name+" " + player + " keys: "+str(game_data.keys())

            if len(game_data.keys()) > 1:
                delete_game = game_data.keys()[1]
                delete_string = "/Teams/"+home_team_id+"/"+player+'/Game'+str(index)+"/"+delete_game+"/"
                print delete_string
                result = firebase_db.delete(delete_string,None)
                
                #print "Team: "+home_team_name + " " + home_team_id
                #print "Player: "+player_name+" " + player + " keys: "+str(game_data.keys())




