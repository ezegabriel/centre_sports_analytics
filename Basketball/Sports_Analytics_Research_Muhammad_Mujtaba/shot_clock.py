import csv
import pandas as pd
from collections import Counter
import os

def add_clock(file_path, new_file_path):
    #File path C:/Users/sheik/Downloads/game24_rhodes_2263.csv'
    df = pd.read_csv(file_path, usecols = ["Play Type", "Shot Outcome", "Team", "Time(seconds)"])
    #print(df)
    #os.remove("C:/Users/sheik/Downloads/testing.csv")
    play_list = df['Play Type'].tolist()
    outcome_list = df['Shot Outcome'].tolist()
    team_list = df['Team'].tolist()
    time_list  = df['Time(seconds)'].tolist()

    print(Counter(play_list))

    if time_list[2]>600: 
        half_time = 1200
    else:
        half_time = 600
    shot_clock = half_time
    sc_list = []
    current_clock = 30
    sc_list.append(30)
    sc_reset_list = ["steal", "turnover", "three pointer", "jumper", "layup", "foul"]
    not_reset_list = ['subbing in', 'subbing out', 'timeout', 'block']
    #loop through the times
    for i in range(1,len(time_list)-2):
        #if time is nan then append nan
        if pd.isna(time_list[i]):
            sc_list.append(time_list[0])
        #if the current time and time before are same then append the current shot clock
        elif time_list[i] == time_list[i-1] and time_list[i]>30:
            sc_list.append(current_clock)
        #if time is 0 then append 0
        elif(time_list[i] == 0):
            shot_clock = half_time
            sc_list.append(0)
        #if time is less than 30s then time is equal to shot clock
        elif(time_list[i] <=30):
            sc_list.append(time_list[i])
        elif play_list[i] in not_reset_list:
            current_clock = current_clock - (shot_clock-time_list[i])
            shot_clock = time_list[i]
            sc_list.append(current_clock)
        else:
            if play_list[i] in sc_reset_list:
                if play_list[i+1] == "block" and play_list[i+2] == "offensive rebound":
                    current_clock = current_clock - (shot_clock-time_list[i])
                    shot_clock = time_list[i]
                    sc_list.append(current_clock)
                elif (current_clock-(shot_clock-time_list[i]) < 0):
                    current_clock = 30 + (current_clock-(shot_clock-time_list[i]))
                    shot_clock = time_list[i]
                    sc_list.append(current_clock)
                    current_clock = 30
                else:
                    current_clock = current_clock-(shot_clock-time_list[i])
                    shot_clock = time_list[i]
                    sc_list.append(current_clock)
                    current_clock = 30
            else:
                sc_list.append(30)
    sc_list.append(time_list[len(time_list)-2])
    sc_list.append(time_list[len(time_list)-1])
    #print(sc_list)
    
    #d= {"shot clock": sc_list}
    df['Shot Clock'] = sc_list
    #print(df)


    df.to_csv (new_file_path, index = False, header=True)

#70,71,72
def main():
    for i in range(1,11):
        year = 2010+i
        directory = r"C:\Users\sheik\OneDrive\Desktop\Code_files\Sports_Analytics_Research\data\all_data"+"\\"+str(year)
        for filename in os.listdir(directory):
            filepath =  directory+"\\"+filename
            new_file_path = r"C:\Users\sheik\OneDrive\Desktop\Code_files\Sports_Analytics_Research\data\all_clock"+"\\"+filename
            add_clock(filepath, new_file_path)

if __name__ == "__main__":
    main()
