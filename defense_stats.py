import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication



firebase_db = firebase.FirebaseApplication('https://bball2018-9c679.firebaseio.com/', authentication=None)

away_team_data = {}
home_team_data = {}

#765
for gameNo in range(808,846):
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


    away_team_stats = away_team_data["statistics"]
    home_team_stats = home_team_data["statistics"]


    away_possessions = away_team_stats["field_goals_att"]+away_team_stats["turnovers"]
    home_possessions = home_team_stats["field_goals_att"]+home_team_stats["turnovers"]

    away_poss_ratio = (away_possessions*100)/(away_possessions+home_possessions)
    home_poss_ratio = (home_possessions*100)/(away_possessions+home_possessions)


    away_TO_ratio = (away_team_stats["turnovers"]*100)/away_possessions
    home_TO_ratio = (home_team_stats["turnovers"]*100)/home_possessions

    #how many BS home team for on away shots
    away_BA_ratio = ((away_team_stats["blocked_att"]+away_team_stats["blocks"])*100)/home_team_stats["field_goals_att"]
    home_BA_ratio = ((home_team_stats["blocked_att"]+home_team_stats["blocks"])*100)/away_team_stats["field_goals_att"]

    away_BSBA_ratio = 0
    home_BSBA_ratio = 0

    if away_team_stats["blocks"]!= 0:
        away_BSBA_ratio = (away_team_stats["blocks"]*100)/(away_team_stats["blocks"]+away_team_stats["blocked_att"])

    if home_team_stats["blocks"]!=0:
        home_BSBA_ratio = (home_team_stats["blocks"]*100)/(home_team_stats["blocks"]+home_team_stats["blocked_att"])


    away_offreb_ratio = (away_team_stats["offensive_rebounds"]*100)/(away_team_stats["field_goals_att"]-away_team_stats["field_goals_made"])
    home_offreb_ratio = (home_team_stats["offensive_rebounds"]*100)/(home_team_stats["field_goals_att"]-home_team_stats["field_goals_made"])


    away_defreb_ratio = (away_team_stats["defensive_rebounds"]*100)/(home_team_stats["field_goals_att"]-home_team_stats["field_goals_made"])
    home_defreb_ratio = (home_team_stats["defensive_rebounds"]*100)/(away_team_stats["field_goals_att"]-away_team_stats["field_goals_made"])


    away_team_data["poss"] = away_possessions
    away_team_data["poss_ratio"] = away_poss_ratio
    away_team_data["TO_ratio"] = away_TO_ratio
    away_team_data["BA_ratio"] = away_BA_ratio
    away_team_data["BSBA_ratio"] = away_BSBA_ratio
    away_team_data["offreb_ratio"] = away_offreb_ratio
    away_team_data["defreb_ratio"] = away_defreb_ratio

    home_team_data["poss"] = home_possessions
    home_team_data["poss_ratio"] = home_poss_ratio
    home_team_data["TO_ratio"] = home_TO_ratio
    home_team_data["BA_ratio"] = home_BA_ratio
    home_team_data["BSBA_ratio"] = home_BSBA_ratio
    home_team_data["offreb_ratio"] = home_offreb_ratio
    home_team_data["defreb_ratio"] = home_defreb_ratio
    

    away_post_string = '/TeamsDef/'+away_team_id+'/Game'+str(gameNo)+'/'
    home_post_string = '/TeamsDef/'+home_team_id+'/Game'+str(gameNo)+'/'


    result = firebase_db.post(away_post_string,away_team_data)
    result = firebase_db.post(home_post_string,home_team_data)






#result = firebase_db.delete("/Teams",None)

    




