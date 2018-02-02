from lxml import html
import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication



## Pull Season schedule from nba sportsradar --------------
#conn = http.client.HTTPSConnection("api.sportradar.us")
#conn.request("GET", "/nba/trial/v4/en/games/2017/REG/schedule.json?api_key=9ced6hbudhabvug4jdhqsew3")
#res = conn.getresponse()
#data = json.load(res)
##pprint(data)
## -------------------------------------------------


##Post in the Firebase database of Schedule of Games -----------------
#firebase_db = firebase.FirebaseApplication('https://bball2018-9c679.firebaseio.com/', authentication=None)
#result = firebase_db.post('/Schedule',data)
## -------------------------------------------------


##In case I need to authorize --------------------
##secret = 'Heatlifer.1'
##dsn = 'https://nbasort.firebaseio.com'
##email = 'mrod642@gmail.com'
##new_user = "Michael"
## -------------------------------------------------


## Get Game Summaries from Game List from Firebase/Schedule -------------------------------
##Post game summaries in Games/Game

conn = http.client.HTTPSConnection("api.sportradar.us")
firebase_db = firebase.FirebaseApplication('https://bball2018-9c679.firebaseio.com/', authentication=None)
result = firebase_db.get('/Schedule/-L3U_D-g6XHGgDclRC69/games',None)
data_str = json.dumps(result)
game_list = json.loads(data_str)

#731
for game in game_list[736:765]:

    game_id = game["id"]
    get_string = "/nba/trial/v4/en/games/"+game_id+"/summary.json?api_key=9ced6hbudhabvug4jdhqsew3"
    conn.request("GET", get_string)
    res = conn.getresponse()
    data = json.load(res)
##    #pprint(data)

    post_string = "/Games/Game"+str(game_list.index(game))
    print post_string
    result = firebase_db.post(post_string,data)

## -------------------------------------------------







