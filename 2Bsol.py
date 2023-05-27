from ProcessGameState import ProcessGameState
from tester import Tester
import numpy as np
import pandas as pd
gameState = ProcessGameState('./data/game_state_frame_data.parquet')
# gameState = Tester()

def solution(gameState,team,side,site):
    # filter data to only have Team2 on T side 
    conditions = [(gameState.df['team'] == team), (gameState.df['side'] == side)]
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
    conditions = [(gameState.df['team'] == team), 
                (gameState.df['side'] == side), 
                (gameState.df['area_name'] == site)]
    gameState.sort('tick')
    weaponClasses = gameState.getWeaponClasses()
    team2TSideData = gameState.filterDf(conditions)
    for i, roundData in team2TSideData.groupby('round_num'):
        uniquePlayers = roundData['player'].unique()
        if len(uniquePlayers) >= 2:
            masks = [roundData['player'] == player for player in uniquePlayers]
            combinedMask = np.logical_or.reduce(masks)
            #get unique players
            filteredEntries = roundData[combinedMask]
            #calculate all the differences of tick values 
            tickDiffs = np.abs(filteredEntries['tick'].to_numpy()[:, None] - filteredEntries['tick'].to_numpy())
            gunCount = 0
            secondLowestTick = 0
            if np.any(tickDiffs <= 1280): #at least 2 people on bombsite B within 10 seconds
                for p in uniquePlayers:
                    indexes = (filteredEntries[filteredEntries['player'] == p]).index
                    for index in indexes:
                        weapons = weaponClasses[index]
                        #check if they hold correct weapons
                        if("Rifle" in weapons or "SMG" in weapons):
                            gunCount +=1
                            saveTick = (filteredEntries[filteredEntries['player'] == p])['tick'].values[0]
                            if(secondLowestTick < saveTick):
                                secondLowestTick = saveTick
                            if (gunCount >= 2):
                                roundEntries[i] = secondLowestTick - lowestTick[i]    
                            continue    
    return roundEntries

roundEntries = solution(gameState, "Team2", "T", "BombsiteB")
print(roundEntries)
# {16: None, 17: None, 18: None, 19: None, 20: None, 21: 2672, 22: None, 23: None, 24: None, 25: None, 26: None, 27: None, 28: 4992, 29: None, 30: 5248}
#These are all within a reasonable range since a csgo round (without planting) is 115 seconds and
#the min value is around 21 seconds which would be a rush and the max is 41 seconds which is slower play
timeSum = 0
counter = 0
for key, val in roundEntries.items():
    if(val is not None):
         counter+=1
         timeSum+=val
print('The average time Team2 entered Bombsite B with 2 Rifles or SMGS on T side is:', (timeSum/counter)/128, 'seconds into the round.')
# The average time Team2 entered Bombsite B on T side is: 33.625 seconds into the round.
#I can trust this answer because if I change the site to BombsiteA I can see little to no overlap in round numbers
#that this strategy is used since it would be quite difficult to have multiple people enter both sites in the same round
#Another reason I can trust this answer is because BombsiteA is the CT spawn so I get values of basically 0 seconds into the round
#that the CT side enters the site wit