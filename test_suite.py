import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication
from nba_functions import *
import sys
import matplotlib.pyplot as plt


def sd_calc(data):
    n = len(data)

    if n <= 1:
        return 0.0

    mean = float(sum(data))/len(data)
    sd = 0.0
    # calculate stan. dev.
    for el in data:
        sd += (float(el) - mean)**2
    sd = math.sqrt(sd / float(n-1))

    return sd


def checkTotal(avg_total,real_total,bov_total):

    if real_total == bov_total:
        return 1

    if avg_total < bov_total:
        if real_total < bov_total:
            return 1
    else:
        if real_total > bov_total:
            return 1
    return 0

def checkLine(avg_line,real_line,bov_line):
    if real_line == bov_line:
        return 1

    #choose away team
    if ((avg_line-bov_line)>0):
        if ((real_line-bov_line)>0):
            return 1

    #choose home team
    else:
        if ((real_line-bov_line)<0):
            return 1 
    

    return 0


def test_games(start,finish):
    correct_line_ratio = []
    correct_total_ratio = []
    
    firebase_db = firebase.FirebaseApplication('https://nbasort.firebaseio.com/', authentication=None)
    for i in range(start,finish):
        if i != 558:
            game_data = {}
            [away_team_id, home_team_id,away_team_name, home_team_name,away_points,home_points]= get_team_ids(i)
            real_total = away_points + home_points
            real_line = away_points - home_points
            
            [lines,sums,home_final_score,away_final_score] = run_game(300,away_team_id, home_team_id,away_team_name, home_team_name)

            #print lines
            avg_line = float(sum(lines))/len(lines)
            sd_line = sd_calc(lines)
            #zline = float(real_line - avg_line)/sd_line
            #zscores_lines.append(zline)

            #print totals
            avg_total = float(sum(totals))/len(totals)
            sd_total = sd_calc(totals)
            #ztotal = float(real_total-avg_total)/sd_total
            #zscores_total.append(ztotal)

            get_string = '/Output/Game'+str(i)+'/'
            result = firebase_db.get(get_string,None)
            data_str = json.dumps(result)
            current_game = json.loads(data_str)

            game_key = current_game.keys()[0]
            game_data = current_game[current_game.keys()[0]]

            game_data["avg_total"] = avg_total
            game_data["avg_line"] = avg_line
            game_data["sd_total"] = sd_total
            game_data["sd_line"] = sd_line

            bov_line = game_data["line"]
            bov_total = game_data["total"]


            post_string = get_string+game_key+"/"
            
            firebase_db.patch(post_string,game_data)

            isTotalCorrect = checkTotal(avg_total,real_total,float(bov_total))
            isLineCorrect =  checkLine(avg_line,real_line,float(bov_line))
            correct_line_ratio.append(isLineCorrect)
            correct_total_ratio.append(isTotalCorrect)

            print "Game Print-----------------"
            print "My line: "+str(avg_line)+ " Bovada line: "+bov_line + " Real Line: "+str(real_line)
            print "My Total: "+str(avg_total)+ " Bovada total: "+bov_total + " Real total: "+str(real_total)

            
    return [correct_line_ratio, correct_total_ratio]

def test_whole_system():
    start = 500
    end = 550

    [l_ratio,t_ratio] = test_games(start,end)
    print l_ratio
    print t_ratio

    pline = []
    ptotal = []
    for y in range(0,len(l_ratio)):
        pline.append(sum(l_ratio[0:y+1])*100/(y+1))
        ptotal.append(sum(t_ratio[0:y+1])*100/(y+1))


    plt.plot(pline)
    plt.plot(ptotal)
    plt.show()

    return -1



def test_onegame(index):
    lines = []
    totals = []

    game_iterations = 30

    [away_team_id, home_team_id,away_team_name, home_team_name,away_points,home_points]= get_team_ids(index)


    print "-------- "+ away_team_name+"("+str(away_points)+") @ " + home_team_name+"("+str(home_points) + ")-----"

    [lines,sums,home_final_score,away_final_score] = run_game(game_iterations,away_team_id, home_team_id,away_team_name, home_team_name)

    print float(sum(lines))/len(lines)

    real_awayscore_plot = []
    for i in range(0,game_iterations):
        real_awayscore_plot.append(away_points)
        
    plt.plot(away_final_score)
    plt.plot(real_awayscore_plot)
    #plt.plot(home_final_score)
    plt.show()
    return [home_final_score,away_final_score]


#1208 Nets at Celtics. Normal game
#650 Blazers at Celtics. High Scoring game

for i in range(0,1):
    [home_final_score,away_final_score]= test_onegame(650+i)
    print home_final_score
    print away_final_score
    print float(sum(away_final_score))/len(away_final_score)
    print float(sum(home_final_score))/len(home_final_score)










    
