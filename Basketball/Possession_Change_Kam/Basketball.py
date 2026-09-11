# Kam Kiesel
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import csv

def main():
     # C:\Users\Kameron.DESKTOP-9OMTKVA\Desktop\FallResearch - File path
     fullData = pd.read_excel(r'C:\Users\Kameron.DESKTOP-9OMTKVA\Desktop\FallResearch\Hendrix.xlsx', converters = {'Team':str})
     data = pd.read_excel(r'C:\Users\Kameron.DESKTOP-9OMTKVA\Desktop\FallResearch\Hendrix.xlsx', usecols = ['Play Type', 'Team', 'Time(seconds)', 'opponent name', 'Points Earned'])
     data = data.fillna(0)
     
     # Creation of Lists
     playData = data['Play Type'].tolist()
     teamName = data['Team'].tolist()
     opponentName = data['opponent name'].tolist()
     points = data['Points Earned'].tolist()
     gameClock = data['Time(seconds)'].tolist()
     gameClock[0] = 1200
     playOutcome = list(zip(playData,teamName,gameClock))
     limit = len(playOutcome) - 2
     possessionChange = []
     possessionCentre = []
     possessionClock = []
     possessionOpp = []
     extraData = ['timeout', 'foul', 'deadball rebound', 'free throw', 'offensive rebound']
     subData = ['subbing in', 'subbing out']
     possessionChange.append(np.nan)
     possessionClock.append(np.nan)

     # Check Possession Change
     i = 1
     while i <= limit:
          #print(i, teamName[i], playData[i])
          if teamName[i] == teamName[i+1] and playData[i] not in subData and playData[i] != 'turnover':
               possessionChange.append(' ') # No change in possession
               i += 1
          elif type(playData[i]) == float: # Start of halves are float
               possessionChange.append(' ') # No change in beginning of halves
               i += 1
          elif playData[i] in extraData and playData[i-1] != 'free throw': # Timeouts, fouls, first free throws, and offensive rebounds do not change possession
               possessionChange.append(' ')
               i += 1
          elif playData[i] in subData or playData[i-1] in subData: # Subbing in/out does not change possession     
               if playData[i] in subData: # If play type is a sub
                    possessionChange.append('SUB')
                    i += 1
               else: # If play before is a sub
                    j = i + 1
                    if playData[j-1] in subData: # While the previous play was a sub
                         j -= 1 # Check previous play
                         print(j, i)
                         if teamName[j-1] != teamName[i-1] and playData[i] not in subData: # Team before sub and current are different
                              possessionChange.append('X')
                              i += 1
                         else: # Team before and after are same
                              possessionChange.append(' ')
                              i += 1
                    else: #playData[j] not in subData:
                         #possessionChange.append('HERE')
                         print(j, teamName[j], i, teamName[i])
                         i += 1
                         if teamName[i] == 'Centre':
                              possessionChange.append('Centre')
                              possessionOpp.append('O')
                         else:
                              possessionChange.append('Hendrix')
                              possessionCentre.append('X')
          elif playData[i] == 'turnover' and playData[i-1] not in subData:
               possessionChange.append('X')
               i += 1
               if teamName[i] == 'Centre': # Centre's possession
                    possessionCentre.append('X')
               else: # Opponent's possession
                    possessionOpp.append('O')
          else:
               possessionChange.append('X') # Change in possession
               i += 1
               if playData[i] != 'foul':
                    if teamName[i] == 'Centre': # Centre's possession
                         possessionCentre.append('X')
                    else: # Opponent's possession
                         possessionOpp.append('O')

     possessionChange.append(np.nan)

     # Total Possession / Home & Opponent Possession
     ballCentre = len(possessionCentre)
     ballOpp = len(possessionOpp)
     totalChanges = ballCentre + ballOpp
     percentCentre = (ballCentre/totalChanges) * 100
     percentCentre = '{:.2f}'.format(percentCentre)
     percentOpp = (ballOpp/totalChanges) * 100
     percentOpp = '{:.2f}'.format(percentOpp)

     print('Centre',ballCentre)
     print('Opponent',ballOpp)
     print(abs(ballCentre) - abs(ballOpp)) # Difference in possessions # Should be ~4, at 16

     # Time of Possession
     i = 1
     while i <= limit:
          if playData[i] == 0:
               gameClock[i] = 1200
               i += 1
          else:
               i += 1
               
     i = 1
     while i <= limit:
          while gameClock[i] == 0:
               gameClock[i] = gameClock[i-1]
          else:
               if (gameClock[i] - gameClock[i-1]) > 30:
                    possessionClock.append(1200 - gameClock[i])
                    i += 1
               elif 'X' in possessionChange and gameClock[i] != 0 and gameClock[i] != gameClock[i-1]:
                    timeOfPossession = gameClock[i] - gameClock[i-1]
                    timeOfPossession = abs(timeOfPossession)
                    possessionClock.append(timeOfPossession)
                    i += 1
               else:
                    possessionClock.append(np.nan)
                    i += 1

     possessionClock.append(np.nan)
     possessionClock = [0 if math.isnan(x) else x for x in possessionClock]
     
     i = 1
     centreTOP = []
     oppTOP = []
     totalTimeCentre = 0
     totalTimeOpp = 0

     while i <= limit:
          if teamName[i] == 'Centre':
               centreTOP.append(possessionClock[i])
               i += 1
          else:
               oppTOP.append(possessionClock[i])
               i += 1

     i = 0
     while i <= (len(centreTOP)-1):
          totalTimeCentre = int(centreTOP[i]) + totalTimeCentre
          i += 1
     i = 0
     while i <= (len(oppTOP)-1):
          totalTimeOpp = int(oppTOP[i]) + totalTimeOpp
          i += 1

     stats = ['Centre T.O.P', totalTimeCentre, opponentName[2] + ' T.O.P', totalTimeOpp]
                         
     # Total Points / Possessions (PPP)
     i = 0
     centrePTs = 0
     opponentPTs = 0
     while i <= limit:
          if teamName[i] == 'Centre':
               centrePTs = points[i] + centrePTs
               i += 1
          else:
               opponentPTs = points[i] + opponentPTs
               i += 1

     pppOpponent = opponentPTs / ballOpp
     pppOpponent = '{:.3f}'.format(pppOpponent)
     pppCentre = centrePTs / ballCentre
     pppCentre = '{:.3f}'.format(pppCentre)
     pppStats = [np.nan, 'Centre Points per Poss.', pppCentre, opponentName[2] + ' Points per Poss.', pppOpponent]
     stats = stats + pppStats
     
     i = 8
     while i <= limit:
          stats.append(np.nan)
          i += 1
   
     # Excel Sheet
     fullData.append(data)
     fullData['Possession Change'] = possessionChange
     fullData['Possession Clock'] = possessionClock
     fullData[''] = np.nan
     fullData['Statline'] = stats
     fullData = fullData.replace({'0':np.nan, 0:np.nan})
     fullData.to_csv (r'C:\Users\Kameron.DESKTOP-9OMTKVA\Desktop\FallResearch\testing.csv', index=False, header=True)
     
if __name__ == "__main__":
     main()
