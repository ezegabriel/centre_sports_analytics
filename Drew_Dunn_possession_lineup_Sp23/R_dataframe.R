library(tidyverse)
library(dplyr)
#This calculates all the stats for every player given a specific game
#The players list will need to be updated for the current years' roster
df = read_csv('/Users/drewdunn/Desktop/Python code for research/Lineup/test.csv')
players = list('bailey rakes', 'jalen williams', 'dawson crump', 'art walker',
               'carter baughman', 'keegan brewer', 'will britt', 'rj smith',
               'drew wilson', 'jacob bates', 'jakob spitzer', 'kc purvis',
               'dustin gerald', 'perry ayers', 'pete knochelmann')
for (i in 1:length(players)){
opponent = df$boxscore_visitor_name[1]
offposs_list = list()
defposs_list = list()
ppr_list = list()
off_rebl = list()
def_rebl = list()
offreb_ratel = list()
defreb_ratel = list()
off_ratel = list()
def_ratel = list()
plusminus_l = list()
df2 = df %>% filter(df['player1'] == players[i] | df['player2'] == players[i]
                    |df['player3'] == players[i] | df['player4'] == players[i]
                    |df['player4'] == players[i])
df2
df3 = df2 %>% filter(df2['Possession Change'] == 'C')
df4 = df2 %>% filter(df2['Possession Change'] == 'O')
off_totpoints = sum(df3['Points Per Possession'])
def_totpoints = sum(df4['Points Per Possession'])
plusminus = off_totpoints - def_totpoints
off_poss = n_distinct(unique(df3['Possession Number']))
def_poss = n_distinct(unique(df4['Possession Number']))
off_rate = off_totpoints/off_poss * 100
def_rate = def_totpoints/def_poss * 100
off_reb = length(which(df3['Play Type'] == 'offensive rebound'))
def_reb = length(which(df4['Play Type'] == 'defensive rebound'))
opp_off_reb = length(which(df4['Play Type'] == 'offensive rebound'))
opp_def_reb = length(which(df3['Play Type'] == 'defensive rebound'))
offreb_rate = off_reb/(off_reb + opp_def_reb)
defreb_rate = def_reb/(def_reb + opp_off_reb)
points = sum(df3['Points Per Possession'])
possession = lengths(unique(df3['Possession Number']))
ppr = points/possession
ppr_list = append(ppr_list, round(ppr, digits = 2))
off_rebl = append(off_rebl, round(off_reb, digits = 2))
def_rebl = append(def_rebl, round(def_reb, digits = 2))
offposs_list = append(offposs_list, round(off_poss, digits = 2))
defposs_list = append(defposs_list, round(def_poss, digits = 2))
offreb_ratel = append(offreb_ratel, round(offreb_rate, digits = 2))
defreb_ratel = append(defreb_ratel, round(defreb_rate, digits = 2))
off_ratel = append(off_ratel, round(off_rate, digits = 2))
def_ratel = append(def_ratel, round(def_rate, digits = 2))
plusminus_l = append(plusminus_l, round(plusminus, digits = 2))
ppr_list
off_rebl
def_rebl
offposs_list
defposs_list
offreb_ratel
defreb_ratel
off_ratel
def_ratel
plusminus_l
nested_list = list(Opponent = opponent,
                   Points_Per_Possession =ppr_list,
                   Offensive_Rebounds = off_rebl,
                   Defensive_Rebounds = def_rebl,
                   Offensive_Possessions = offposs_list,
                   Defensive_Possessions = defposs_list,
                   Offensive_Rebound_Rate = offreb_ratel,
                   Defensive_Rebound_Rate = defreb_ratel,
                   Offensive_Rating = off_ratel,
                   Defensive_rating = def_ratel,
                   Plus_Minus = plusminus_l)
player_df = data.frame(nested_list)
colnames(player_df) <- c('Opponent', 'PPR', 'Off Reb', 'Def Reb', 'Off Poss', 'Def Poss',
                         'Off Reb Rate', 'Def Reb Rate', 'Off Rating', 'Def Rating',
                         '+/-')
write.csv(player_df, paste("/Users/drewdunn/Desktop/Python code for research/Research R stuff/", players[i], "_stats.csv"), row.names=FALSE)
}