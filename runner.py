from ProcessGameState import ProcessGameState
regionOfInterest = [(-1735,250),(-2024,398),(-2806,742),(-2472,1233),(-1565,580)]
zSampleBounds = (285,421)
gameState = ProcessGameState('./data/game_state_frame_data.parquet')

#2A
checkStrategy = gameState.check_strategy('Team2', 'T', regionOfInterest, zSampleBounds)
count = sum(value == True for value in checkStrategy.values())
print('This strategy was used', count, 'time by Team 2 on T side which is', count/len(checkStrategy)*100, "% of rounds played")

#2B
roundEntries = gameState.checkGunsOnSite("Team2", "T", "BombsiteB", ['Rifle', 'SMG'])
timeSum = 0
counter = 0
for key, val in roundEntries.items():
    if(val is not None):
         counter+=1
         timeSum+=val
print('The average time Team2 entered Bombsite B with 2 Rifles or SMGS on T side is:', (timeSum/counter)/128, 'seconds into the round.')

gameState.generateHeatmap('Team2', 'CT', 'BombsiteB')
print("Heatmap saved to /heatmap folder")
