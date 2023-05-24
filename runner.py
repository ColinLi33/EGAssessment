from ProcessGameState import ProcessGameState
import pandas as pd
regionOfInterest = [(-1735,250),(-2024,398),(-2806,742),(-2472,1233),(-1565,580)]
zSampleBounds = (285,421)

gameState = ProcessGameState('./data/game_state_frame_data.parquet')
boundaryData = gameState.check_boundary(regionOfInterest,zSampleBounds)
weaponClasses = gameState.getWeaponClasses()


#Answering question 2

#A)
# based on my knowledge of csgo I need to check if multiple people enter the
# light blue boundary at similar times atleast once in the round to count it off as using that strategy


#this dict will contain boolean for each round that Team2 played on T side that 
#are True if the strategy was used and false otherwise
# roundEntries = {}

# # filter data to only have Team2 on T side 
# conditions = [(gameState.df['team'] =='Team2'), (gameState.df['side'] == 'T')]
# team2TSideData = gameState.filterDf(conditions)

# maxRound = team2TSideData['round_num'].max()
# minRound = team2TSideData['round_num'].min()
# roundEntries = {key: False for key in range(minRound, maxRound+1)}

# # filter data further to only have data where the boundary was entered
# conditions.append(boundaryData)
# team2TSideData = gameState.filterDf(conditions)
# # 


# for i, roundData in team2TSideData.groupby('round_num'):
#     uniquePlayersInInterval = roundData.groupby(roundData['tick'] // 1280)['player'].nunique()
#     #if atleast two players 
#     if (uniquePlayersInInterval >= 2).any():
#         roundEntries[i] = True
#     else:
#         roundEntries[i] = False

# count = sum(value == True for value in roundEntries.values())
# print('This strategy was used', count, 'time(s) which is', count/len(roundEntries), "% of rounds played")
#OUTPUT: This strategy was used 1 time(s) which is 0.06666666666666667 % of rounds played
#based on this Team2 does not enter the light blue boundary very often on T side

#B)
#similar logic to first question
roundEntries = {}

# filter data to only have Team2 on T side 
conditions = [(gameState.df['team'] =='Team2'), (gameState.df['side'] == 'T')]
team2TSideData = gameState.filterDf(conditions)

maxRound = team2TSideData['round_num'].max()
minRound = team2TSideData['round_num'].min()
roundEntries = {key: None for key in range(minRound, maxRound+1)}

#filter the data based on conditions needed
conditions = [(gameState.df['team'] =='Team2'), 
              (gameState.df['side'] == 'T'), 
              (gameState.df['area_name'] =='BombsiteB')]


