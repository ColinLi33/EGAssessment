from ProcessGameState import ProcessGameState
from tester import Tester
import numpy as np
regionOfInterest = [(-1735,250),(-2024,398),(-2806,742),(-2472,1233),(-1565,580)]
zSampleBounds = (285,421)

gameState = ProcessGameState('./data/game_state_frame_data.parquet')
# gameState = Tester()

def solution(gameState, team, side, roi, zBounds):
    # this dict will contain boolean for each round that Team2 played on T side that 
    # are True if the strategy was used and false otherwise
    boundaryData = gameState.check_boundary(roi,zBounds)
    roundEntries = {}

    # filter data to only have Team2 on T side 
    conditions = [(gameState.df['team'] == team), (gameState.df['side'] == side)]
    team2TSideData = gameState.filterDf(conditions)
    maxRound = team2TSideData['round_num'].max()
    minRound = team2TSideData['round_num'].min()
    roundEntries = {key: False for key in range(minRound, maxRound+1)}

    # filter data further to only have data where the boundary was entered
    conditions.append(boundaryData)
    gameState.sort('tick')
    team2TSideData = gameState.filterDf(conditions)

    for i, roundData in team2TSideData.groupby('round_num'):
        uniquePlayers = roundData['player'].unique()
        if len(uniquePlayers) >= 2:
            #look at all of their entries to see if there is any overlap
            masks = [roundData['player'] == player for player in uniquePlayers]
            combinedMask = np.logical_or.reduce(masks)
            filteredEntries = roundData[combinedMask]
            tickDiffs = np.abs(filteredEntries['tick'].to_numpy()[:, None] - filteredEntries['tick'].to_numpy())
            if np.any(tickDiffs <= 1280):
                roundEntries[i] = True
    return roundEntries

roundEntries = solution(gameState, 'Team2', 'T', regionOfInterest, zSampleBounds)
count = sum(value == True for value in roundEntries.values())
print('This strategy was used', count, 'time(s) which is', count/len(roundEntries), "% of rounds played")
#OUTPUT: This strategy was used 1 time(s) which is 0.06666666666666667 % of rounds played
#based on this Team2 does not enter the light blue boundary very often on T side
#I can trust this answer because if I change the side to CT, I observed a very high rate of this strategy
#being used and because the boundary is one of the ways CT side gets to BombsiteB it should be pretty commonly used