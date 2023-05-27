from ProcessGameState import ProcessGameState
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
gameState = ProcessGameState('./data/game_state_frame_data.parquet')

def generateHeatmap(gameState, team, side, areaName):
    conditions = [(gameState.df['team'] == team), 
                (gameState.df['side'] == side), 
                (gameState.df['area_name'] == areaName)]
    gameState.sort('tick')
    team2CTSideData = gameState.filterDf(conditions)

    #holds tuples of positionData
    positionList = []
    #running movement speed > 200, walking movement speed > 100
    def checkNotMoving(data):
        return data[(abs(data['x'].diff(4)) <= 32) & (abs(data['y'].diff(4)) <= 32)]

    #function to scale from csgo coords to map coords
    def scaleCoords(pos):
        x = pos[0]+2806
        y = pos[1]-1233
        xScalar = 2
        yScalar = 2.6
        y = (y/yScalar)+200
        return ((x/xScalar)-360,-y+150)

    for i, roundData in team2CTSideData.groupby('round_num'):
        uniquePlayers = roundData['player'].unique()
        masks = [roundData['player'] == player for player in uniquePlayers]
        combinedMask = np.logical_or.reduce(masks)
        filteredEntries = roundData[combinedMask]
        #for each player
        for p in uniquePlayers:
            playerData = (filteredEntries[filteredEntries['player'] == p])
            notMoving = checkNotMoving(playerData)
            #if they have not moved for a bit then add position to list because
            #we want to see where the defenderes are holding from
            for index, row in notMoving.iterrows():
                positionList.append(scaleCoords((row['x'],row['y'])))
            continue

    xValues = [x[0] for x in positionList]
    yValues = [y[1] for y in positionList]

    background_image = Image.open('./map/' + areaName + '.png')
    ax = plt.axes(frameon=True)
    ax.imshow(background_image)
    sns.kdeplot(x=xValues, y=yValues, cmap='RdYlBu', fill=True, alpha=0.6)
    plt.axis('off')
    ax.figure.savefig('./heatmap/2C_' + team + '_' + side + '_' + areaName + '.png', bbox_inches='tight',transparent=True, pad_inches=0)

generateHeatmap(gameState, 'Team2', 'CT', 'BombsiteB')
#I am not extremely confident in the result I got because I found this task to be quite challenging for some reason. I thought it should've been a pretty
#simple task to translate the coordinates from the game to the image so I can overlay the heatmap, but
#it seemed to be much harder than I anticipated 