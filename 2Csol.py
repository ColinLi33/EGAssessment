from ProcessGameState import ProcessGameState
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import image
gameState = ProcessGameState('./data/game_state_frame_data.parquet')

conditions = [(gameState.df['team'] =='Team2'), 
              (gameState.df['side'] == 'CT'), 
              (gameState.df['area_name'] =='BombsiteB')]
team2CTSideData = gameState.filterDf(conditions)


#TODO: need to scale the coordinates from CSGO data to the coordinates of the map background
minX = team2CTSideData['x'].min()
maxX = team2CTSideData['x'].max()
minY = team2CTSideData['y'].min()
maxY = team2CTSideData['y'].max()

sns.kdeplot(data=team2CTSideData, x='x', y='y', cmap='YlOrRd', fill=True,alpha=.5)
map_image = image.imread('./map/BombsiteB.png')

plt.imshow(map_image, extent=[minX, maxX, minY, maxY], aspect='auto')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Heatmap of Team2 CT side BombsiteB')
plt.show()

