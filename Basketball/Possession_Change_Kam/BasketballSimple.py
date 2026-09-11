# Imports
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import csv

#import heartrate
#from time import sleep
#heartrate.trace(browser=True)
#sleep(0.25)

def main():
     # Read file
     fullData = pd.read_excel(r'C:\Users\Kameron.DESKTOP-9OMTKVA\Desktop\FallResearch\Hendrix.xlsx', converters = {'Team':str})
     data = pd.read_excel(r'C:\Users\Kameron.DESKTOP-9OMTKVA\Desktop\FallResearch\Hendrix.xlsx', usecols = ['Play Type', 'Team', 'Time(seconds)', 'opponent name', 'Points Earned', 'Shot Outcome'])
     data = data.fillna(0)

     # List Creation
     opponentName = data['opponent name'].tolist()
     shotOutcome = data['Shot Outcome'].tolist()
     gameClock = data['Time(seconds)'].tolist()
     points = data['Points Earned'].tolist()
     playData = data['Play Type'].tolist()
     teamName = data['Team'].tolist()
     gameClock[0] = 1200
     playOutcome = list(zip(playData,teamName,gameClock))

     # Empty Lists
     possessionOpponent = []
     possessionChange = []
     possessionCentre = []
     possessionClock = []
     subList = []

     # Check Lists
     noChangeData = ['block', 'deadball rebound', 'offensive rebound', 'timeout']
     subData = ['subbing in', 'subbing out']
     
     # Misc.
     limit = len(playOutcome) - 2 # 497
     possessionClock.append(np.nan)
     playData.append(np.nan)
     teamName.append(np.nan)
     preSubValue = 0

     # Possession
     for i in range(len(playOutcome)):
          # Tip Off & Start of Second Half
          if playData[i] == 0:
               if teamName[i] == 'Centre':
                    possessionChange.append('X'); possessionCentre.append('X')
               else:
                    possessionChange.append('O'); possessionOpponent.append('O')
          # End of Halves
          elif playData[i+1] == 0 or i == len(playOutcome)-1:
               possessionChange.append(' ')
          # Substitutions
          elif playData[i] in subData:
               possessionChange.append('-')
          # Continuous play
          elif teamName[i] == teamName[i+1] and playData[i] != 'turnover':
               possessionChange.append(' ')
          # Free Throw with First Missed
          elif playData[i-2] == 'free throw' and playData[i-1] == 'deadball rebound' and playData[i] == 'free throw' and shotOutcome[i] == 'good':
               if teamName[i] == 'Centre':
                    possessionChange.append('O'); possessionCentre.append('O')
               else:
                    possessionChange.append('X'); possessionOpponent.append('X')
          # No Change
          elif playData[i] == 'free throw' and playData[i+1] == 'deadball rebound'  or playData[i] in noChangeData:
               possessionChange.append(' ')
          elif playData[i] == 'free throw' and playData[i+1] == 'free throw':
               possessionChange.append(' ')
          # Change
          elif playData[i] == 'turnover':
               if teamName[i] == 'Centre':
                    possessionChange.append('O'); possessionCentre.append('O')
               else:
                    possessionChange.append('X'); possessionOpponent.append('X')
          elif playData[i] == 'foul' or playData[i+1] == 'foul':
               if playData[i] == 'turnover':
                    if teamName[i] == 'Centre':
                         possessionChange.append('O'); possessionCentre.append('O')
                    else:
                         possessionChange.append('X'); possessionOpponent.append('X')
               elif shotOutcome[i] == 'good' and playData[i+1] == 'foul':
                    if teamName[i] == 'Centre':
                         possessionChange.append('O'); possessionCentre.append('O')
                    else:
                         possessionChange.append('X'); possessionOpponent.append('X')
               else:
                    possessionChange.append(' ')
          elif playData[i] == 'free throw' and playData[i+1] != 'free throw' and shotOutcome[i] == 'good':
               if teamName[i] == 'Centre':
                    possessionChange.append('O'); possessionCentre.append('O')
               else:
                    possessionChange.append('X'); possessionOpponent.append('X')
          # Made Shot (Assisted or Not)
          elif playData[i] == 'assist':
               print(i, playData[i+1], playData[i+2])
               if teamName[i] == 'Centre':
                    possessionChange.append('O'); possessionCentre.append('O')
               else:
                    possessionChange.append('X'); possessionOpponent.append('X')
          elif shotOutcome[i] == 'good' and playData[i+1] != 'assist':
               if teamName[i] == 'Centre':
                    possessionChange.append('O'); possessionCentre.append('O')
               else:
                    possessionChange.append('X'); possessionOpponent.append('X')
          # Missed Shot
          elif shotOutcome[i] == 'missed' and teamName[i] == teamName[i+1]:
               possessionChange.append(' ')
          elif shotOutcome[i] == 'missed' and playData[i+1] == 'block' and playData[i+2] == 'defensive rebound':
               if teamName[i] == 'Centre':
                    possessionChange.append('O'); possessionCentre.append('O')
               else:
                    possessionChange.append('X'); possessionOpponent.append('X')
          elif playData[i+1] == 'defensive rebound' and playData[i] != 'block':
               if teamName[i] == 'Centre':
                    possessionChange.append('O'); possessionCentre.append('O')
               else:
                    possessionChange.append('X'); possessionOpponent.append('X')
          elif playData[i] == 'defensive rebound' and teamName[i] != teamName[i+1] and playData[i+1] not in subData:
               if teamName[i] == 'Centre':
                    possessionChange.append('O'); possessionCentre.append('O')
               else:
                    possessionChange.append('X'); possessionOpponent.append('X')
          elif playData[i] == 'defensive rebound' and playData[i+1] in subData:
               possessionChange.append(' ')
          # Team in Bonus
          elif playData[i] == 'foul' and playData[i+1] == 'free throw' and teamName[i] != teamName[i+1]:
               if teamName[i] == 'Centre':
                    possessionChange.append('O'); possessionCentre.append('O')
               else:
                    possessionChange.append('X'); possessionOpponent.append('X')
          # Extra Cases
          elif playData[i+1] == 'offensive rebound' and teamName[i] != teamName[i+1]:
               possessionChange.append(' ')
          else:
               possessionChange.append('BROKE')

     # Total Possession / Home & Opponent Possession
     ballCentre = len(possessionCentre); ballOpponent = len(possessionOpponent); totalChanges = ballCentre + ballOpponent
     percentCentre = (ballCentre/totalChanges) * 100; percentOpponent = (ballOpponent/totalChanges) * 100 # Formatted into percentages
     percentCentre = '{:.2f}'.format(percentCentre); percentOpponent = '{:.2f}'.format(percentOpponent) # Formatted into 2 decimal percentages

     # Time of Possession
     i = 1
     while i <= limit:
          if playData[i] == 0:
               gameClock[i] = 1200; i += 1
          else:
               i += 1
     i = 1
     while i <= limit:
          while gameClock[i] == 0:
               gameClock[i] = gameClock[i-1]
          else:
               if (gameClock[i] - gameClock[i-1]) > 30:
                    possessionClock.append(1200 - gameClock[i]); i += 1
               elif 'X' in possessionChange and gameClock[i] != 0 and gameClock[i] != gameClock[i-1]:
                    timeOfPossession = abs(gameClock[i] - gameClock[i-1])
                    possessionClock.append(timeOfPossession); i += 1
               else:
                    possessionClock.append(np.nan); i += 1
                    
     possessionClock.append(np.nan)
     possessionClock = [0 if math.isnan(x) else x for x in possessionClock]

     i = 1
     centreTOP = []; opponentTOP = []
     totalTimeCentre = 0; totalTimeOpponent = 0

     while i <= limit:
          if teamName[i] == 'Centre':
               centreTOP.append(possessionClock[i]); i += 1
          else:
               opponentTOP.append(possessionClock[i]); i += 1
     i = 0
     while i <= (len(centreTOP)-1):
          totalTimeCentre = int(centreTOP[i]) + totalTimeCentre; i += 1
     i = 0
     while i <= (len(opponentTOP)-1):
          totalTimeOpponent = int(opponentTOP[i]) + totalTimeOpponent; i += 1
          
     stats = ['Centre T.O.P', totalTimeCentre, opponentName[2] + ' T.O.P', totalTimeOpponent]
     
     # Total Points / Possessions (PPP)
     centrePoints = 0; opponentPoints = 0
     for i in range(len(playOutcome)):
          if teamName[i] == 'Centre':
               centrePoints = points[i] + centrePoints
          else:
               opponentPoints = points[i] + opponentPoints

     pppCentre = centrePoints / ballCentre; pppCentre = '{:.3f}'.format(pppCentre)
     pppOpponent = opponentPoints / ballOpponent; pppOpponent = '{:.3f}'.format(pppOpponent)
     pppStats = [np.nan, 'CENTRE Points per Possession', pppCentre, opponentName[2].upper() + ' Points per Possession', pppOpponent]
     stats = stats + pppStats
     
     i = 8
     while i <= limit:
          stats.append(np.nan); i += 1


     ### CHECK
     for i in range(len(playOutcome)):
          print(i, possessionChange[i])
          
     print('Centre', ballCentre)
     print('Opponent', ballOpponent)
     
     # Excel Sheet
     fullData.append(data)
     fullData['Possession Change'] = possessionChange; fullData['Possession Clock'] = possessionClock; fullData[''] = np.nan; fullData['Statline'] = stats
     fullData = fullData.replace({'0':np.nan, 0:np.nan})
     fullData.to_csv (r'C:\Users\Kameron.DESKTOP-9OMTKVA\Desktop\FallResearch\simpletest.csv', index=False, header=True)
     
if __name__ == "__main__":
     main()
