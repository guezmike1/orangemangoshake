import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication



firebase_db = firebase.FirebaseApplication('https://nbasort.firebaseio.com/', authentication=None)




##GET TEAMS PLAYING
result = firebase_db.get('/Schedule/-KnFSyixTJlx59nX6C1C/games/0',None)
data_str = json.dumps(result)

current_game = json.loads(data_str)

away_team_alias = current_game['away']['alias']
home_team_alias = current_game['home']['alias']

print away_team_alias
print home_team_alias



