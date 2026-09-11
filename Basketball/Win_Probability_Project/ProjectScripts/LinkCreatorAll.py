import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from pandas import DataFrame
import os
import shutil
import glob

# These were the sports that had box scores on their schedule pages.
# Not all sports would have them, such as track and field, cheer, etc.
sports = ['baseball', 'mens-basketball', 'football', 'mens-lacrosse', 'mens-soccer', 'mens-tennis', 'womens-basketball', 
          'field-hockey', 'womens-lacrosse', 'womens-soccer', 'softball', 'womens-tennis', 'womens-volleyball']
sports = ['mens-basketball', 'womens-basketball']
# league_sports = ['baseball', 'mens-basketball', 'football', 'mens-lacrosse', 'mens-soccer', 'mens-tennis', 'womens-basketball', 
#           'field-hockey', 'womens-lacrosse', 'womens-soccer', 'softball', 'womens-tennis', 'womens-volleyball']

multi_year_sports = ['mens-basketball', 'womens-basketball', 'mens-tennis', 'womens-tennis']

fall_sports = ['mens-basketball', 'football', 'mens-soccer', 'womens-basketball', 'field-hockey', 'womens-soccer', 'womens-volleyball']

schools = ['berryvikings', 'bscsports', 'centrecolonels', 'hendrixwarriors', 'gomajors', 'rhodeslynx', 'sewaneetigers']
# schools = ['centrecolonels']

for school in schools:
    if school != 'bscsports':
        base_path = 'https://' + school + '.com'
    else:
        base_path = 'https://' + school + '.net'
    print(base_path)
    # if school == 'gopetrels':
    #     sports = ['bsb', 'mbkb', 'football', 'mlax', 'msoc', 'mten', 'wbkb', 'field-hockey', 'wlax', 'wsoc', 'softball', 'wten', 'wvball']

    for ind, sport in enumerate(sports):
        if sport == 'mens-tennis' or sport == 'womens-tennis':
            year = 2018
        elif sport in fall_sports:
            year = 2010
        else:
            year = 2011

        main_dir = '/Users/ericmerdian/Desktop/Desktop/A_Summer_Research/AllTeams/'

        present_dir = main_dir + school + '/' + str(sport)
        school_dir = main_dir + school

        if not os.path.exists(school_dir):
            os.mkdir(school_dir)

        if not os.path.exists(present_dir):
            os.mkdir(present_dir)

        while year != 2022:
            if sport in multi_year_sports:
                if year == 2021:
                    url = base_path + '/sports/' + str(sport) + '/schedule/'
                else:
                    next_year = year + 1
                    year_ext = str(next_year)[-2:]
                    url = base_path + '/sports/' + str(sport) + '/schedule/' + str(year) + '-' + year_ext
                    print( url)
            else:
                if year == 2021:
                    url = base_path + '/sports/' + str(sport) + '/schedule/'
                else:
                    url = base_path + '/sports/' + str(sport) + '/schedule/' + str(year)
            # if school == 'gopetrels':
            #     next_year = year + 1
            #     year_ext = str(next_year)[-2:]
            #     url = base_path + '/sports/' + str(sport) + '/' + str(year) + '-' + year_ext + '/schedule/' 

            print(url)
            r = requests.get(url)

            # Convert to a BS object
            soup = bs(r.content, features='lxml')

            # Print out html
            # print(soup.prettify())

            links = []
            if school != 'gopetrels':
                for li in soup.find_all(class_="sidearm-schedule-game-links-boxscore"):
                    links.append(li.a.get('href'))
            else:
                for li in soup.find_all(class_="links"):
                    # print(li)
                    links.append(li.a[1].get('href'))

            # print(links)


            full_link_list = []

            for index, link in enumerate(links):
                full_path = base_path + link
                
                full_link_list.append(full_path)

            #This gets rid of double links, escept for Burmingham Southern, who didn't have duplicates
            if school != 'bscsports':
                full_link_list = full_link_list[::2]

            #print(full_link_list)

            df = DataFrame (full_link_list, columns=['Links'])

            print(df)

            df.to_csv(r'/Users/ericmerdian/Desktop/Desktop/A_Summer_Research/AllTeams/' + school + '/' + str(sport) + '/' + str(year) + '_links.csv', 
                index = False, header=False)

            year = year + 1

        # After all the links have been put in for each year's file, we can then cobine them into a merged file 

        # allFiles = glob.glob(present_dir + "/*.csv")
        # allFiles.sort()
        # os.chdir(present_dir)
        # with open('merged' + sport + '.csv', 'wb') as outfile:
        #     for i, fname in enumerate(allFiles):
        #         with open(fname, 'rb') as infile:
        #             shutil.copyfileobj(infile, outfile)
        #             print(fname + " has been imported.")

        # if not os.path.exists(present_dir + '/HTML'):
        #     os.mkdir(present_dir + '/HTML')
        # if not os.path.exists(present_dir + '/Tables'):
        #     os.mkdir(present_dir + '/Tables')
        year = 2010

