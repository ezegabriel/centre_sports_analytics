import csv
import pandas as pd
from collections import Counter
import os

def get_df(file_path):
    df = pd.read_csv(file_path, usecols = ["Play Type", "Shot Outcome", "Shot Clock"])
    play_list = df['Play Type'].tolist()
    outcome_list = df['Shot Outcome'].tolist()
    clock_list = df['Shot Clock'].tolist()

    return play_list, outcome_list, clock_list
    

def sc_two(p_l, o_l, c_l):
    d = {}
    for i in range(30):
        d[i] = []
    twos = ["jumper", "layup"]
    for i, p in enumerate(p_l):
        if p in twos:
            if c_l[i] in d:
                if o_l[i] == "good":
                    d[c_l[i]].append(1)
                else:
                    d[c_l[i]].append(0)        
    for key in d.keys():
        total = sum(d[key])
        if len(d[key]) > 0:
            n = len(d[key])
            percentage = total/n
            d[key] = percentage
        else:
            d[key] = 0
    
    return d

def sc_three(p_l, o_l, c_l):
    d = {}
    for i in range(30):
        d[i] = []
    three = ["three pointer"]
    for i, p in enumerate(p_l):
        if p in three:
            if c_l[i] in d:
                if o_l[i] == "good":
                    d[c_l[i]].append(1)
                else:
                    d[c_l[i]].append(0)        
    for key in d.keys():
        total = sum(d[key])
        if len(d[key]) > 0:
            n = len(d[key])
            percentage = total/n
            d[key] = percentage
        else:
            d[key] = 0
    
    return d

def per_three(p_l, o_l, c_l):
    d = {}
    for i in range(30):
        d[i] = []
    three = ["three pointer"]
    for i, p in enumerate(p_l):
        if p in three:
            if c_l[i] in d:
                d[c_l[i]].append(1)
        else:
            if c_l[i] in d:
                d[c_l[i]].append(0) 
                        
    for key in d.keys():
        total = sum(d[key])
        if len(d[key]) > 0:
            n = len(d[key])
            percentage = total/n
            d[key] = percentage
        else:
            d[key] = 0
    
    return d

def points_per_shot(p_l, o_l, c_l):
    d = {}
    for i in range(30):
        d[i] = []
    three = ["three pointer"]
    for i, p in enumerate(p_l):
        if p in three:
            if c_l[i] in d:
                if o_l[i] == "good":
                    d[c_l[i]].append(3)
                else:
                    d[c_l[i]].append(0)
        else:
            if c_l[i] in d:
                if o_l[i] == "good":
                    d[c_l[i]].append(2)
                else:
                    d[c_l[i]].append(0)
            
    for key in d.keys():
        total = sum(d[key])
        if len(d[key]) > 0:
            n = len(d[key])
            percentage = total/n
            d[key] = percentage
        else:
            d[key] = 0

    return d
        
        
    
            

def d_to_arr(d):
    keys = []
    data = []
    for key in d.keys():
        percentage = d[key]
        keys.append(key)
        data.append(percentage)
    return keys, data 
    
def main():
    file_path = r"C:\Users\sheik\OneDrive\Desktop\Code_files\Sports_Analytics_Research-DESKTOP-7CNE082\data\all_combined.csv"
    p_l, o_l, c_l = get_df(file_path)
    two_d = sc_two(p_l, o_l, c_l)
    #print(two_d)
    three_d = sc_three(p_l, o_l, c_l)
    #print(three_d)
    per_three_d = per_three(p_l, o_l, c_l)
    print(per_three_d)
    pps_d = points_per_shot(p_l, o_l, c_l)
    print(pps_d)

    shot_clock, two_per = d_to_arr(two_d)
    shot_clock, three_per = d_to_arr(three_d)
    shot_clock, per_three_tot = d_to_arr(per_three_d)
    shot_clock, pps_total = d_to_arr(pps_d)

    df = pd.DataFrame(list(zip(shot_clock, two_per, three_per, per_three_tot, pps_total)), columns =['Shot Clock', '2pt made', '3pt made', 'percentage 3pt', 'points per shot'])

    
    df.to_csv (r"C:\Users\sheik\OneDrive\Desktop\Code_files\Sports_Analytics_Research-DESKTOP-7CNE082\data\vis_data.csv", index = False, header=True)

    
if __name__ == "__main__":
    main()
