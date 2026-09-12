#from openpyxl import load_workbook
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import csv
import os
import itertools
from collections import Counter
from getBasketballClean import *



def classification(playDescription, playData, points, teamName, a):
#playDescription is Play column in play by play csv
#playData is play Type column in play by play csv
#points is points earned column in play by play csv
#teamName is team column in play by play csv     
#a is year_check
    '''classifies plays into different subcategories so they can be sorted
    later on'''
    subData = ['subbing in', 'subbing out']
    shot = ['layup', 'three pointer', 'jumper']
    d = {}
    count = 0
    quarter = []
    if a == True:
        print('it works')
    #print(playData)
    #print(playData[655], "AAA")
    for i in range(0, len(playData)):
        if playData[i-1] == 'free throw':
            if points[i-1] == 1:
                if playData[i-2] != 'free throw' and playData[i-2] != 'deadball rebound':
                    if playData[i] != 'free throw' and playData[i] != 'deadball rebound':
                        d[i-1] = 'final free throw made'
                                               
        if playData[i] == 'free throw':
            if points[i] == 1:
                if playData[i-1] == 'free throw':
                    d[i] = 'final free throw made'
                elif playData[i-1] == 'deadball rebound':
                    d[i] = 'final free throw made'
                    
                else:
                    d[i] = 'free throw made'
            else:
                d[i] = 'free throw missed'
        elif playData[i] in subData:
            d[i] = 'sub'
        elif playData[i] in shot and points[i] == 2 or points[i] == 3:
            d[i] = 'made shot'    
        elif playData[i] in shot and points[i] != 2 and points[i] != 3:
            if 'GOOD DUNK' in str(playDescription[i]):
                #print(i, 'its working')
                d[i] = 'made shot'
            else:
                d[i] = 'missed shot'    
        elif playData[i] == 'turnover':
            d[i] = 'turnover'
            
        elif playData[i] == 'steal':
            d[i] = 'steal'
        elif playData[i] == 'block':
            d[i] = 'block'
        elif playData[i] == 'assist':
            d[i] = 'assist'
        elif playData[i] == 'defensive rebound':
            if 'TEAM' in str(playDescription[i]):
                d[i] = 'team rebound'
                print(i, 'what')
            else:
                d[i] = 'defensive rebound'
        elif playData[i] == 'offensive rebound':
            d[i] = 'offensive rebound'
        elif playData[i] == 'deadball rebound':
            d[i] = 'deadball rebound'
        elif playData[i] == 'timeout':
            d[i] = 'timeout'
        elif playData[i] == 'foul':
            if 'TECH' in str(playDescription[i]):
                #print(i, 'Tech')
                d[i] = 'technical foul'
            else:
                d[i] = 'foul'
        #elif playData[i] == 'technical foul':
            #d[i] = 'technical foul'
        #I don't think any plays are classified as technical fouls, but if wrong
        #this can be used
        
        
        else:
            #d[i] = 'start of quarter'
            #print(i)
            count = count + 1
            quarter.append(i)
            if count == 1:
                d[i] = 'start of quarter1'
                #print(i, d[i])
            if count == 2:
                d[i] = 'start of quarter2'
                #print(i, d[i])
            if count == 3:
                d[i] = 'start of quarter3'
                #print(i, d[i])
            if count == 4:
                d[i] = 'start of quarter4'
                #print(i, d[i])
        for i in range(2, len(d)):
            if d[i-2] == 'technical foul':
                if d[i-1] == 'final free throw made':
                    #print(i, 'technical free throw made')
                    d[i-1] = 'techincal free throw made'
                elif d[i-1] == 'free throw missed':
                    #print(i, 'technical free throw missed')
                    d[i-1] ='technical free throw missed'
                elif d[i] == 'final free throw made':
                    #print(i, 'technical free throw made')
                    d[i] = 'technical free throw made'
                elif d[i] == 'free throw missed':
                    #print(i, 'technical free throw missed')
                    d[i] = 'technical free throw missed'
    #print(count)
    #print(d)
    #print(quarter)
    #print(len(d))
    return d
    return quarter
    
                    
        
def possession_tracker(d, teamName, quarter, p, a):
#d is classification of plays
#teamName is Team column in play by play csv
#quarter is what quarter/half it is: returned in classfication()
#p is an empty list passed through that eventually tracks possession
#a is year_check()
    '''Tracks who has possession for every play. Marks as C for Centre or
    O for opponent'''
    nochange = ['free throw made', 'free throw missed', 'sub', 'timeout', 'missed shot', 'block', 'offensive rebound', 'deadball rebound'] 
    tagon = ['assist', 'steal']
    track = ""
    #at the start of each quarter it checks who has possession
    if d[1] == 'made shot' or d[1] == 'turnover':
        if teamName[1] == 'Centre':
            track = "C"
        elif teamName[1] != 'Centre':
            track = "O"
    elif d[1] == 'foul':
        if teamName[1] == 'Centre':
            track = "O"
        elif teamName[1] != 'Centre':
            track = "C"
    else:
        if teamName[1] == 'Centre':
            track = "C"
        else:
            track = "O"
    c = 0
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for i in range(0, len(d)):
        if d[i] == 'defensive rebound':
            if teamName[i] == 'Centre':
                p.append(track)
                track = "C"
            else:
                p.append(track)
                track = "O"
        elif d[i] == 'team rebound':
            if teamName[i] == teamName[i-1]:
                if teamName[i] == 'Centre':
                    track = 'O'
                    p.append(track)
                else:
                    track = 'C'
                    p.append(track)
            else:
                if teamName[i] == 'Centre':
                    track = 'C'
                    p.append(track)
                else:
                    track = 'O'
                    p.append(track)
        elif d[i] == 'turnover':
            if teamName[i] == 'Centre':
                p.append(track)
                track = "O"
            else:
                p.append(track)
                track = "C"
        elif d[i] == 'defensive rebound':
            if teamName[i] == 'Centre':
                track = "O"
                p.append(track)
            else:
                track = "C"
                p.append(track)    
        elif d[i] == 'made shot':
        #Checks to see if it's an and one situation
            if i != len(d) - 2 and i != len(d) - 1:
                if d[i+1] == 'foul' and teamName[i+2] == teamName[i] and d[i+2] == 'final free throw made' or d[i+2] == 'free throw missed':
                    d[i+1] = 'defensive foul'
                    if teamName[i] != teamName[i+1]:
                        d[i] = 'and one'
                        #print(d[i], i, teamName[i], teamName[i+1])
                        if track == 'C':
                            p.append(track)
                        elif track == 'O':
                            p.append(track)
                    else:
                        if track == 'C':
                            p.append(track)
                            track = "O"
                        elif track == 'O':
                            p.append(track)
                            track = "C"
                elif d[i+1] == 'assist' and d[i+2] == 'foul' and teamName[i+3] == teamName[i] and (d[i+3] == 'final free throw made' or d[i+3] == 'free throw missed'):
                    d[i+2] = 'defensive foul'
                    if teamName[i] != teamName[i+2]:
                        d[i] = 'and one'
                        #print(d[i], i, teamName[i], teamName[i+1])
                        if track == 'C':
                            p.append(track)
                        elif track == 'O':
                            p.append(track)
                    else:
                        if track == 'C':
                            p.append(track)
                            track = "O"
                        elif track == 'O':
                            p.append(track)
                            track = "C"
                else:
                    if teamName[i] == 'Centre':
                        p.append(track)
                        track = "O"
                    else:
                        p.append(track)
                        track = "C"
            elif i == len(d) - 2 or i == len(d) - 1:
                if teamName[i] == 'Centre':
                    p.append(track)
                    track = "O"
                else:
                    p.append(track)
                    track = "C"
        elif d[i] == 'final free throw made':
            if teamName[i] == 'Centre':
                p.append(track)
                track = "O"
            else:
                p.append(track)
                track = "C"
        elif d[i] == 'start of quarter':
            if teamName[1] == 'Centre':
                if quarter[i] == 1 or quarter[i] == 3:
                    track = "C"
                    p.append(track)
                else:
                    track = "O"
                    p.append(track)
            else:
                if quarter[i] == 1 or quarter[i] == 3:
                    track = "O"
                    p.append(track)
                else:
                    track = "C"
                    p.append(track)
        elif d[i] == 'start of quarter1':
        #at the start of each quarter it checks who has possession
            if d[i+1] == 'made shot' or d[i+1] == 'turnover':
                if teamName[i+1] == 'Centre':
                    track = "C"
                    p.append(track)
                elif teamName[i+1] != 'Centre':
                    track = "O"
                    p.append(track)
            elif d[i+1] == 'foul':
                if teamName[i+1] == 'Centre':
                    track = "O"
                    p.append(track)
                elif teamName[i+1] != 'Centre':
                    track = "C"
                    p.append(track)
            else:
                if teamName[1] == 'Centre':
                    track = "C"
                    p.append(track)
                    #print(p[i], 7)
                else:
                    track = "O"
                    p.append(track)
        elif d[i] == 'start of quarter2':
            if d[i+1] == 'made shot' or d[i+1] == 'turnover':
                if teamName[i+1] == 'Centre':
                    track = "C"
                    p.append(track)
                elif teamName[i+1] != 'Centre':
                    track = "O"
                    p.append(track)
            elif d[i+1] == 'foul':
                if teamName[i+1] == 'Centre':
                    track = "O"
                    p.append(track)
                elif teamName[i+1] != 'Centre':
                    track = "C"
                    p.append(track)
            else:
                if p[q1] == 'C':
                    track = "O"
                    p.append(track)
                elif p[q1] == 'O':
                    track = "C"
                    p.append(track)
        elif d[i] == 'start of quarter3':
            if d[i+1] == 'made shot' or d[i+1] == 'turnover':
                if teamName[i+1] == 'Centre':
                    track = "C"
                    p.append(track)
                elif teamName[i+1] != 'Centre':
                    track = "O"
                    p.append(track)
            elif d[i+1] == 'foul':
                if teamName[i+1] == 'Centre':
                    track = "O"
                    p.append(track)
                elif teamName[i+1] != 'Centre':
                    track = "C"
                    p.append(track)
            else:
                if p[q2] == 'C':
                    track = "O"
                    p.append(track)
                elif p[q2] == 'O':
                    track = "C"
                    p.append(track)
        elif d[i] == 'start of quarter4':
            if d[i+1] == 'made shot' or d[i+1] == 'turnover':
                if teamName[i+1] == 'Centre':
                    track = "C"
                    p.append(track)
                elif teamName[i+1] != 'Centre':
                    track = "O"
                    p.append(track)
            elif d[i+1] == 'foul':
                if teamName[i+1] == 'Centre':
                    track = "O"
                    p.append(track)
                elif teamName[i+1] != 'Centre':
                    track = "C"
                    p.append(track)
            else:
                if p[q3] == 'C':
                    track = "O"
                    p.append(track)
                elif p[q3] == 'O':
                    track = "C"
                    p.append(track)
                #print(p[i], 7)
        elif d[i] in nochange:
            #if len(p)!= 0:
                if track == 'C':
                    p.append(track)
                elif track == 'O':
                    p.append(track)
        elif d[i] == 'defensive foul':
            if track == 'C':
                p.append(track)
            elif track == 'O':    
                p.append(track)
        elif d[i] == 'and one':
            if track == 'C':    
                p.append(track)
            elif track == 'O':   
                p.append(track)
        elif d[i] == 'foul':
        #Checks if fouls are offensive or defensive
                if track == 'C':
                    if teamName[i] == 'Centre':
                        if d[i+1] != 'turnover':
                            if a == False:
                                p.append(track)
                                track = "O"
                            elif a == True:
                                track = "C"
                                p.append(track)
                            d[i] = 'offensive foul'
                        else:
                            p.append(track)
                    
                    elif teamName[i] != 'Centre':
                        track = "C"
                        p.append(track)
                        d[i] = 'defensive foul'
                    
                elif track == 'O':
                    if teamName[i] == 'Centre':
                        track = "O"
                        p.append(track)
                        d[i] = 'defensive foul'
                
                    elif teamName[i] != 'Centre':
                        if d[i+1] != 'turnover':
                            if a == False:
                                p.append(track)
                                track = "C"
                            elif a == True:
                                track = "O"
                                p.append(track)
                            d[i] = 'offensive foul'
                            #print(i, 'off foul')
                        else:
                            p.append(track)
        elif d[i] == 'technical foul':
            if track == 'C':
                if teamName[i] == 'Centre':
                    p.append(track)
                    track = 'O'
                else:
                    p.append(track)
            else:
                if teamName[i] == "Centre":
                    p.append(track)
                else:
                    p.append(track)
                    track == 'C'
        
        elif d[i] in tagon:
            p.append(p[i-1])
        elif d[i] == 'technical free throw made' or 'technical free throw missed':
            p.append(track)
        else:
            print(d[i])

    '''for i in range(0, len(p)-2):
        if p[i] != p[i+1]:
            print(i+2)'''
    #print(p)
    #print(len(p))
    #print(p[q1], p[q2], p[q3], p[q4])
    return (d)
    return p

def possession_points(points, poss, p, d, ppr, ppr2):
#b is possession_tracker()
#points is points earned column in play by play csv
#poss is an empty list passed through that eventually tracks possession number
#p tracks possession
#d is classfication()
#ppr is an empty list that eventually tracks points scored during a whole possession
#ppr2 is the same but shows that ppr on every row
    '''tracks points and prints the total points for possesssion at the end of
    the play and then in a seperate column the total points are printed on
    every play. Also tracks what possession number it is.'''
    count = 1
    counter = 0
    point = 0
    per = {}
    pe = []
    for i in range(0, len(p)-1):
        if p[i] == p[i+1]:
            poss.append(count)
            pe.append(0)
            if d[i+1] == 'start of quarter2':
                count = count + 1
            if d[i+1] == 'start of quarter3':
                count = count + 1            
            if d[i+1] == 'start of quarter4':
                count = count + 1
        elif p[i] != p[i+1]:
            poss.append(count)
            count = count + 1
            pe.append(points[i])
    '''for i in range(0, len(p)-1):
        if points[i] == 2 or points[i] == 3:
            if p[i] == p[i-1]:
                poss[i] = poss[i-1]
            #elif p[i] != p[i-1]:
                #poss[i] = poss[i] - 1
        if d[i] == 'turnover':
            if p[i] == p[i-1]:
                poss[i] = poss[i-1]
            #else:
                #poss[i] = poss[i] - 1
        if d[i] == 'assist':
            poss[i] = poss[i-1]
        if d[i] == 'final free throw made':
            poss[i] = poss[i-1]
            if i > 2:
                if d[i-2] == 'and one':
                    if p[i] == p[i-1]:
                        poss[i-2] = poss[i-3]
                        poss[i] = poss[i-1]
                    elif p[i] != p[i-1]:
                        poss[i] = poss[i] - 1
                        poss[i-2] = poss[i-2] - 1'''
    '''for i in range(0, len(p) - 1):
        if d[i] == 'made shot':
            if d[i] == d[i+1]:
                poss[i+1] = poss[i] + 1'''
    for i in range(1, len(d)):
        if d[i] == 'start of quarter':
            #print(i, start)
            poss[i] = poss[i] + 1
    '''for i in range(0, len(p) - 1):
        if d[i] == 'and one':
            poss[i] = poss[i] + 1
            poss[i+2] = poss[i+2] + 1
            if d[i-1] == 'turnover':
                poss[i] = poss[i] + 1   '''     
    for i in range(0, len(poss)):
        per[poss[i]] = 0
    for i in range(0, len(poss)):
        if points[i] == 2 or points[i] == 3 or points[i] == 1:
            per[poss[i]] += points[i]
            counter += points[i]
        elif d[i] == 'made shot' and points[i] == 0:
            per[poss[i]] += 2
            counter += 2
        '''if points[i] == 2 or points[i] == 3:
            per[int(poss[i])] = int(points[i])
            for j in range(0, len(poss)):
                if points[j] == 2 or points[i] == 3 or points[i] == 1 and poss[j] == poss[i] and i != j:
                    per[int(poss[[i]])] += int(points[j])
            #if d[i] == 'and one':
                #per[poss[i]] = per[poss[i]] + 
        else:
            per[poss[i]] = 0'''
            
    for i in range(0, len(poss)-1):
        #Designates which play is last in a possession
        if i != len(poss)-1:
            if poss[i] != poss[i+1]:
                ppr.append(per[poss[i]])
                if per[poss[i]] == 1 or per[poss[i]] == 2 or per[poss[i]] == 3:
                    ppr2.append(per[poss[i]])
                else:
                    ppr2.append(0)
            if poss[i] == poss[i+1]:
                ppr.append(' ')
                if per[poss[i]] == 1 or per[poss[i]] == 2 or per[poss[i]] == 3:
                    ppr2.append(per[poss[i]])
                else:
                    ppr2.append(0)
        if i == len(poss)-1 and d[i] != 'made shot':
            ppr.append(' ')
        if i == len(poss)-1 and d[i] == 'made shot':
            if points[i] == 0:
                ppr.append(2)
            else:
                ppr.append(points[i])
        '''if poss[i] == poss[len(poss)-1]:
            print('hhhh')
            if d[i+1] == 'made shot':
                del ppr[-1]
                ppr.append(per[poss[i]])
            if d[i+1] == 'made shot':
                del ppr[-1]
                ppr.append(per[poss[i]])'''
    #print(ppr)
    #print(per)
    ppr.append(' ')
    ppr.append(' ')
    ppr2.append(per[poss[len(poss)-1]])
    ppr2.append(per[poss[len(poss)-1]])
    for i in range(0, len(ppr)):
        if ppr[i] == ' ':
            ppr[i] = 0
    print(ppr[len(ppr)-1], 'should be 0')
    #print(sum(ppr), 'game sum')
    #print(len(ppr))        
    #print(counter)            
    #print(per)
    #print(poss[len(poss)-1], 'here')
    #print(ppr2)
    if p[len(p)-2] == p[len(p)-1]:
        poss.append(poss[len(poss)-1])
    else:
        poss.append(poss[len(poss)-2] + 1)
    if d[len(poss)-2] == 'made shot':
        ppr[len(poss)-2] = per[poss[len(poss) - 2]]
    if d[len(poss)-1] == 'made shot':
        del ppr[-1]
        ppr.append(per[poss[len(poss)-1]])
    return poss
    return ppr
        
            
            
                
def possession_counter(d, a):
#d is classification()
#a is year_check()
    '''counts total possessions'''
    possession = 0
    #print(d)
    for i in range(0, len(d)):
        if d[i] == 'final free throw made':
            possession += 1
            #print(i+2)
            #print(d[i])
        elif d[i] == 'made shot':
            possession += 1
            #print(i+2)
            #print(d[i])
        elif d[i] == 'turnover':
            possession += 1
            #print(i+2)
            #print(d[i])
        elif d[i] == 'defensive rebound':
            possession += 1
            #print(i+2)
            #print(d[i])
        elif d[i] == 'start of quarter1':
            possession += 1
            #print(i+2)
            #print(d[i])
        elif d[i] == 'start of quarter2':
            possession += 1
            #print(i+2)
            #print(d[i])
        elif d[i] == 'start of quarter3':
            possession += 1
            #print(i+2)
            #print(d[i])
        elif d[i] == 'start of quarter4':
            possession += 1
            #print(i+2)
            #print(d[i])
        elif d[i] == 'offensive foul':
            if a == False:
                possession += 1
            #print(i+2)
            #print(d[i])
    #print(possession, 'here')
    #print(d[137], d[138], d[139], d[140], d[141], d[142], d[143])
            
    
def year_check(file_path):
    '''checks if year is before 2016 because offensive fouls are marked as
    turnovers before that year.'''
    ch = ['2010', '2011', '2012', '2013', '2014', '2015']
    early_year = False
    for element in ch:
        if element in file_path:
            early_year = True
            print('Yep')
    #print(early_year)
    return early_year


def plusminus(player, p, ppr, poss, player1, player2, player3, player4, player5):
    #print(p)
    plusminus = 0
    lineup = ["", "", "", "", ""]
    for i in range(0, len(player1)):
        lineup[0] = player1[i]
        lineup[1] = player2[i]
        lineup[2] = player3[i]
        lineup[3] = player4[i]
        lineup[4] = player5[i]
        #lineup = lineup.sort()
        if ppr[i] != " ":
            if player  == (player1[i] or player2[i] or player3[i] or player4[i] or player5[i]):
                if p[i] == "C":
                    plusminus = plusminus + ppr[i]
                else:
                    plusminus = plusminus - ppr[i]
    print(plusminus, player)
    #print(lineup)        
    
    




#def lineups():
    
def main():
    '''Uncomment the directory part to go through multiple games'''
      #C:\Users\Kameron.DESKTOP-9OMTKVA\Desktop\FallResearch - File path
    # directory = r"/Users/HP/.spyder-py3/Summer_Research/Basketball/WomenBB_raw_data_by_year/2015"
    # for filename in os.listdir(directory):
    #     #print(filename)
    #     file_path =  directory+"/"+filename
    file_path = '/Users/HP/.spyder-py3/Summer_Research/Basketball/WomenBB_raw_data_by_year/2015/game1_maryville-tenn-_2264.csv'
    a = year_check(file_path)
    #aggregate_stats()
    print(a)
    fullData = pd.read_csv(file_path, converters = {'Team':str})
    #put opponent name in data when not doing lineups
    data = pd.read_csv(file_path, usecols = ['Play', 'Play Type', 'Team', 'Time(seconds)', 'Points Earned', 'player1',
                                              'player2', 'player3', 'player4', 'player5'])
    data = data.fillna(0)
    print(file_path)
    # Creation of Lists
    playDescription = data['Play'].tolist()
    playData = data['Play Type'].tolist()
    teamName = data['Team'].tolist()
    #opponentName = data['opponent name'].tolist()
    points = data['Points Earned'].tolist()
    gameClock = data['Time(seconds)'].tolist()
    player1 = data['player1'].tolist()
    player2 = data['player2'].tolist()
    player3 = data['player3'].tolist()     
    player4 = data['player4'].tolist()
    player5 = data['player5'].tolist()
    gameClock[0] = 1200
    playOutcome = list(zip(playData,teamName,gameClock))   
    limit = len(playOutcome) - 2
    possessionChange = []
    possessionCentre = []
    possessionClock = []
    possessionOpp = []
    
    p = []
    poss = []
    ppr = []
    ppr2 = []
    
    extraData = ['timeout', 'foul', 'deadball rebound', 'free throw', 'offensive rebound']
    change = ['defensive rebound', 'steal']
    possessionChange.append(np.nan)
    possessionClock.append(np.nan)
    #a is year check
    d = classification(playDescription, playData, points, teamName, a)
    e = classification(playDescription, playData, points, teamName, a)
    b = possession_tracker(d, teamName, e, p, a)
    possession_counter(b, a)
    
    print(ppr2)
    possession_points(points, poss, p, d, ppr, ppr2)
    fullData.append(data)
    for i in range(0, len(ppr2)):
        ppr2[i] = float(ppr2[i])
    print(ppr2)
    fullData['Possession Change'] = p
    fullData['Possession Number'] = poss
    fullData['Points Per Possession'] = ppr
    fullData['Points Per Possession2'] = ppr2
    fullData.to_csv (r'//Users/HP/.spyder-py3/Summer_Research/test.csv', index=False, header=True)
    print(d[302], d[303], d[304], d[305])
    counter2 = 0
    for i in range(0, len(p)-1):
        if p[i] != p[i+1]:
            counter2 = counter2 + 1
    print(counter2)
    print(playDescription[677], 'playDescription')
    jacob = plusminus("jacob bates", p, ppr, poss, player1, player2, player3, player4, player5)
    #g = lineup_analysis()
     
      
main()
