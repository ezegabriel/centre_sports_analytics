import csv
#import pandas as pd
from collections import Counter
import os

def combine(p_l, out_l, c_l, te, ti, file_path):
    shots = ['jumper', 'three pointer', 'layup']
    df = pd.read_csv(file_path, usecols = ["Play Type", "Shot Outcome", "Shot Clock", "Time(seconds)", "Team"])
    play_list = df['Play Type'].tolist()
    outcome_list = df['Shot Outcome'].tolist()
    clock_list = df['Shot Clock'].tolist()
    team = df['Team'].tolist()
    time = df['Time(seconds)'].tolist()

    for i,play in enumerate(play_list):
        if play in shots:
            p_l.append(play)
            out_l.append(outcome_list[i])
            c_l.append(clock_list[i])
            te.append(team[i])
            ti.append(time[i])
            
    
#C:\Users\sheik\OneDrive\Desktop\Code_files\Sports_Analytics_Research-DESKTOP-7CNE082\data\all_clock            

def main():
    execute()

def execute():
    directory = r"C:\Users\HP\OneDrive\Desktop\Summer Research\Basketball\Sports_Analytics_Research_Muhammad_Mujtaba\data"
    play_l = []
    outcome_l = []
    clock_l = []
    team_l = []
    time_l = []
    for filename in os.listdir(directory):
        #print(filename)
        file_path =  directory+"\\"+filename
        combine(play_l, outcome_l, clock_l, team_l, time_l, file_path)
        
    df = pd.DataFrame(list(zip(play_l, outcome_l, clock_l, team_l, time_l)), columns =["Play Type", "Shot Outcome", "Shot Clock", "Team", "Time(seconds)"])

    df.to_csv (r"C:\Users\sheik\OneDrive\Desktop\Code_files\Sports_Analytics_Research-DESKTOP-7CNE082\data\all_combined.csv", index = False, header=True)

if __name__ == "__main__":
    main()
