from ProcessGameState import ProcessGameState
regionOfInterest = [(-1735,250),(-2024,398),(-2806,742),(-2472,1233),(-1565,580)]
zSampleBounds = (285,421)

#2A
gameState = ProcessGameState('./data/game_state_frame_data.parquet')
checkStrategy = gameState.check_strategy('Team2', 'T', regionOfInterest, zSampleBounds)
count = sum(value == True for value in checkStrategy.values())
print('This strategy was used', count, 'time(s) which is', count/len(checkStrategy), "% of rounds played")

#2B
gameState = ProcessGameState('./data/game_state_frame_data.parquet')
roundEntries = gameState.checkGunsOnSite("Team2", "T", "BombsiteB", ['Rifle', 'SMG'])
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

gameState = ProcessGameState('./data/game_state_frame_data.parquet')
gameState.generateHeatmap('Team2', 'CT', 'BombsiteB')
