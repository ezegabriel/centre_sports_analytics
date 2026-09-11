import csv
import pandas as pd
from collections import Counter
import os

def clock_shots(file_path):
    d = {}
    #intialize dictionary
    for i in range(31):
        d[i] = []
    shots = ['free throw', 'jumper', 'three pointer', 'layup']
    df = pd.read_csv(file_path, usecols = ["Play Type", "Shot Outcome", "Shot Clock"])
    play_list = df['Play Type'].tolist()
    outcome_list = df['Shot Outcome'].tolist()
    clock_list = df['Shot Clock'].tolist()

    for i in range(len(play_list)):
        
        if play_list[i] in shots:
            if clock_list[i] in d:
                if outcome_list[i] == "good":
                    d[clock_list[i]].append(1)
                else:
                    d[clock_list[i]].append(0)
            else:
                print(clock_list[i])
    for key in d.keys():
        total = sum(d[key])
        if len(d[key]) > 0:
            n = len(d[key])
            percentage = total/n
            d[key] = [percentage, n]
        else:
            d[key] = [0,0]
        
    return d
    
def d_to_arr(d):
    keys = []
    data = []
    for key in d.keys():
        percentage = d[key][0]
        keys.append(key)
        data.append(percentage)
    return keys, data
        
    

def execute():
    directory = r"C:\Users\sheik\OneDrive\Desktop\Code_files\Sports_Analytics_Research\data\all_clock"
   # _percentage
    d_p = {}
    for i in range(31):
        d_p[i] = [0,0]
    for filename in os.listdir(directory):
        print(filename)
        file_path =  directory+"\\"+filename
        shots_data = clock_shots(file_path)
        print(shots_data)
        for key in shots_data.keys():
            if d_p[key][1]+shots_data[key][1] == 0:
                d_p[key][0] = d_p[key][0]
            else:
                d_p[key][0] = ((d_p[key][0]*d_p[key][1])+shots_data[key][0]*shots_data[key][1])/(d_p[key][1]+shots_data[key][1])
                d_p[key][1] += shots_data[key][1]
    col1, col2 = d_to_arr(d_p)

    df = pd.DataFrame(list(zip(col1, col2)), columns =['Shot Clock', 'Shot Percentage'])
    print(df)
    
    df.to_csv (r"C:\Users\sheik\OneDrive\Desktop\Code_files\Sports_Analytics_Research\data\shot_percentage_running.csv", index = False, header=True)

    


def main():
    execute()




if __name__ == "__main__":
    main()
