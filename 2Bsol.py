from ProcessGameState import ProcessGameState

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
