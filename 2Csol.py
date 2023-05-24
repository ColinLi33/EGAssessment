from ProcessGameState import ProcessGameState
gameState = ProcessGameState('./data/game_state_frame_data.parquet')

# c)
conditions = [(gameState.df['team'] =='Team2'), 
              (gameState.df['side'] == 'CT'), 
              (gameState.df['area_name'] =='BombsiteB')]
team2CTSideData = gameState.filterDf(conditions)

# need to scale the coordinates to fit the map


#Q3)
#I would use a library called pyinstaller https://pyinstaller.org/en/stable/
# to package the script into an executable. I could  add a simple interface
#that allows for input of a parquet file, and map and lets you outline the boundary 
#of interest directly onto the map. I can then take the coordinates from the outline
#to use for the boundary