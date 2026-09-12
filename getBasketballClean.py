from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
import os
import urllib
import urllib.request
from pathlib import Path
import csv
import re
import ssl

'''This is for basketball
'''
import requests
import fileinput
import math



players = ['Jacob Bates', 'Perry Ayers', 'Art Walker', 'Bailey Rakes',
          'Carter Baughman', 'Dawson Crump', 'RJ Smith', 'Jakob Spitzer',
          'KC Purvis', 'Jalen Williams', 'Caleb Snyder']
symbol = '*'

starters = []
sl = []

def getTable():
    with open('/Users/drewdunn/Downloads/centre_mens-basketball_2019-20_3907_greenville.html', 'r') as f:

        contents = f.read()
        soup = bs(contents, 'html.parser')

        print(soup.h2)
        print(soup.head)
        print(soup.li)
    with open("pypi_packages.txt", "w+") as f:
        f.write(''.join(soup.html.findAll(text=True)))
    
    with open("pypi_packages.txt", "r") as fp:
        lines = fp.readlines()
        for line in lines:
            if line.find(symbol) !=-1:
                #print(symbol)
                #print(lines.index(line))
                #print(line)
                starters.append(symbol)
            for player in players:
                if line.find(player) != -1:
                    #print(player)
                    #print(lines.index(line))
                    #print(line)
                    starters.append(player)
    print(starters)
    for i in range(1, len(starters)-1):
        if starters[i] != "*":
            if starters[i+1] == "*" and starters[i-1] == "*":
                sl.append(starters[i])
    print(sl)
            
                   
    heading_tags = ["h1", "h2","h3", "h4"]
    for tags in soup.find_all(heading_tags):
        print(tags.name + ' -> ' + tags.text.strip())
    '''for row in soup.findAll('table')[0].tbody.findAll('tr'):
        first_column = row.findAll('th')[0].contents
        third_column = row.findAll('td')[0].contents
        print(first_column, third_column)

    df = pd.read_html'/Users/drewdunn/Downloads/centre_mens-basketball_2019-20_3907_greenville.html'.content,attrs = {'id': 'curr_table'})[0]
'''        
    return sl

def getOfficialName(boxscore,sport):
    headline=[]
    graphic = boxscore.find('div', {'class':'box-score-graphic'})
 
    away_team = graphic.find('div', {'class':'team away'})
    
    away_logo = away_team.find('img')
    home_team = graphic.find('div',{'class':'team home'})
    home_logo= home_team.find('img')
    headline.append(away_logo.attrs['alt'])
    headline.append(home_logo.attrs['alt'])
    centre_index = getCentreIndex(boxscore)
    if centre_index == 1:
        opponent_index = 0
    else:
        opponent_index = 1

    opponent_name = headline[opponent_index]
    opponent_name = opponent_name.replace('logo','')
    opponent_name = opponent_name.strip()
    opponent_name = opponent_name.lower()
 
    centre_name = headline[centre_index]
    centre_name = centre_name.replace('logo','')
    centre_name = centre_name.strip()
    centre_name = centre_name.lower()

    return opponent_name, centre_name
    
    
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

            if ',' in player_name:
                player_name = player_name.split(',')
                name = player_name[1] + ' ' + player_name[0]
            else:
                name = player_name
            if '(in the paint)' in data:
                name = name.replace('(in the paint)', '')

            return name

        
    else:
       
        return '0'
           

def getBoxScore(game_url):
    ssl._create_default_https_context = ssl._create_unverified_context
    r = urllib.request.urlopen(game_url)
            # Convert to a BS object
    soup = bs(r, 'html.parser')
    boxscore = soup.find('section', {'id':'box-score'})
    return boxscore
def getCentreIndex(boxscore):
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
    return index


    
def isCentre(data, df, centre):
    '''determines if play was  centre  or opponent
1 if centre
0 if not

'''
    check_centre = 0
    
    for info in df[centre]:
       info = info.lower()
       if data == info:   
             check_centre = 1
  
    if check_centre == 1:
        return '1'
    else:
        return '0'
   
def makeHeaderPBP(sport, year1):
    '''sport_schedule = open(r'/Users/ellie/Documents/Summer Research 2021/' + sport + '/' + str(year1) + '_links.csv', 'r')
    sport_schedule = open(r'/Users/drewdunn/Desktop/Python code for research/WomenBB_raw_data_by_year' ,'r')

    sport_games = [line.rstrip('\n') for line in sport_schedule]
    sport_schedule.close()'''
    game = 1
    game_url = 'file:///Users/drewdunn/Downloads/centre_mens-basketball_2019-20_3907_greenville%20(9).html'
    print(game_url)
    print(game)
    list_game = game_url.split("/")
    print(list_game)
    ssl._create_default_https_context = ssl._create_unverified_context
    r= urllib.request.urlopen(game_url)
    game_opponent = "Greenville" #change this to get opponent of any game
    game_id = 3907 #^
    boxScoreTab = getBoxScore(game_url)
    centre_index = getCentreIndex(boxScoreTab)

     
    soup = bs(r, 'html.parser')
            
          
    #header = open('/Users/drewdunn/Downloads/centre_mens-basketball_2019-20_3907_greenville.html', 'r')
    header = open('/Users/drewdunn/Downloads/game1_greenville_3907 (1).csv', 'r')
    #assigns first row of the header as list'header_titles' and second row as 'header_info'
    header_data = list(csv.reader(header)) 
    header_titles = header_data[0]
    header_info = header_data[1]
    path = '/Users/drewdunn/Downloads/centre_mens-basketball_2019-20_3907_greenville.html'

    if os.path.exists(path):
        table = open('/Users/drewdunn/Desktop/Python code for research/3907_greenville.csv', 'r')
        pbp = soup.find('section', {'id' : 'play-by-play'})
        centre_column = pbp.find_all('th',{'class':'hide-on-medium-down text-center'})[centre_index].text
        centre_column = centre_column.strip()

        #assigns the first row of the table as list'table_titles'
        table_data = list(csv.reader(table))
        table_titles = table_data[0]

        #puts all titles into a combined list
        all_titles = header_titles
        all_titles.extend(table_titles)

        df = pd.DataFrame(columns = all_titles)
        print(len(table_data))
        #for i in range(0, 10):
            #print(table_data[i])
        print(header_info[:])
        print(len(header_info))
        print(len(all_titles))
        for i in range(1, len(table_data)-1):
            combined = header_info[:]
            combined.extend(table_data[i])
            df.loc[len(df.index)] = combined
            
        print(len(combined))
        print("hi")
        print(i)
                               
             
        official_opponent_name , official_centre_name = getOfficialName(boxScoreTab, sport)

        df.head()
        #loops through the dataFrame.
        #going to use to loop through play data to create a new column
        #called type.
        Type = []
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
                                'steal', 'assist', 'layup', 'block ','sub']
              
                
        for data in df['Play']:
            data = data.lower()
            player_added = False
            for play_type in type_of_plays:
                player_name = getPlayer(play_type, data)
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
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
            elif 'dunk by' in data:
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
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)       
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
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
                            
            elif 'assist ' in data:
                Type.append('assist')
                if player_added == False:
                    player.append('')
                Outcome.append('')
                points.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
                        
            elif 'ft by ' in data:
                if player_added == False:
                    player.append('')
                Type.append('free throw')
                if 'good ft by ' in data:
                    Outcome.append('good')
                    points.append('1')
                elif 'miss ft by ' in data:
                    Outcome.append('missed')
                    points.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
                            
            elif "2ptr by " in data:
                if player_added == False:
                    player.append('')
                Type.append('two pointer')
                if 'good ' in data:
                    Outcome.append('good')
                    points.append('2')
                elif 'miss ' in data:
                    Outcome.append('miss')
                    points.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
                        
            elif 'foul ' in data:
                if player_added == False:
                    player.append('')
                Type.append('foul')
                Outcome.append('')
                points.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
            elif 'turnover ' in data:
                if player_added == False:
                    player.append('')
                Type.append('turnover')
                Outcome.append('')
                points.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
            elif 'steal ' in data:
                if player_added == False:
                    player.append('')
                Type.append('steal')
                Outcome.append('')
                points.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
            elif 'rebound ' in data:
                if player_added == False:
                    player.append('')
                Outcome.append('')
                points.append('')
                if 'def by ' in data:
                    Type.append('defensive rebound')
                elif 'deadb by ' in data:
                    Type.append('deadball rebound')
                            
                elif 'off by ' in data:
                    Type.append('offensive rebound')
                            
                else:
                    Type.append('')

                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
                            
            elif 'sub ' in data:
                if ' in ' in data:
                    Type.append('subbing in')
                elif ' out ' in data:
                    Type.append('subbing out')
                elif ' starter ' in data:
                    Type.append('starter')
                Outcome.append('')
                points.append('')
                if player_added == False:
                    player.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
            elif 'block ' in data:
                Type.append('block')
                Outcome.append('')
                points.append('')
                if player_added == False:
                    player.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
            elif '3ptr by' in data:
                Type.append('three pointer')
                if 'miss ' in data:
                    Outcome.append('missed')
                    points.append('')
                elif 'good ' in data:
                    Outcome.append('good')
                    points.append('3')

                if player_added == False:
                    player.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
            elif 'timeout' in data:
                Type.append('timeout')
                Outcome.append('')
                points.append('')
                if player_added == False:
                    player.append('')
                if isCentre(data, df, centre_column) == '1':
                    Team.append('Centre')
                else:
                    Team.append(official_opponent_name)
            else:
                Type.append('')
                Outcome.append('')
                points.append('')
                Team.append('')
                if player_added == False:
                    player.append('')
        
        count = 0
        subData = ['subbing in', 'subbing out']            
        for i in range(0, len(Type)):
            if Type[i] in subData:
                count = count + 1
        for i in range(0, len(sl)):
            sl[i] = sl[i].lower()
        print(sl)
        print(count)
        sl0 = sl[0]
        sl1 = sl[1]
        sl2 = sl[2]
        sl3 = sl[3]
        sl4 = sl[4]
            
        player1 = []
        player2 = []
        player3 = []
        player4 = []
        player5 = []
        print(len(table_data))
        count1 = 0
        count2 = 0
        time_in_secs = []
        for time in df['Time Remaining']:
            if time != '--' and 'Start' not in time:
                minutes = int(time.split(':')[0])
                seconds = int(time.split(':')[1])
                total_seconds = minutes * 60 + seconds
                time_in_secs.append(total_seconds)
            elif time == 'Start Period 2':
                time_in_secs.append('*')
            else:
                time_in_secs.append('')
        for i in range(0, len(table_data)-2):
            if Type[i] == 'subbing in' and Team[i] == 'Centre':
                sl.append(player[i])
                player1.append("")
                player2.append("")
                player3.append("")
                player4.append("")
                player5.append("")
                count1 = count1 + 1
            elif Type[i] == 'subbing out' and Team[i] == 'Centre':
                sl.remove(player[i])
                player1.append("")
                player2.append("")
                player3.append("")
                player4.append("")
                player5.append("")
                count2 = count2 +1
                print(i)
            elif time_in_secs[i] == '*':
                sl.clear()
                sl.append(sl0)
                sl.append(sl1)
                sl.append(sl2)
                sl.append(sl3)
                sl.append(sl4)
            else:
                player1.append(sl[0])
                player2.append(sl[1])
                player3.append(sl[2])
                player4.append(sl[3])
                player5.append(sl[4])
        print(sl)
        player1.append(sl[0])
        player2.append(sl[1])
        player3.append(sl[2])
        player4.append(sl[3])
        player5.append(sl[4])
        '''Idea:
        on plays where there are subs make players empty strings and then continously
        update list and when subs are over players columns become actual players again'''

              #EDIT!!!!!!!!!!!!          
                    
                    
                   
        df['Play Type'] = Type
        df['Shot Outcome'] = Outcome
        df['Team']= Team
        df['Player'] = player
        df['Points Earned'] = points
        df['player1'] = player1
        df['player2'] = player2
        df['player3'] = player3
        df['player4'] = player4
        df['player5'] = player5
        

        
        
        df['Time(seconds)'] = time_in_secs

        output_file = 'game'+str(game)+'_1'+game_opponent+'_'+str(game_id)+'.csv'
        output_dir = Path('/Users/drewdunn/Desktop/Python code for research/Lineup')
        output_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_dir / output_file)
        print('game'+str(game)+'_1'+game_opponent+'_'+str(game_id)+'.csv')       
          
    else:
        print("Play by play does not exist for that game, but a header does")
    return sl            
    
    
        
            
 
 
  
 
def main():
    getTable()
    makeHeaderPBP('mens-basketball', 2019)
    
'''
sports = ['baseball', 'mens-basketball', 'football', 'mens-lacrosse',
    'mens-soccer', 'mens-tennis', 'womens-basketball',
          'field-hockey', 'womens-lacrosse', 'womens-soccer', 'softball', 'womens-tennis', 'womens-volleyball']
  
    multi_year_sports = ['mens-basketball', 'womens-basketball', 'mens-tennis', 'womens-tennis']
 
    fall_sports = ['mens-basketball', 'football', 'mens-soccer', 'womens-basketball', 'field-hockey', 'womens-soccer', 'womens-volleyball']
    for sport in sports:
        if sport == 'mens-tennis' or sport == 'womens-tennis':
            year1 = 2018
        elif sport in fall_sports:
            year1 = 2010
        else:
            year1 = 2011
 '''
'''
    sports = ['mens-soccer','womens-soccer']
    
    for sport in sports:
        while year1 != 2022:
            #year2 = year1 + 1
            #if sport in multi_year_sports:
                #years = str(year1) + '-' + str(year2)
            #else:
                #years = year1
            makeHeaders(sport,year1)
            year1 += 1
 
'''
main()
