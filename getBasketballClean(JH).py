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

# Main directory to Summer Research folder
main_dir = '/Users/HP/.spyder-py3/Summer_Research/'
#sports = ['mens-basketball', 'womens-basketball']

# Temporary variable; should loop through all sports
sports = ['mens-basketball']


saa_teams = ['berry', 'birmingham-southern', 'centre', 'hendrix', 'millsaps', 'oglethorpe', 'rhodes', 'sewanee']
schools = ['berryvikings', 'bscsports', 'centrecolonels', 'hendrixwarriors', 'gomajors', 'rhodeslynx', 'sewaneetigers']
# Temporary variable; should loop through all schools
schools = ['centrecolonels']

start_year = 2022  # fall of first year to get header data
end_year = 2022  # fall of last year to get header data


def getOfficialName(boxscore):
    headline=[]
    graphic = boxscore.find('div', {'class':'box-score-graphic'})
 
    away_team = graphic.find('div', {'class':'team away'})
    away_logo = away_team.find('img')
    home_team = graphic.find('div',{'class':'team home'})
    home_logo= home_team.find('img')
    headline.append(away_logo.attrs['alt'])
    headline.append(home_logo.attrs['alt'])
    print(headline)
    centre_index, headline_lower = getCentreIndex(boxscore)
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
    
    if not opponent_name in headline_lower[0]:
        s_name_temp = opponent_name
        opponent_name = centre_name
        centre_name = s_name_temp
        
    print(opponent_name, centre_name, "say my nameee")
    print()
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
    headline=[]
    away_team = boxscore.find('div', {'class':'team away'})
    away_logo = away_team.find('img')
    home_team = boxscore.find('div',{'class':'team home'})
    home_logo= home_team.find('img')
    
    headline.append(away_logo.attrs['alt'].lower())
    headline.append(home_logo.attrs['alt'].lower())
    print(headline, "omo i jusr deyy here")
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
    #print(header_files)
    
    for header_file in header_files: # Loop through every csv files from the list
        #print(header_file)
        #print(header_file.split("_header"))
        
        # Open the csv files from the header directory for reading
        header_file_h = open(header_dir + header_file, 'r')
        #print(header_dir)
        print(header_file)
        print()
        
        header_data = list(csv.reader(header_file_h))
        #print(header_data)
 
        #ssl._create_default_https_context = ssl._create_unverified_context
        #r= urllib.request.urlopen(game_url)
        #game_opponent = list_game[7]
        #game_id= list_game[9]
        
        html_file = html_dir + header_file.split('_header')[0] + '.html'
        html_file_h = open(html_file, 'r')
        soup = bs(html_file_h, 'lxml')
        #soup = bs(r, 'html.parser')

        player_tables = soup.find_all('table',{'class':'sidearm-table overall-stats full hide-caption highlight-hover highlight-column-hover'})
        away_starters = get_starters(player_tables[0])
        home_starters = get_starters(player_tables[1])

        boxscore = soup.find('section', {'id':'box-score'})
        
        centre_index, headline_temp = getCentreIndex(boxscore)

        #assigns first row of the header as list'header_titles' and second row as 'header_info'
        header_titles = header_data[0]
        header_info = header_data[1]

        table_file = header_file.replace('header', 'table')
        table_file_h = table_dir + table_file
        try:
            table = open(table_file_h, 'r')
        except FileNotFoundError:
            continue
        
        pbp = soup.find('section', {'id' : 'play-by-play'})
        centre_column = pbp.find_all('th',{'class':'hide-on-medium-down text-center'})[centre_index].text
        centre_column = centre_column.strip()
        centre_column = "home_play"
        #assigns the first row of the table as list'table_titles'
        table_data = list(csv.reader(table))
        table_titles = table_data[0]
        table_titles[1], table_titles[5] = "away_play", "home_play"
        #print(table_titles)
        print()
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
        # print("Away Lineup", away_lineup)
        # print("Home Lineup", home_lineup)
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
                        'steal', 'assist', 'layup', 'block ','sub']
        
        i = 0
        skip_line = 0 # Sets boolean to check order of substituition
        for data in df['Play']:
            data = data.lower()
            player_added = False
            for play_type in type_of_plays:
                player_name = getPlayer(play_type, data)
                player_name = player_name.replace(" ", "")
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
                if data == df['home_play'][i].lower():
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
                if data == df['home_play'][i].lower():
                    #Team.append('Centre')
                    Team.append(home_name)
                else:
                    #Team.append(official_opponent_name)
                    Team.append(away_name)
            elif 'assist ' in data:
                Type.append('assist')
                if player_added == False:
                    player.append('')
                Outcome.append('')
                points.append('')
                #if isHome(data, df) == '1':
                if data == df['home_play'][i].lower():
                    #Team.append('Centre')
                    Team.append(home_name)
                else:
                    #Team.append(official_opponent_name)
                    Team.append(away_name)
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
                #if isHome(data, df) == '1':
                if data == df['home_play'][i].lower():
                    #Team.append('Centre')
                    Team.append(home_name)
                else:
                    #Team.append(official_opponent_name)
                    Team.append(away_name)
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
                #if isHome(data, df) == '1':
                if data == df['home_play'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
                
            elif 'foul ' in data:
                if player_added == False:
                    player.append('')
                Type.append('foul')
                Outcome.append('')
                points.append('')
                #if isHome(data, df) == '1':
                if data == df['home_play'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
            elif 'turnover ' in data:
                if player_added == False:
                    player.append('')
                Type.append('turnover')
                Outcome.append('')
                points.append('')
                #if isHome(data, df) == '1':
                if data == df['home_play'][i].lower():
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
                if data == df['home_play'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
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

                #if isHome(data, df) == '1':
                if data == df['home_play'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
                    
            elif 'sub ' in data:
                if ' out ' in data:
                    Type.append("subbing out")
                    if skip_line == 0: # Run this block of command if there's a correct order of substituition
                        if (player_name in home_lineup) or (player_name in away_lineup):
                            # if player_name in home_lineup:
                            #     print(home_lineup.index(player_name))
                            #     print("hey1")
                            # if player_name in away_lineup:
                            #     print(away_lineup.index(player_name))
                            #     print("hey2")
                            
                            if data == df["home_play"][i].lower():
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
                    
                elif " in " in data:
                    Type.append("subbing in")
                    if skip_line == 0: # Run this block of command if there's a correct order of substituition: 
                        if not (player_name in home_lineup or player_name in away_lineup): 
                            if data == df["home_play"][i].lower():
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
                
                    
                elif ' starter ' in data:
                    Type.append('starter')
                Outcome.append('')
                points.append('')
                if player_added == False:
                    player.append('')
                #if isHome(data, df) == '1':
                if data == df['home_play'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
            elif 'block ' in data:
                Type.append('block')
                Outcome.append('')
                points.append('')
                if player_added == False:
                    player.append('')
                #if isHome(data, df) == '1':
                if data == df['home_play'][i].lower():
                    Team.append(home_name)
                else:
                    Team.append(away_name)
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
                #if isHome(data, df) == '1':
                if data == df['home_play'][i].lower():
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
                if data == df['home_play'][i].lower():
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
            
        # index, i_count = 0, 0
        # while i_count != len(l_away_lineup):
        #     if l_away_lineup[index] == l_away_lineup[index + 1]:
        #         del l_away_lineup [index]
        #         i_count += 1
        # print(l_away_lineup)
            #print(l_away_lineup)
        #if header_files.index(header_file) == 0:
            #print(l_away_lineup)
        # if header_files.index(header_file) == 0:
        #     for num in range(5):
        #         test.append("")
        #         bt.append("")
        # l_away_lineup.append(test)
        # l_home_lineup.append(bt)
        
        
        #EDIT!!!!!!!!!!!!          
                            
        df['Play Type'] = Type
        df['Shot Outcome'] = Outcome
        #print(Outcome, Team)
        df['Team']= Team
        df['Player'] = player
        df['Points Earned'] = points
        df["Away Lineup"] = l_away_lineup
        df["Home Lineup"] = l_home_lineup
        
        time_in_secs = []
        for time in df['Time Remaining']:
            if time != '--' and 'Start' not in time:
                minutes = int(time.split(':')[0])
                seconds = int(time.split(':')[1])
                total_seconds = minutes * 60 + seconds
                time_in_secs.append(total_seconds)
                    
            else:
                time_in_secs.append('')
        df['Time(seconds)'] = time_in_secs

        pbp_file = pbp_dir + header_file.replace('header', 'pbp')
        df.to_csv(pbp_file)
        
        '''
        Getting the lineups for modificiations during every event through the game
        This would help extract and manipulate useful data from the play - by - play
        The Goal is acheived by creating a dataframe with all starters
        then exporting it as a csv file
        
        '''
        # # Returns the initial starters for both teams as lists
        # a, b = get_starters(player_tables[0]), get_starters(player_tables[1]) 
        
        # # Initialize variables to help create the data frame               
        # p_data, l_list, a_str, b_str = [], [], "", ""
        
        # # Check which team plays on home turf, to keep the corelation of team names against lineups
        # if centre_index == 1: # Refers to the function getCentreIndex
        #     l_list.append(away_name + " v " + home_name)
        # else: # Switch order in which team names appear
        #     l_list.append(home_name + " v " + away_name)
        
        # # Length of list a & b are the same
        # for index in range(len(a)): # Index refering to every starter on the list
        #     a_str += a[index] + ";" + " "
        #     b_str += b[index] + ";" + " "
            
        # # Removes the extra space and semi - colon at the end    
        # l_list.append(a_str[: len(a_str) - 2])
        # l_list.append(b_str[: len(b_str) - 2])
        
        # p_data.append(l_list) # Creates a double list to ensure the record of one row per parsed file
        # print(p_data)
        
        # lineup = pd.DataFrame(p_data, columns = ["Game", "Away Lineup", "Home Lineup"])
        
        # if header_files.index(header_file) == 0: # Overwrite the dataframe to a new csv file for the first html file
        #      lineup.to_csv("C:/Users/HP/.spyder-py3/Summer_Research/tentative_lineup.csv", index = False)
        # else: # Append the remaining dataframe to the existing csv file
        #      lineup.to_csv("C:/Users/HP/.spyder-py3/Summer_Research/tentative_lineup.csv", mode = "a", index = False, header = False)
             
def main(schools, sports, start_year, end_year):
    for sport in sports: 
        for school in schools:
            year = start_year
            while year <= end_year:
                year_str = str(year) + '-' + str(year-2000+1)
                makeHeaderPBP(sport, school, year_str)
                year += 1
    #print(sports)
main(schools, sports, start_year, end_year)

