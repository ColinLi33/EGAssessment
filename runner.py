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
#roundEntries will be key:round num, val: first time entered site with 2 rifles/smgs
team2TSideData = team2TSideData.groupby('round_num')

#Save the lowest tick of each round so we can find time elapsed
lowestTick = {}
for roundNum, roundData in team2TSideData:
     lowestTick[roundNum] = roundData['tick'].min()
     
#roundEntries will hold the data we need it is formatted
#:key=roundNum, val=earliest tick 2 players entered B with smg/rifle
roundEntries = {key: None for key in range(minRound, maxRound+1)}

#filter the data based on conditions needed
conditions = [(gameState.df['team'] =='Team2'), 
              (gameState.df['side'] == 'T'), 
              (gameState.df['area_name'] =='BombsiteB')]
team2TSideData = gameState.filterDf(conditions)
team2TSideData = team2TSideData.groupby('round_num')

#for each round
for roundNum, roundData in team2TSideData:
    sortedByTick = roundData.sort_values('tick')
    smgRifleCount = 0
    #set to make sure we don't count the same player twice
    playerSet = set()

    #for each tick in the round
    for i, row in sortedByTick.iterrows():
        #check for rifles/smgs
        if('Rifle' in weaponClasses[i] or 'SMG' in weaponClasses[i]):
             for player in row['player']:
                    if player not in playerSet:
                        smgRifleCount += 1
                        playerSet.add(player)
                        # print(row['tick'])
        #get earliest time 2 rifles/smg entered the area
        if smgRifleCount >= 2:
            roundEntries[roundNum] = (row['tick'] - lowestTick[roundNum])
            break

print(roundEntries)
#{16: None, 17: None, 18: None, 19: None, 20: None, 21: 2416, 22: None, 23: 
# None, 24: None, 25: 3888, 26: 13136, 27: None, 28: 3584, 29: None, 30: 4576}
#These are all within a reasonable range since a csgo round (without planting) is 115 seconds and
#the min value is around 18 seconds and the max is 102 seconds
timeSum = 0
counter = 0
for key, val in roundEntries.items():
    if(val is not None):
         counter+=1
         timeSum+=val
print('The average time Team2 entered Bombsite B on T side is:', (timeSum/counter)/128, 'seconds into the round.')
#The average time Team2 entered Bombsite B on T side is: 43.125 seconds into the round.      


#c)
# conditions = [(gameState.df['team'] =='Team2'), 
#               (gameState.df['side'] == 'CT'), 
#               (gameState.df['area_name'] =='BombsiteB')]
# team2CTSideData = gameState.filterDf(conditions)


#need to scale the coordinates to fit the map





#Q3)
#I would use a library called pyinstaller https://pyinstaller.org/en/stable/
# to package the script into an executable. I could  add a simple interface
#that allows for input of a parquet file, and map and lets you outline the boundary 
#of interest directly onto the map. I can then take the coordinates from the outline
#to use for the boundary