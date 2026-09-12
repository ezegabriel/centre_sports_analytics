from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from pandas import DataFrame
import os
import urllib
import urllib.request
from pathlib import Path
import csv
import re
import ssl

# Main directory to Summer Research folder
main_dir = '/Users/HP/.spyder-py3/Summer_Research/'
#sports = ['mens-basketball', 'womens-basketball']

# Temporary variable; should loop through all sports
sports = ['mens-basketball']


saa_teams = ['berry', 'birmingham-southern', 'centre', 'hendrix', 'millsaps', 'oglethorpe', 'rhodes', 'sewanee']
schools = ['berryvikings', 'bscsports', 'centrecolonels', 'hendrixwarriors', 'gomajors', 'rhodeslynx', 'sewaneetigers']
# Temporary variable; should loop through all schools
schools = ['centrecolonels']

# Come back to 2018 for sewaneetigers
start_year = 2022 # fall of first year to get header data
end_year = 2022 # fall of last year to get header data

  
    
def getPlayer(play_type, data):
    '''Returns player name or 0 if not applicable
'''
    
  
    if play_type in data:
        if ' team' in data:
            return '0'
        else:
            index = data.find('by')
            subset = data[index+len('by '):(len(data))]
            occurance = 1
            end_of_name = len(subset)
            for m in re.finditer(',', subset):
                start = m.start()
                end = m.end()
                if occurance == 2:
                    end_of_name = m.end()
                occurance +=1
            player_name = subset[0:(end_of_name)]
            player_name = player_name.replace('.','')
            player_name = player_name.strip()
            name = player_name
            # if ',' in player_name:
            #      player_name = player_name.split(',')
            #      name = player_name[1] + ' ' + player_name[0]
            # else:
            #      name = player_name
            if '(in the paint)' in data:
                name = name.replace('(in the paint)', '')

            return name

        
    else:
       
        return '0'
           

def getCentreIndex(boxscore):
    '''
    

    Parameters
    ----------
    boxscore : bs tag
        Derived from beautiful soup, has all useful data from the html boxscore..

    Returns
    -------
    index : TYPE: int
        Index used to properly assign players to their team in possession information.
    headline : TYPE
        List holding the two schools involved.

    '''
    headline=[]
    away_team = boxscore.find('div', {'class':'team away'})
    away_logo = away_team.find('img')
    home_team = boxscore.find('div',{'class':'team home'})
    home_logo= home_team.find('img')
    
    headline.append(away_logo.attrs['alt'].lower())
    headline.append(home_logo.attrs['alt'].lower())
    
    if "centre" in headline[0]:
        index = 0
    else:
        index = 1
   
    return index, headline


# Gets all players from both teams assiged with an asterisk
def get_starters(player_table):
    lineup = []
    for tr in player_table.find_all('tr')[1:]:
            #print(tr)
            all_td = tr.find_all('td')
            
            '''
            This is very tricky. Some starters in the HTML file appear to have a single digit jersery number
            Others have double digits
            This line of code is written to take take of the above situation and any whitespace out of place
            The string is sliced from the second index to remove the jersey number attached
            Then, if there was a space after a single digit jersey number has been removed, the lstrip removes the whitespace from the left
            If after slicing and stripping, there remains a white space in any random position, the replace method removes that
            
            '''
            if all_td[2].text == '*':
                s_name = all_td[1].text[2:].lstrip().lower()
                if "," in s_name:
                    s_name = s_name.replace(", ", ",").replace(" ", ",")
                    #print(all_td[1].text)
                    lineup.append(s_name)
                else:
                    l_name = s_name.split(" ")
                    s_name = l_name[1] + "," + l_name[0]
                    lineup.append(s_name)
                
            '''It appears that games with the exception of the 2022-23 season, 
            have the orientation of the names wrong, 
            and with a discrepancy in how the commas are inserted
            
            Also, the encoding is off.
            The starters name are encoded in a table header data cell
            So the position of the asterisk moves down by one when extracting the table data from the table row
            
            An anomaly has been found in a particular game
            There happens to be a sixth starters and his name is "Team"
            The try and except computation deals with this data problem
            
            '''
            if all_td[1].text == "*":
                s_name = tr.find("th").text.lower()
                
                # Computation for starters with no comma                
                if not "," in s_name:
                    l_name = s_name.split(" ")
                    #print(l_name, 1)
                    try:
                        s_name = l_name[2] + "," + l_name[1]
                        lineup.append(s_name)
                    except IndexError:
                        continue
                
                # Computation for starters with a comma and/or whitespace between first and last names
                # Sometimes the comma is followed by a white space
                # The strip method doesn't work, so i used the replace method twice
                # Note that only one replace method will be used
                # Because it's either there is a comma followed by a space
                # or there's a lone comma
                
                else:
                    s_name = s_name.replace(", ", " ").replace(",", " ")
                    l_name = s_name.split(" ")
                    #print(l_name, 2)
                    try:
                        s_name = l_name[1] + "," + l_name[2]
                        lineup.append(s_name)
                    except IndexError:
                        continue
                
    return lineup                


def isHome(data, df):
    '''
    Checks for an essential gameplay in the dataframe
    Returns a 1 if play occured for the home team
    Returns a 0 if not
    '''
    
    for info in df["home_play"]:
       info = info.lower()
       if data == info:   
             return '1'
       else:
            return "0"

    
def classification(playDescription, playData, points, teamName, a):
#playDescription is Play column in play by play csv
#playData is play Type column in play by play csv
#points is points earned column in play by play csv
#teamName is team column in play by play csv     
#a is year_check
    '''classifies plays into different subcategories so they can be sorted
    later on'''
    subData = ['subbing in', 'subbing out']
    shot = ['layup', 'three pointer', 'jumper', "tipin", 'dunk']
    d = {}
    count = 0
    quarter = []
    if a == True:
        print('it worksss')
    #print(playData)
    #print(playData[655], "AAA")
    for i in range(len(playData)):
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
            try:
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
            except KeyError:
                continue
    
                    
    #print(count)
    # print(d, len(d))
    # print()
    # print()
    # #print(quarter)
    # #print(len(d), len(playData))
    # print(playData, len(playData))
    # for key in range(len(d)):
    #     if not key in d.keys():
    #         d[key] = ""
    print("Another banger by rema")
    #print(d)
    print(len(playData))
    
    return d
    return quarter


    

def getOfficialName(boxscore):
    '''
    Function to get the names of the teams involved

    Parameters
    ----------
    boxscore : TYPE: bs tag
        Derived from beautiful soup, has all useful data from the html boxscore.

    Returns
    -------
    opponent_name : TYPE: string
        School name of the opponents.
    home_name : TYPE: string
        School name for either of the schools involved in line 22.

    '''
    headline=[]
    graphic = boxscore.find('div', {'class':'box-score-graphic'})
 
    away_team = graphic.find('div', {'class':'team away'})
    
    away_logo = away_team.find('img')
    home_team = graphic.find('div',{'class':'team home'})
    home_logo= home_team.find('img')
    headline.append(away_logo.attrs['alt'])
    headline.append(home_logo.attrs['alt'])
    print("fromgetofficial name")
    print(headline)
    # centre_index, headline_lower = getCentreIndex(boxscore)
    # if centre_index == 1:
    #     opponent_index = 0
    # else:
    #     opponent_index = 1

    away_name = headline[0].replace('logo','').strip().lower()
    #away_name = opponent_name
    #opponent_name = opponent_name
    #opponent_name = opponent_name
 
    home_name = headline[1].replace('logo','').strip().lower()
    # home_name = home_name
    # home_name = home_name.strip()
    # home_name = home_name.lower()
    
    # Opponenet msut come first, if it doesn't players will be assigned to the worong schools
    # This computation cross checks the order of the schools involved with the headline
    # if not opponent_name in headline_lower[0]:
    #     s_name_temp = opponent_name
    #     opponent_name = home_name
    #     home_name = s_name_temp
        
    return away_name, home_name


def possession_tracker(d, teamName, quarter, p, a, boxscore):
#d is a dictionary of classification of plays
#teamName is a list of all values in the Team column 
#quarter is a list of what quarter/half it is: returned in classfication()
#p is an empty list passed through that eventually tracks possession
#a is year_check()
    '''Tracks who has possession for every play. Marks as C for Centre or
    O for opponent'''
    nochange = ['free throw made', 'free throw missed', "sub", 'subbing in', 'subbing out', 'timeout', 'missed shot', 'block', 'offensive rebound', 'deadball rebound'] 
    tagon = ['assist', 'steal']
    track = ""
    away_team_name, home_team_name = getOfficialName(boxscore)
    print(away_team_name, home_team_name, 999)
    #at the start of each quarter it checks who has possession
    if d[0] == 'made shot' or d[0] == 'turnover':
        if teamName[0] == home_team_name:
            track = home_team_name
        elif teamName[0] != home_team_name:
            track = away_team_name
    elif d[0] == 'foul':
        if teamName[0] == home_team_name:
            track = away_team_name
        elif teamName[0] != home_team_name:
            track = home_team_name
    else:
        if teamName[0] == home_team_name:
            track = home_team_name
        else:
            track = away_team_name
    c = 0
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for i in range(0, len(d)):
        if d[i] == 'defensive rebound':
            if teamName[i] == home_team_name:
                p.append(track)
                track = home_team_name
            else:
                p.append(track)
                track = away_team_name
        elif d[i] == 'team rebound':
            if teamName[i] == teamName[i-1]:
                if teamName[i] == home_team_name:
                    track = away_team_name
                    p.append(track)
                else:
                    track = home_team_name
                    p.append(track)
            else:
                if teamName[i] == home_team_name:
                    track = home_team_name
                    p.append(track)
                else:
                    track = away_team_name
                    p.append(track)
        elif d[i] == 'turnover':
            if teamName[i] == home_team_name:
                p.append(track)
                track = away_team_name
            else:
                p.append(track)
                track = home_team_name
        elif d[i] == 'defensive rebound':
            if teamName[i] == home_team_name:
                track = away_team_name
                p.append(track)
            else:
                track = home_team_name
                p.append(track)    
        elif d[i] == 'made shot':
        #Checks to see if it's an and one situation
            if i != len(d) - 2 and i != len(d) - 1:
                if d[i+1] == 'foul' and teamName[i+2] == teamName[i] and d[i+2] == 'final free throw made' or d[i+2] == 'free throw missed':
                    d[i+1] = 'defensive foul'
                    if teamName[i] != teamName[i+1]:
                        d[i] = 'and one'
                        #print(d[i], i, teamName[i], teamName[i+1])
                        if track == home_team_name:
                            p.append(track)
                        elif track == away_team_name:
                            p.append(track)
                    else:
                        if track == home_team_name:
                            p.append(track)
                            track = away_team_name
                        elif track == away_team_name:
                            p.append(track)
                            track = home_team_name
                elif d[i+1] == 'assist' and d[i+2] == 'foul' and teamName[i+3] == teamName[i] and (d[i+3] == 'final free throw made' or d[i+3] == 'free throw missed'):
                    d[i+2] = 'defensive foul'
                    if teamName[i] != teamName[i+2]:
                        d[i] = 'and one'
                        #print(d[i], i, teamName[i], teamName[i+1])
                        if track == home_team_name:
                            p.append(track)
                        elif track == away_team_name:
                            p.append(track)
                    else:
                        if track == home_team_name:
                            p.append(track)
                            track = away_team_name
                        elif track == away_team_name:
                            p.append(track)
                            track = home_team_name
                else:
                    if teamName[i] == home_team_name:
                        p.append(track)
                        track = away_team_name
                    else:
                        p.append(track)
                        track = home_team_name
            elif i == len(d) - 2 or i == len(d) - 1:
                if teamName[i] == home_team_name:
                    p.append(track)
                    track = away_team_name
                else:
                    p.append(track)
                    track = home_team_name
        elif d[i] == 'final free throw made':
            if teamName[i] == home_team_name:
                p.append(track)
                track = away_team_name
            else:
                p.append(track)
                track = home_team_name
        elif d[i] == 'start of quarter':
            if teamName[1] == home_team_name:
                if quarter[i] == 1 or quarter[i] == 3:
                    track = home_team_name
                    p.append(track)
                else:
                    track = away_team_name
                    p.append(track)
            else:
                if quarter[i] == 1 or quarter[i] == 3:
                    track = away_team_name
                    p.append(track)
                else:
                    track = home_team_name
                    p.append(track)
        elif d[i] == 'start of quarter1':
        #at the start of each quarter it checks who has possession
            if d[i+1] == 'made shot' or d[i+1] == 'turnover':
                if teamName[i+1] == home_team_name:
                    track = home_team_name
                    p.append(track)
                elif teamName[i+1] != home_team_name:
                    track = away_team_name
                    p.append(track)
            elif d[i+1] == 'foul':
                if teamName[i+1] == home_team_name:
                    track = away_team_name
                    p.append(track)
                elif teamName[i+1] != home_team_name:
                    track = home_team_name
                    p.append(track)
            else:
                if teamName[1] == home_team_name:
                    track = home_team_name
                    p.append(track)
                    #print(p[i], 7)
                else:
                    track = away_team_name
                    p.append(track)
        elif d[i] == 'start of quarter2':
            if d[i+1] == 'made shot' or d[i+1] == 'turnover':
                if teamName[i+1] == home_team_name:
                    track = home_team_name
                    p.append(track)
                elif teamName[i+1] != home_team_name:
                    track = away_team_name
                    p.append(track)
            elif d[i+1] == 'foul':
                if teamName[i+1] == home_team_name:
                    track = away_team_name
                    p.append(track)
                elif teamName[i+1] != home_team_name:
                    track = home_team_name
                    p.append(track)
            else:
                if p[q1] == home_team_name:
                    track = away_team_name
                    p.append(track)
                elif p[q1] == away_team_name:
                    track = home_team_name
                    p.append(track)
        elif d[i] == 'start of quarter3':
            if d[i+1] == 'made shot' or d[i+1] == 'turnover':
                if teamName[i+1] == home_team_name:
                    track = home_team_name
                    p.append(track)
                elif teamName[i+1] != home_team_name:
                    track = away_team_name
                    p.append(track)
            elif d[i+1] == 'foul':
                if teamName[i+1] == home_team_name:
                    track = away_team_name
                    p.append(track)
                elif teamName[i+1] != home_team_name:
                    track = home_team_name
                    p.append(track)
            else:
                if p[q2] == home_team_name:
                    track = away_team_name
                    p.append(track)
                elif p[q2] == away_team_name:
                    track = home_team_name
                    p.append(track)
        elif d[i] == 'start of quarter4':
            if d[i+1] == 'made shot' or d[i+1] == 'turnover':
                if teamName[i+1] == home_team_name:
                    track = home_team_name
                    p.append(track)
                elif teamName[i+1] != home_team_name:
                    track = away_team_name
                    p.append(track)
            elif d[i+1] == 'foul':
                if teamName[i+1] == home_team_name:
                    track = away_team_name
                    p.append(track)
                elif teamName[i+1] != home_team_name:
                    track = home_team_name
                    p.append(track)
            else:
                if p[q3] == home_team_name:
                    track = away_team_name
                    p.append(track)
                elif p[q3] == away_team_name:
                    track = home_team_name
                    p.append(track)
                #print(p[i], 7)
        elif d[i] in nochange:
            #if len(p)!= 0:
                if track == home_team_name:
                    p.append(track)
                elif track == away_team_name:
                    p.append(track)
        elif d[i] == 'defensive foul':
            if track == home_team_name:
                p.append(track)
            elif track == away_team_name:    
                p.append(track)
        elif d[i] == 'and one':
            if track == home_team_name:    
                p.append(track)
            elif track == away_team_name:   
                p.append(track)
        elif d[i] == 'foul':
        #Checks if fouls are offensive or defensive
                if track == home_team_name:
                    if teamName[i] == home_team_name:
                        if d[i+1] != 'turnover':
                            if a == False:
                                p.append(track)
                                track = away_team_name
                            elif a == True:
                                track = home_team_name
                                p.append(track)
                            d[i] = 'offensive foul'
                        else:
                            p.append(track)
                    
                    elif teamName[i] != home_team_name:
                        track = home_team_name
                        p.append(track)
                        d[i] = 'defensive foul'
                    
                elif track == away_team_name:
                    if teamName[i] == home_team_name:
                        track = away_team_name
                        p.append(track)
                        d[i] = 'defensive foul'
                
                    elif teamName[i] != home_team_name:
                        if d[i+1] != 'turnover':
                            if a == False:
                                p.append(track)
                                track = home_team_name
                            elif a == True:
                                track = away_team_name
                                p.append(track)
                            d[i] = 'offensive foul'
                            #print(i, 'off foul')
                        else:
                            p.append(track)
        elif d[i] == 'technical foul':
            if track == home_team_name:
                if teamName[i] == home_team_name:
                    p.append(track)
                    track = away_team_name
                else:
                    p.append(track)
            else:
                if teamName[i] == home_team_name:
                    p.append(track)
                else:
                    p.append(track)
                    track = home_team_name ####
        
        elif d[i] in tagon:
            #print("001", i, p)
            p.append(p[i-1])
        elif d[i] == 'technical free throw made' or 'technical free throw missed':
            p.append(track)
        else:
            print(d[i], "Gabriel")
        # if i < 20:
        #     #print(d[i], p)
    '''for i in range(0, len(p)-2):
        if p[i] != p[i+1]:
            print(i+2)'''
    #print(p)
    #print(len(p))
    #print(p[q1], p[q2], p[q3], p[q4])
    # return (d)
    # return p


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

# No actual use for this function
def plusminus(player, p, ppr, poss, players):
    #print(p)
    plusminus = 0
    lineup = ["", "", "", "", ""]
    for i in range(0, len(players)):
        #lineup = lineup.sort()
        if ppr[i] != " ":
            if player in players:
                if p[i] == "C":
                    plusminus = plusminus + ppr[i]
                else:
                    plusminus = plusminus - ppr[i]
    print(plusminus, player)
    print(players[0])
   
def makeHeaderPBP(sport, school, year_str):
    
    # Directory to the header folder of the current year
    header_dir = main_dir + sport + '/SAA/' + school + '/headers/' + year_str + '/'

    if not os.path.exists(header_dir): 
        return # bail out if no header directory for that year
    
    # Directory to the HTML folder of the current year
    html_dir = main_dir + sport + '/SAA/' + school + '/HTML/' + year_str + '/'
    
    # Directory to the Table folder of the current year
    table_dir = main_dir + sport + '/SAA/' + school + '/tables/' + year_str + '/'
    
    # Directory to the pbp folder of the current year
    pbp_dir = main_dir + sport + '/SAA/' + school + '/pbp/' + year_str + '/'
    
    # Create a pbp directory for that team is not already in existence
    if not os.path.exists(main_dir + sport + '/SAA/' + school + '/pbp/'):
        os.mkdir(main_dir + sport + '/SAA/' + school + '/pbp/')

    # Create a directory for that year if not already in existence
    if not os.path.exists(pbp_dir):
        os.mkdir(pbp_dir)

    # Creates a list of all csv files from the header directory of the current year
    header_files = sorted(os.listdir(header_dir))
    
    
    for header_file in header_files: # Loop through every csv files from the list

        # Open the csv files from the header directory for reading
        header_file_h = open(header_dir + header_file, 'r')
        #print(header_dir)
        print(header_file)
        print()
        
        header_data = list(csv.reader(header_file_h))
        #print(header_data)
 
        html_file = html_dir + header_file.split('_header')[0] + '.html'
        html_file_h = open(html_file, 'r')
        soup = bs(html_file_h, 'lxml')
        #soup = bs(r, 'html.parser')

        player_tables = soup.find_all('table',{'class':'sidearm-table overall-stats full hide-caption highlight-hover highlight-column-hover'})
        away_starters = get_starters(player_tables[0])
        home_starters = get_starters(player_tables[1])
        #print(player_tables[0])

        boxscore = soup.find('section', {'id':'box-score'})
        #centre_index, headline_temp = getCentreIndex(boxscore)
        #centre_index, headline = getCentreIndex(boxscore)

        #assigns first row of the header as list'header_titles' and second row as 'header_info'
        header_titles = header_data[0]
        header_info = header_data[1]

        table_file = header_file.replace('header', 'table')
        table_file_h = table_dir + table_file
        # Skip the entire game if table file does not exist
        try:
            table = open(table_file_h, 'r')
        except FileNotFoundError:
            continue
        
        pbp = soup.find('section', {'id' : 'play-by-play'})
        #centre_column = pbp.find_all('th',{'class':'hide-on-medium-down text-center'})[centre_index].text
        # centre_column = centre_column.strip()
        # centre_column = "home_play"
        #assigns the first row of the table as list'table_titles'
        table_data = list(csv.reader(table))
        table_titles = table_data[0]
        table_titles[0], table_titles[1], table_titles[5] ="timeRemaining", "awayPlay", "homePlay"
        table_titles[2], table_titles[3], table_titles[4] = "awayTeamScore", "playTeamIndicator", "homeTeamScore"
        table_titles[6], table_titles[7] = "gameScore", "teamIndicator"
        s_away, s_home = "", ""
        for pos in range(1, len(table_data)):
            '''
            I had to split the code into multiple if statements
            For the away and home side
            
            The away and home score don't have the same format
            so an error might occur if i try to encompass everything in one boolean expression
            Also, it will not look neat
            
            '''
            # For score with parenthesis on away side
            if "(" in table_data[pos][2]:
                away_index = table_data[pos][2].find("(")
                table_data[pos][2] = table_data[pos][2][:away_index]
                s_away = table_data[pos][2]
            
            # For regular score on away side
            if not "(" in table_data[pos][2] and table_data[pos][2] != "":
                s_away = table_data[pos][2]
                
            # For score with parenthesis on home side   
            if "(" in table_data[pos][4]:
                home_index = table_data[pos][4].find("(")
                table_data[pos][4] = table_data[pos][4][:home_index]
                s_home = table_data[pos][4]
                
            # For regular score on home side   
            if not "(" in table_data[pos][4] and table_data[pos][4] != "":
                s_home = table_data[pos][4]
                
            # Only place where the format is the same on play-by-play
            # For cells with empty strings
            # Replace with current home and away score
            if "" == table_data[pos][2]:
                table_data[pos][2] = s_away
                table_data[pos][4] = s_home
        
        # print(table_data)
    
        #puts all titles into a combined list
        all_titles = header_titles
        all_titles.extend(table_titles)

        df = pd.DataFrame(columns = all_titles)

        i = 1
        for row in range(len(table_data)-1):
            combined = header_info[:]
            combined.extend(table_data[i])
            df.loc[len(df.index)] = combined
            i+=1
                        
        away_name , home_name = getOfficialName(boxscore)
        away_lineup, home_lineup = get_starters(player_tables[0]), get_starters(player_tables[1]) 
        if "vanstaalduinen,matthijis" in away_lineup:
            a = away_lineup.index("vanstaalduinen,matthijis")
            away_lineup[a] = "van staalduinen,matt"
        df.head()
        #loops through the dataFrame.
        #going to use to loop through play data to create a new column
        #called type.
        Type, l_away_lineup, l_home_lineup = [], [], []
        #outcome from a shot
        Outcome= []
        #what team did what
        Team = []
        #name of player who was involved in the play
        player=[]
        #points earned
        points = []
        
        type_of_plays = ['foul ', 'jumper', 'rebound', '3ptr', ' ft ',
                            'turnover', 'timeout 30sec by ', '2ptr'
                        'steal', 'assist', 'layup', 'block ','sub', 'tipin']
        
        i = 0
        skip_line = 0 # Sets boolean to check order of substituition
        for data in df['Play']:
            data = data.lower()
            player_added = False
            for play_type in type_of_plays:
                player_name = getPlayer(play_type, data)
                player_name_check = player_name
                if player_name != '0' and player_name != "":
                    player.append(player_name)
                    player_added = True
                    break

            if 'jumper by' in data:
                Type.append('jumper')
                if 'good jumper ' in data:
                    Outcome.append('good')
                    points.append('2')
                elif 'miss jumper ' in data:
                    Outcome.append('missed')
                    points.append('')
                
                if player_added == False:
                    player.append('')
                #if isHome(data, df)== '1':
                if data == df['homePlay'][i].lower():
                    #Team.append('Centre')
                    Team.append(home_name)
                else:
                    #Team.append(official_opponent_name)
                    Team.append(away_name)
            elif 'layup by' in data:
                Type.append('layup')
                if 'good layup' in data:
                    Outcome.append('good')
                    points.append('2')
                elif 'miss layup' in data:
                    Outcome.append('missed')
                    points.append('')
                else:
                    Outcome.append('')
                    points.append('')
                if player_added == False:
                    player.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    #Team.append('Centre')
                    Team.append(home_name)
                else:
                    #Team.append(official_opponent_name)
                    Team.append(away_name)
                    
            elif 'tipin' in data:
                 Type.append('tipin')
                 if 'good tipin' in data:
                     Outcome.append('good')
                     points.append('2')
                 elif 'miss tipin' in data:
                     Outcome.append('missed')
                     points.append('')
                 else:
                     Outcome.append('')
                     points.append('')
                 if player_added == False:
                     player.append('')
                 #if isHome(data, df) == '1':
                 if data == df['homePlay'][i].lower():
                     #Team.append('Centre')
                     Team.append(home_name)
                 else:
                     #Team.append(official_opponent_name)
                     Team.append(away_name)
            elif 'dunk' in data:
                Type.append('dunk')
                if 'good dunk' in data:
                    Outcome.append('good')
                    points.append('2')
                else:
                    Outcome.append('')
                    points.append('')
                if player_added == False:
                    player.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    #Team.append('Centre')
                    Team.append(home_name)
                else:
                    #Team.append(official_opponent_name)
                    Team.append(away_name)
            elif 'assist' in data:
                Type.append('assist')
                if player_added == False:
                    player.append('')
                Outcome.append('')
                points.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    #Team.append('Centre')
                    Team.append(home_name)
                else:
                    #Team.append(official_opponent_name)
                    Team.append(away_name)
            elif 'ft by' in data:
                if player_added == False:
                    player.append('')
                Type.append('free throw')
                if 'good ft by ' in data:
                    Outcome.append('good')
                    points.append('1')
                elif 'miss ft by ' in data:
                    Outcome.append('missed')
                    points.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    #Team.append('Centre')
                    Team.append(home_name)
                else:
                    #Team.append(official_opponent_name)
                    Team.append(away_name)
            elif "2ptr by" in data:
                if player_added == False:
                    player.append('')
                Type.append('two pointer')
                if 'good' in data:
                    Outcome.append('good')
                    points.append('2')
                elif 'miss' in data:
                    Outcome.append('miss')
                    points.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
                
            elif 'foul' in data:
                if player_added == False:
                    player.append('')
                Type.append('foul')
                Outcome.append('')
                points.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
            elif 'turnover' in data:
                if player_added == False:
                    player.append('')
                Type.append('turnover')
                Outcome.append('')
                points.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
            elif 'steal ' in data:
                if player_added == False:
                    player.append('')
                Type.append('steal')
                Outcome.append('')
                points.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
            elif 'rebound' in data:
                if player_added == False:
                    player.append('')
                Outcome.append('')
                points.append('')
                if 'def by' in data:
                    Type.append('defensive rebound')
                elif 'deadb by' in data:
                    Type.append('deadball rebound')
                    
                elif 'off by' in data:
                    Type.append('offensive rebound')
                    
                else:
                    Type.append('')

                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
                    
            elif 'sub' in data:
                if 'out' in data:
                    Type.append("subbing out")
                    if skip_line == 0: # Run this block of command if there's a correct order of substituition
                        if (player_name in home_lineup) or (player_name in away_lineup):
                            
                            if data == df["homePlay"][i].lower():
                                #print(player_name, "hey")
                                #print("home lineup", home_lineup)
                                home_lineup.remove(player_name)
                                #print("edited home lineup", home_lineup)
                            else:
                                #print("away lineup", away_lineup)
                                away_lineup.remove(player_name)
                                #print("edited away lineup", away_lineup)
                        else:
                            skip_line = 1 # Skip the next substituition if no one came out
                            
                    # If a substituition was skipped, set skip_line to 0
                    # So that the next substituition can be validated in the right order
                    else:
                        skip_line = 0
                    
                elif "in" in data:
                    Type.append("subbing in")
                    if skip_line == 0: # Run this block of command if there's a correct order of substituition: 
                        if not (player_name in home_lineup or player_name in away_lineup): 
                            if data == df["homePlay"][i].lower():
                                #print("Home Lineup", home_lineup)
                                home_lineup.append(player_name)
                                #print("Edited home lineup", home_lineup)
                            else:
                                #print("Away Lineup", away_lineup)
                                away_lineup.append(player_name)
                                #print("Edited away lineup", away_lineup)
                        else:
                            skip_line = 1
                    else:
                        skip_line = 0
                    
                    
                elif 'starter' in data:
                    Type.append('starter')
                Outcome.append('')
                points.append('')
                if player_added == False:
                    player.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
            elif 'block' in data:
                Type.append('block')
                Outcome.append('')
                points.append('')
                if player_added == False:
                    player.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
            elif '3ptr by' in data:
                Type.append('three pointer')
                if 'miss' in data:
                    Outcome.append('missed')
                    points.append('')
                elif 'good' in data:
                    Outcome.append('good')
                    points.append('3')

                if player_added == False:
                    player.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
            elif 'timeout' in data:
                Type.append('timeout')
                Outcome.append('')
                points.append('')
                if player_added == False:
                    player.append('')
                #if isHome(data, df) == '1':
                if data == df['homePlay'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
            else:
                Type.append('')
                Outcome.append('')
                points.append('')
                Team.append('')
                if player_added == False:
                    player.append('')
            i+=1
            #print(away_lineup)
            l_away_lineup.append(away_lineup.copy())
            l_home_lineup.append(home_lineup.copy())
            
            
        
        
        #EDIT!!!!!!!!!!!!          
                            
        df['playType'] = Type
        print("len of play type", len(Type))
        df['shotOutcome'] = Outcome
        #print(Outcome, Team)
        df['Team']= Team
        df['Player'] = player
        df['pointsEarned'] = points
        df["awayLineup"] = l_away_lineup
        df["homeLineup"] = l_home_lineup
        time_in_secs = []
        for time in df['timeRemaining']:
        #for time in df['Time Remaining']:
            if time != '--' and 'Start' not in time:
                minutes = int(time.split(':')[0])
                seconds = int(time.split(':')[1])
                total_seconds = minutes * 60 + seconds
                time_in_secs.append(total_seconds)
                    
            else:
                time_in_secs.append('')
        df['timeSeconds'] = time_in_secs
        pbp_file = pbp_dir + header_file.replace('header', 'pbp')
        df.to_csv(pbp_file)
    
        '''
        BEGIN
        POSSESSION
        DATA
        
        I need the possession code to loop through all the game data
        The same time makeHeaderPBP function does it
        That way the pbp and function csv files are created accurately at the same time
        '''
        #file_path = '/Users/HP/.spyder-py3/Summer_Research/mens-basketball/SAA/centrecolonels/pbp/2019-20/centre_mens-basketball_2019-20_3907_greenville_pbp_1.csv'
        #file_path = main_dir + "/SAA/" + school + "/pbp/" + year_str +
        #a = year_check(file_path)
        b_check_year = year_check(pbp_file)
        #aggregate_stats()
        fullData = pd.read_csv(pbp_file, converters = {'Team':str})
        #put opponent name in data when not doing lineups
        data = pd.read_csv(pbp_file, usecols = ['Play', 'playType', 'Team', 'timeSeconds', 'pointsEarned', "homeLineup"])
        data = data.fillna(0)
        print(pbp_file)
        # Creation of Lists
        playDescription = data['Play'].tolist()
        
        print()
        print()
        try:
            time_in_secs[0] = 1200
        except IndexError:
            continue
        playOutcome = list(zip(Type,Team,time_in_secs))   
        limit = len(playOutcome) - 2
        possessionChange = []
        possessionCentre = []
        possessionClock = []
        possessionOpp = []
        
        p_tracker = [] # An empty list passed through that eventually tracks possession
        p_track_number = [] # An empty list passed through that eventually tracks possession number
        ppp_home = [] # An empty list that eventually tracks points scored during a whole possession
        ppp_away= [] # Same thing but for the away side
        
        p_track_time = []
        extraData = ['timeout', 'foul', 'deadball rebound', 'free throw', 'offensive rebound']
        change = ['defensive rebound', 'steal']
        possessionChange.append(np.nan)
        possessionClock.append(np.nan)
        #a is year check
        
        # Dictionary holding the play types from pbp, 'd' stands for the data type
        d_play_type = classification(playDescription, Type, points, Team, b_check_year)
        print()
        
        # This is a copy of d_play_type used to validate the possession_tracker function
        d_copy = d_play_type.copy()
        '''
        This sole purpose of this function is to modify some of the arguments passed
        Such as the main dictionary (d_play_type) and possession tracker (p_tracker)
        
        '''
        possession_tracker(d_play_type, Team, d_copy, p_tracker, b_check_year, boxscore)

        print("this is the lenght of b")
        if header_files.index(header_file) >= 11:
            #print(time_in_secs)
            print()
        print("daddy is home")
        #possession_counter(d_play_type, b_check_year)
        possession_points(points, p_track_number, p_tracker, d_copy, ppp_home, ppp_away)
        fullData.append(data)
        print()
        for i in range(0, len(ppp_away)):
            ppp_away[i] = float(ppp_away[i])

        fullData['Poss'] = p_tracker
        fullData['possNum'] = p_track_number
        #print(p_track_number)
        # print(len(p_track_number))
        # print(time_in_secs)
        #for i in range(len):
            
        print("this is ppr")
        if len(ppp_home) != len(ppp_away):
            ppp_home.append(0)
        fullData['pppHome'] = ppp_home
        fullData['pppAway'] = ppp_away
        #print(ppp_home)
        i_num, play_of_poss = 1, [1]
        for i in range(1, len(p_track_number)):
            if p_track_number[i] == i_num:
                play_of_poss.append(0)
            else:
                play_of_poss.append(1)
                i_num += 1
       
        fullData["PlayOfPoss"] = play_of_poss
        
        # Outputs csv file for possession information
        outname = header_file.replace("header", "possession") # Name of the possession csv file
        outdir = Path(main_dir + sport + "/SAA/" + school + "/possession/" + year_str + "/") # Name of the possession directory
        outdir.mkdir(parents = True, exist_ok = True) # Creates the non-existent directory above
        fullData.to_csv(outdir / outname) # Write all useful possession information to the file stored in the newly created directory
        
     

        
def main(schools, sports, start_year, end_year):
    for sport in sports: 
        for school in schools:
            year = start_year
            while year <= end_year:
                year_str = str(year) + '-' + str(year-2000+1)
                makeHeaderPBP(sport, school, year_str)
                #possession(sport, school, year_str)
                year += 1
    #print(sports)
main(schools, sports, start_year, end_year)