import requests
import math
import http.client
import json
from firebase import firebase,FirebaseAuthentication
from nba_functions import *


firebase_db = firebase.FirebaseApplication('https://bball2018-9c679.firebaseio.com/', authentication=None)

#result = firebase_db.post('/Output/',None)

away_name_list = []
home_name_list = []
away_points_list = []
home_points_list = []

#start = 610
#end = 660
start = 523
end = 524
for x in range(start,end):
    [away_team_id, home_team_id,away_team_name, home_team_name,away_points,home_points]= get_team_ids(x)

    away_name_list.append(away_team_name)
    home_name_list.append(home_team_name)
    away_points_list.append(away_points)
    home_points_list.append(home_points)

    print x





for i in range(start,end):
    game_data = {}
    index = i - start

    away_team_name = away_name_list[index]
    home_team_name = home_name_list[index]
    away_points = away_points_list[index]
    home_points = home_points_list[index]

    
    real_total = away_points + home_points

    print str(i)+ " " +away_team_name +" @ " + home_team_name
    line = raw_input("Line: a-h  ")
    total = raw_input("Total: ")

    game_data["line"] = line
    game_data["total"] = total
    game_data["real_line"] = away_points - home_points
    game_data["real_total"]= away_points + home_points


    post_string = '/Output/'+'/Game'+str(i)+'/'


    result = firebase_db.post(post_string,game_data)
