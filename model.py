import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication
from nba_functions import *
from credentials import *


#Run sportsradar to gamelist
#Run game_summary to gamelog
#Run defense stats

#Run model

#firebase_db = get_firebasedb();

#firebase_db = firebase.FirebaseApplication('https://bball2018-9c679.firebaseio.com/', authentication=None)


#stats= get_player_stat_list("points", '583ec5fd-fb46-11e1-82cb-f4ce4684ea4c', "036f914a-aad0-4ff1-9771-54f9e963d1b8")
#print stats

def get_trainedNo():
    return 736;

#652 Start of 1/17
#686-694 are the games for 1/22
#690 Suns Bucks 1/22
#700 Suns Pacers 1/24
#730 Suns Rockets 1/28
#750 Warriors Jazz 1/30
#695- 695+57 games was ran and on sublime

start = 500
howmany = 1


firebase_db = get_firebasedb()

#Trained until 736
for i in range(0,howmany):
#for i in range(0,1):
    gameNo = start + i
    [away_team_id, home_team_id,away_team_name, home_team_name] = get_team_ids(gameNo)

#print away_team_id
#print home_team_id
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "------------- "+ away_team_name + " @ " + home_team_name + "-----"


    [h_score,a_score] = run_game(1,away_team_id, home_team_id,away_team_name, home_team_name,gameNo)

    post = True

    post_data = {}
    post_data["homeid"] = home_team_id
    post_data["awayid"] = away_team_id
    post_data["homename"] = home_team_name
    post_data["awayname"] = away_team_name
    post_data["homescore"] = h_score
    post_data["awayscore"] = a_score


    if post:
        post_string = "/Output/"+str(gameNo)
        print post_string
        print post_data
        #result = firebase_db.post(post_string,post_data)

    
#post_string = '/Teams/'+home_team_id+'/'+player["id"]+'/Game'+str(gameNo)
#result = firebase_db.post(post_string,player["statistics"])















#returns player stats in dictionary {player:[stats]}

##    get_string = "/Names/Players/"+shooter
##    
##    result = firebase_db.get(get_string,None)
##    data_str = json.dumps(result)
##    player_outer = json.loads(data_str)
##    if player_outer is None:
##        shooter_name = shooter
##    else:
##        shooter_name = player_outer[player_outer.keys()[0]]
##    
##    #print "Shooter is: "+str(shooter)
##
