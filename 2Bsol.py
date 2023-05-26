from ProcessGameState import ProcessGameState
import numpy as np
import pandas as pd
gameState = ProcessGameState('./data/game_state_frame_data.parquet')
weaponClasses = gameState.getWeaponClasses()

# filter data to only have Team2 on T side 
conditions = [(gameState.df['team'] =='Team2'), (gameState.df['side'] == 'T')]
team2TSideData = gameState.filterDf(conditions)

maxRound = team2TSideData['round_num'].max()
minRound = team2TSideData['round_num'].min()
team2TSideData = team2TSideData.groupby('round_num')
     
#roundEntries will hold the data we need it is formatted
#:key=roundNum, val=earliest tick 2 players entered B with smg/rifle
roundEntries = {key: None for key in range(minRound, maxRound+1)}

#Save the lowest tick of each round so we can find time elapsed
lowestTick = {}
for roundNum, roundData in team2TSideData:
     lowestTick[roundNum] = roundData['tick'].min()

#filter the data based on conditions needed
conditions = [(gameState.df['team'] =='Team2'), 
              (gameState.df['side'] == 'T'), 
              (gameState.df['area_name'] =='BombsiteB')]
team2TSideData = gameState.filterDf(conditions)
team2TSideData.sort_values(by='tick')
for i, roundData in team2TSideData.groupby('round_num'):
    uniquePlayers = roundData['player'].unique()
    if len(uniquePlayers) >= 2:
        masks = [roundData['player'] == player for player in uniquePlayers]
        combinedMask = np.logical_or.reduce(masks)
        filteredEntries = roundData[combinedMask]
        tickDiffs = np.abs(filteredEntries['tick'].to_numpy()[:, None] - filteredEntries['tick'].to_numpy())
        gunCount = 0
        if np.any(tickDiffs <= 1280): #at least 2 people on bombsite B within 10 seconds
            for p in uniquePlayers:
                indexes = (filteredEntries[filteredEntries['player'] == p]).index
                for index in indexes:
                    weapons = weaponClasses[index]
                    if("Rifle" in weapons or "SMG" in weapons):
                        gunCount +=1
                        continue
            if (gunCount >= 2):
                roundEntries[i] = filteredEntries['tick'].max() - lowestTick[i]
                            
print(roundEntries)
#{16: None, 17: None, 18: None, 19: None, 20: None, 21: 12689, 22: None, 23: None, 24: None, 25: None, 26: None, 27: None, 28: 10688, 29: None, 30: 5344}
#These are all within a reasonable range since a csgo round (without planting) is 115 seconds and
#the min value is around 41 seconds and the max is 99 seconds
timeSum = 0
counter = 0
for key, val in roundEntries.items():
    if(val is not None):
         counter+=1
         timeSum+=val
print('The average time Team2 entered Bombsite B on T side is:', (timeSum/counter)/128, 'seconds into the round.')
# The average time Team2 entered Bombsite B on T side is: 74.79427083333333 seconds into the round. 
