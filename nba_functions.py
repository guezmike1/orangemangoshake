import requests
import math
import http.client
import json
from pprint import pprint
from firebase import firebase,FirebaseAuthentication
from random import randint
from credentials import *

firebase_db = get_firebasedb()
conn= get_conn()
trainedNo = get_trainedNo()
api_key = get_apikey()

#Only picks games before this one and home if home, away if away
def usethisgame(schedule_list, game, team_id,home,gameNo):
    usegame = True
    gameNumber = game[4:]
    
    if gameNo <= int(gameNumber):
        return False
    else:
        if schedule_list[int(gameNumber)]["home"]["id"] == team_id:
            if home:
                usegame = True
            else:
                usegame = False
        else:
            if home:
                usegame = False
            else:
                usegame = True

    return usegame


#stat is a string of the stat you want
def get_player_stat_list(team_id, player_id, player_fullname,home,gameNo):

    fgatt= []
    fgmade=[]
    ftatt=[]
    ftmade=[]
    threeatt=[]
    threemade=[]

    schedule_string = "/Schedule/-L3U_D-g6XHGgDclRC69/games"
    resultschedule = firebase_db.get(schedule_string,None)
    schedule_str = json.dumps(resultschedule)
    schedule_list = json.loads(schedule_str)
    
    get_string = "/Teams/"+team_id+"/"+player_id
    result = firebase_db.get(get_string,None)
    data_str = json.dumps(result)
    game_list = json.loads(data_str)
    

    if game_list is None:
        print player_fullname + " not on roster"
        return [[0],[0],[0],[0],[0],[0],0]

    else:
        name_key = game_list.keys()[0]
        #print "game number tested is: " + str(gameNo)
        for game in game_list:
            if game != "fullname":
                
                usegame = usethisgame(schedule_list,game, team_id,home,gameNo);
                #print "currentgame is "+str(game)+" and " +str(usegame)
                if usegame:
                    current_game = game_list[game]
                    game_stats = current_game[current_game.keys()[0]]
                    
                    if game_stats["minutes"] != "00:00":
                        fgatt.append(game_stats["field_goals_att"])
                        fgmade.append(game_stats["field_goals_made"])
                        ftatt.append(game_stats["free_throws_att"])
                        ftmade.append(game_stats["free_throws_made"])
                        threeatt.append(game_stats["three_points_att"])
                        threemade.append(game_stats["three_points_made"])
        noGames = len(fgatt)
        #print fgatt
        return [fgatt,fgmade,ftatt,ftmade,threeatt,threemade,noGames]


def usegamedef(schedule_list, game, team_id,home,gameNo):
    usegame = True
    gameNumber = game[4:]
    
    if gameNo <= int(gameNumber):
        return False
    else:
        if schedule_list[int(gameNumber)]["home"]["id"] == team_id:
            if home:
                usegame = True
            else:
                usegame = False
        else:
            if home:
                usegame = False
            else:
                usegame = True

    return usegame


def get_def_data(away_team_id, home_team_id, gameNo):

    poss = []
    ba_ratio = []
    bsba_ratio = []
    defreb_ratio = []
    offreb_ratio = []
    to_ratio = []

    schedule_string = "/Schedule/-L3U_D-g6XHGgDclRC69/games"
    resultschedule = firebase_db.get(schedule_string,None)
    schedule_str = json.dumps(resultschedule)
    schedule_list = json.loads(schedule_str)
    
    
    stat_string = "TeamsDef/"+home_team_id
    result = firebase_db.get(stat_string,None)
    data_str = json.dumps(result)
    game_list = json.loads(data_str)

    usegame = True;

    for game in game_list:
        usegame = usegamedef(schedule_list, game, home_team_id,True, gameNo)
        if usegame:
            current_game = game_list[game]
            game_stats = current_game[current_game.keys()[0]]
            poss.append(game_stats["poss"])
            ba_ratio.append(game_stats["BA_ratio"])
            bsba_ratio.append(game_stats["BSBA_ratio"])
            defreb_ratio.append(game_stats["defreb_ratio"])
            offreb_ratio.append(game_stats["offreb_ratio"])
            to_ratio.append(game_stats["TO_ratio"])

    avg_poss = round(float(sum(poss))/len(poss))
    avg_ba_ratio = round(float(sum(ba_ratio))/len(ba_ratio))
    avg_bsba_ratio = round(float(sum(bsba_ratio))/len(bsba_ratio))
    avg_defreb_ratio = round(float(sum(defreb_ratio))/len(defreb_ratio))
    avg_offreb_ratio = round(float(sum(offreb_ratio))/len(offreb_ratio))
    avg_to_ratio = round(float(sum(to_ratio))/len(to_ratio))

    stat_string = "TeamsDef/"+away_team_id
    result = firebase_db.get(stat_string,None)
    data_str = json.dumps(result)
    game_list = json.loads(data_str)

    poss = []
    ba_ratio = []
    bsba_ratio = []
    defreb_ratio = []
    offreb_ratio = []
    to_ratio = []
    usegame = True

    for game in game_list:
        usegame = usegamedef(schedule_list, game, away_team_id,False, gameNo)
        if usegame:
            current_game = game_list[game]
            game_stats = current_game[current_game.keys()[0]]
            poss.append(game_stats["poss"])
            ba_ratio.append(game_stats["BA_ratio"])
            bsba_ratio.append(game_stats["BSBA_ratio"])
            defreb_ratio.append(game_stats["defreb_ratio"])
            offreb_ratio.append(game_stats["offreb_ratio"])
            to_ratio.append(game_stats["TO_ratio"])

    avg_a_poss = round(float(sum(poss))/len(poss))
    avg_a_ba_ratio = round(float(sum(ba_ratio))/len(ba_ratio))
    avg_a_bsba_ratio = round(float(sum(bsba_ratio))/len(bsba_ratio))
    avg_a_defreb_ratio = round(float(sum(defreb_ratio))/len(defreb_ratio))
    avg_a_offreb_ratio = round(float(sum(offreb_ratio))/len(offreb_ratio))
    avg_a_to_ratio = round(float(sum(to_ratio))/len(to_ratio))        


    return [avg_poss,avg_ba_ratio,avg_bsba_ratio,avg_defreb_ratio,avg_offreb_ratio,avg_to_ratio,avg_a_poss,avg_a_ba_ratio,
            avg_a_bsba_ratio,avg_a_defreb_ratio,avg_a_offreb_ratio,avg_a_to_ratio]

def get_team_ids(index):
    
    schedule_string = "/Schedule/-L3U_D-g6XHGgDclRC69/games/"+str(index)
    result = firebase_db.get(schedule_string,None)
    data_str = json.dumps(result)
    this_game = json.loads(data_str)
    
    #pprint(this_game)
    
    #away_points = this_game["away_points"]
    #print away_points
    #home_points = this_game["home_points"]
    #print home_points

    away_team_id = this_game["away"]["id"]
    home_team_id = this_game["home"]["id"]

    away_team_name = this_game["away"]["name"]
    home_team_name = this_game["home"]["name"]
    #print

    #names = {away_team_id:away_team_name, home_team_id:home_team_name}
    #result = firebase_db.post("/Names",names)
    
    #return [away_team_id, home_team_id,away_team_name, home_team_name,away_points,home_points]
    return [away_team_id, home_team_id,away_team_name, home_team_name]


def get_stat_dict(team_id,home,gameNo):

    fgatt_dict = {}
    fgmade_dict = {}
    threeatt_dict = {}
    threemade_dict = {}
    ftatt_dict = {}
    ftmade_dict = {}
    nogames_dict = {}

    conn.request("GET", "/nba/trial/v4/en/teams/"+team_id+"/profile.json?api_key="+api_key)
    res = conn.getresponse()
    data_roster = json.load(res)

    player_list = data_roster["players"]
    
    #stat_string = "Teams/"+team_id
    #result = firebase_db.get(stat_string,None)
    #data_str = json.dumps(result)
    #player_list = json.loads(data_str)
    for player in player_list:
        use_player = True
        player_id = player["id"]
        player_fullname = player["full_name"]
        #print player_fullname + ": "+player_id

        if player["status"] == "ACT":
            if "injuries" in player.keys():
                player_inj = player["injuries"]
                player_status = player_inj[0]["status"]
                if "Out" in player_status:
                    use_player = False

        else:
            use_player = False
            
        #print use_player
        if use_player:  
            [fgatt,fgmade,ftatt,ftmade,threeatt,threemade,noGames] = get_player_stat_list(team_id, player_id, player_fullname,home,gameNo)
            #print player_fullname +" "+ str(fgatt)
            if len(fgatt) == 0:
                fgatt_dict[player_id] = 0
                #print player_fullname + "Games Average : "+str(round(100*float(sum(fgatt))/len(fgatt)))
                fgmade_dict[player_id] = 0
                threeatt_dict[player_id] = 0
                threemade_dict[player_id] = 0
                ftatt_dict[player_id] = 0
                ftmade_dict[player_id] = 0
                nogames_dict[player_id] = 0
            else:
                fgatt_dict[player_id] = round(100*float(sum(fgatt))/len(fgatt))
                #print player_fullname + "Games Average : "+str(round(100*float(sum(fgatt))/len(fgatt)))
                fgmade_dict[player_id] = round(100*float(sum(fgmade))/len(fgmade))
                threeatt_dict[player_id] = round(100*float(sum(threeatt))/len(threeatt))
                threemade_dict[player_id] = round(100*float(sum(threemade))/len(threemade))
                ftatt_dict[player_id] = round(100*float(sum(ftatt))/len(ftatt))
                ftmade_dict[player_id] = round(100*float(sum(ftmade))/len(ftmade))
                nogames_dict[player_id] = noGames

    ##Change this to be percentage of shots per game. account for a player not playing a game
    return [fgatt_dict, fgmade_dict,threeatt_dict,threemade_dict,ftatt_dict,ftmade_dict, nogames_dict]
        


def choose_play_type(two,three,ft,to):
    printer = False
    total = ft+two+three+to
    val = randint(0,total)

    if printer:
        print "FT: "+ str(ft)+" Two: "+str(two)+" Three: "+str(three)+" TO: "+str(to) +" VAL: "+str(val)

    if val <= ft:
        return 1
    elif val <= (two+ft):
        return 2
    elif val <= (three+two+ft):
        return 3
    else:
        return 4



def choose_shooter(play_type, data_att):

    printer = False
    
    total = sum(data_att.values())
    val = randint(0,total)
    
    csum = 0

    
    for player in data_att.keys():
        csum = csum + data_att[player]
        if csum >= val:
            return player

    print "Error in choosing Shooter"
    return 0



def points_made(play_type,shooter,data_att,data_made,team):

    printer = False

    points = 0
    shots_att = data_att[shooter]
    shots_made = data_made[shooter]

    if team == 1:
        max_val = round(shots_att*0.95)
    else:
        max_val = shots_att

    val = randint(0,max_val)

    if printer:
        print "Player: "+shooter+" Type: "+str(play_type)+" "+str(shots_made)+"/"+str(shots_att)+ " val: "+str(val)
    
    if val <= shots_made:
        points = play_type

    else:
        points = points

    if play_type == 1:
        val = randint(0,shots_att)
        if val<shots_made:
            points = points + play_type
        else:
            #Add offensive boards on second miss instead of double miss
            points = points

    return points




def choose_block(ba_ratio,bsba_ratio):

    val = randint(0,100)

    if val < ba_ratio:
        val2 = randint(0,100)
        if val2 < bsba_ratio:
            return True
    
    return False

#returns 100*totalshotsoverallgames
def find_pg(cur_dict,game_dict, ft):
    #sum_shots = 0
    sum_shots = round(float(sum(cur_dict.values()))/100)
    
##    for player in cur_dict.keys():
##        p_shotspg = cur_dict[player]
##        p_noGames = game_dict[player]
##        season_shots = p_shotspg*p_noGames
##        sum_shots = sum_shots+season_shots
    if ft:
        sum_shots = round(sum_shots/2)
    #print sum_shots
    return sum_shots

    

def run_game(loops,away_team_id,home_team_id,away_team_name,home_team_name,gameNo):
    
    [afgatt_dict, afgmade_dict,athreeatt_dict,athreemade_dict,aftatt_dict,aftmade_dict,anogames_dict]= get_stat_dict(away_team_id,False,gameNo)
    [fgatt_dict, fgmade_dict,threeatt_dict,threemade_dict,ftatt_dict,ftmade_dict,nogames_dict]= get_stat_dict(home_team_id,True,gameNo)

    #returned team stats
    [poss,ba_ratio,bsba_ratio,defreb_ratio,offreb_ratio,to_ratio,aposs,aba_ratio,absba_ratio,adefreb_ratio,aoffreb_ratio,ato_ratio]= get_def_data(away_team_id,home_team_id,gameNo)


    print_boxscore = False
    print_summary = False
    print_finalscore = False
    

    lines = []
    sums = []
    home_final_score = []
    away_final_score = []

    #Averaged the average possessions of each team. 
    game_poss = round((poss+aposs)/2)

    #print "Total possessions: "+str(game_poss)
    #Get number of each shot per game
    shots_pg = find_pg(fgatt_dict, nogames_dict,False)
    #print home_team_name + " Shots_pg: " +str(shots_pg)
    three_pg = find_pg(threeatt_dict, nogames_dict,False)
    #print home_team_name + " Three_pg: " +str(three_pg)
    ft_pg = find_pg(ftatt_dict, nogames_dict,True)
    #print home_team_name + " ft_pg: " +str(ft_pg)

    ashots_pg = find_pg(afgatt_dict, anogames_dict,False)
    #print away_team_name + " afg_pg: " +str(ashots_pg)
    athree_pg = find_pg(athreeatt_dict, anogames_dict,False)
    #print away_team_name + " athree_pg: " +str(athree_pg)
    aft_pg = find_pg(aftatt_dict, anogames_dict,True)
    #print away_team_name + " aft_pg: " +str(aft_pg)


    for x in range(0,loops):
        final_score = [0,0]
        turnovers = [0,0]
        blocks = [0,0]
        fg = [0,0]
        fgatt = [0,0]
        offreb = [0,0]
        box_score_away = {}
        box_score_home = {}

        for i in range(0,int(game_poss)):
        #for i in range(0,5):
            off_reb = True
            while off_reb:
                team = 1
                off_reb = False
                play_type = choose_play_type(shots_pg-three_pg, three_pg, ft_pg, to_ratio)
                if play_type != 4:
                    [att_dict, made_dict] = select_dict(play_type,fgatt_dict, fgmade_dict,threeatt_dict,threemade_dict,ftatt_dict,ftmade_dict)
                    [points_added, is_blocked,fg_val,fgatt_val,blocks_val,shooter] = field_goal_att(team,play_type,att_dict,made_dict,fg[team],fgatt[team],blocks[0],aba_ratio,absba_ratio) 
                    fg[team] = fg_val
                    fgatt[team] = fgatt_val
                    blocks[0] = blocks_val

                    if print_boxscore:
                        box_score_home = update_boxscore(box_score_home,points_added, play_type, shooter) 
                    
                    
                    if is_blocked==False:
                        if points_added == 0:
                            off_reb = is_offreb(offreb_ratio, adefreb_ratio)
                            if off_reb:
                                offreb[team] = offreb[team]+1                
                    final_score[team] = final_score[team] + points_added
                else:
                    turnovers[team] = turnovers[team]+1


            off_reb = True
            while off_reb:
                off_reb = False
                team = 0
                aplay_type = choose_play_type(ashots_pg-athree_pg, athree_pg, aft_pg,ato_ratio)
                if aplay_type != 4:
                    [att_dict, made_dict] = select_dict(aplay_type,afgatt_dict, afgmade_dict,athreeatt_dict,athreemade_dict,aftatt_dict,aftmade_dict)
                    [apoints_added, ais_blocked,fg_val,fgatt_val,blocks_val,shooter] = field_goal_att(team,aplay_type,att_dict,made_dict,fg[team],fgatt[team],blocks[1],ba_ratio,bsba_ratio) 
                    fg[team] = fg_val
                    fgatt[team] = fgatt_val
                    blocks[1] = blocks_val

                    if print_boxscore:
                        box_score_away = update_boxscore(box_score_away,apoints_added, aplay_type, shooter) 
                    
                    
                    if ais_blocked==False:
                        if apoints_added == 0:
                            off_reb =  is_offreb(aoffreb_ratio, defreb_ratio)
                            if off_reb:
                                offreb[team] = offreb[team]+1
                    final_score[team] = final_score[team] + apoints_added
                else:
                    turnovers[team] = turnovers[team]+1

                
            #print str(i) + ": " + str(final_score[0]) + ", " +str(final_score[1])

        if print_finalscore:
            print "Final score is "+ away_team_name +" " + str(final_score[0]) + " "  + home_team_name + " " +str(final_score[1])

        if print_summary:
            print "Turnovers: ["+away_team_name+": "+str(turnovers[0])+","+home_team_name+": "+str(turnovers[1])+"]"
            print "Blocks:    ["+away_team_name+": "+str(blocks[0])+","+home_team_name+": "+str(blocks[1])+"]"
            print "FG:        ["+away_team_name+": "+str(fg[0])+","+home_team_name+": "+str(fg[1])+"]"
            print "FGatt:     ["+away_team_name+": "+str(fgatt[0])+","+home_team_name+": "+str(fgatt[1])+"]"
            print "offreb:    ["+away_team_name+": "+str(offreb[0])+","+home_team_name+": "+str(offreb[1])+"]"
            print
            print
        line = final_score[0]-final_score[1]
        lines.append(line)
        total = final_score[0]+final_score[1]
        sums.append(total)
        home_final_score.append(final_score[1])
        away_final_score.append(final_score[0])

        if print_boxscore:
            print_boxscore_function(box_score_away, box_score_home,away_team_name,home_team_name,away_team_id,home_team_id)


    print "~~~~~Averages of " + str(loops) + " loops ~~~~"
    avg_away_score = sum(away_final_score)/float(len(away_final_score))
    avg_home_score = sum(home_final_score)/float(len(home_final_score))
    print "Final score is "+ away_team_name +" " + str(avg_away_score) + " "  + home_team_name + " " +str(avg_home_score)

    return [home_final_score,away_final_score]



def print_boxscore_function(box_score_away, box_score_home,away_team_name,home_team_name,away_team_id,home_team_id):
    firebase_db = firebase.FirebaseApplication('https://bball2018-9c679.firebaseio.com/', authentication=None)

    print "---------------  "+away_team_name+ "-----------"
    for shooter in box_score_away:
        #print "Shooter is "+ shooter
        
        get_string = "/Teams/"+away_team_id+"/"+shooter
    
        result = firebase_db.get(get_string,None)
        data_str = json.dumps(result)
        player_outer = json.loads(data_str)
        
        if player_outer is None:
            box_score_away[shooter][0] = shooter
        else:
            name_json = player_outer["fullname"]
            name = name_json[name_json.keys()[0]]
            box_score_away[shooter][0] = name

        print box_score_away[shooter][0] + " :" + str(box_score_away[shooter][1:len(box_score_away[shooter])] )
        

    print "---------------  "+home_team_name+ "-----------"

    for shooter in box_score_home:
        
        get_string = "/Teams/"+home_team_id+"/"+shooter
    
        result = firebase_db.get(get_string,None)
        data_str = json.dumps(result)
        player_outer = json.loads(data_str)
        
        if player_outer is None:
            box_score_home[shooter][0] = shooter
        else:
            name_json = player_outer["fullname"]
            name = name_json[name_json.keys()[0]]
            box_score_home[shooter][0] = name

        print box_score_home[shooter][0] + " :" + str(box_score_home[shooter][1:len(box_score_home[shooter])]) 

    print "----------------------------------"
    print "----------------------------------"
    return True




def update_boxscore(box_score,points_added, play_type, shooter):
    name_idx = 0
    points_idx = 1
    fgmade_idx = 2
    fgatt_idx = 3
    threemade_idx = 4
    threeatt_idx = 5
    ftmade_idx = 6
    ftatt_idx = 7
    
    if shooter in box_score.keys():
        shooter_stats = box_score[shooter]
    else:
        shooter_stats = ["Name",0,0,0,0,0,0,0]

    if play_type == 1:
        shooter_stats[ftatt_idx] = shooter_stats[ftatt_idx]+2
        shooter_stats[ftmade_idx] = shooter_stats[ftmade_idx] + points_added

    elif play_type == 2:
        shooter_stats[fgatt_idx] = shooter_stats[fgatt_idx]+1
        if points_added != 0:
            shooter_stats[fgmade_idx] = shooter_stats[fgmade_idx] + 1

    elif play_type == 3:
        shooter_stats[fgatt_idx] = shooter_stats[fgatt_idx]+1
        shooter_stats[threeatt_idx] = shooter_stats[threeatt_idx]+1

        if points_added != 0:
            shooter_stats[fgmade_idx] = shooter_stats[fgmade_idx] + 1
            shooter_stats[threemade_idx] = shooter_stats[threemade_idx]+1
    else:
        shooter_stats = shooter_stats


    shooter_stats[points_idx] = shooter_stats[points_idx] + points_added


    box_score[shooter] = shooter_stats

    return box_score




def select_dict(play_type,fgatt_dict, fgmade_dict,threeatt_dict,threemade_dict,ftatt_dict,ftmade_dict):
    if play_type == 1:
        data_att = ftatt_dict
        data_made = ftmade_dict
    elif play_type == 2:
        data_att = fgatt_dict
        data_made = fgmade_dict
    elif play_type == 3:
        data_att = threeatt_dict
        data_made = threemade_dict
    else:
        print "bad play type"
        data_att = {}


    return [data_att, data_made]


def is_offreb(my_offreb, their_defreb):
    total = my_offreb+their_defreb
    val = randint(0,int(total))

    if val < my_offreb:
        return True

    return False


def field_goal_att(team, play_type,att_dict, made_dict,fg,fgatt,blocks_val,aba_ratio,absba_ratio):
      
    shooter = choose_shooter(play_type, att_dict)
    points_added = points_made(play_type,shooter,att_dict, made_dict,team)
    is_blocked = False
    
    if play_type == 2:
        is_blocked = choose_block(aba_ratio,absba_ratio)
        if is_blocked:
            blocks_val = blocks_val+1
            points_added = 0

    if play_type==2 or play_type == 3:
        fgatt = fgatt+1
        if points_added != 0:
            fg = fg+1

    

    return [points_added, is_blocked,fg,fgatt,blocks_val,shooter]
    
