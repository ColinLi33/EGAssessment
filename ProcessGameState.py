import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
import seaborn as sns
from matplotlib import pyplot as plt
from PIL import Image

class ProcessGameState():
    #1A)
    def __init__(self, file):
        self.df = pd.read_parquet(file, engine='pyarrow')

    #helper function
    def getRow(self, row):
        return self.df.loc[row]
    #helper function
    def getCol(self,col):
        return self.df[col]
    
    def sort(self,col):
        self.df.sort_values(by=col, inplace=True)
    
    #function to return a filtered df based on list of conditions
    def filterDf(self, conditions):
        condition = pd.Series(True, index=self.df.index)
        for cond in conditions:
            if isinstance(cond, pd.Series):
                condition &= cond
            else:
                condition &= cond(self.df)
        filteredDf = self.df.loc[condition]
        return filteredDf
    
    #1B)
    def check_boundary(self, roi, zBoundary):
        if 'x' not in self.df.columns or 'y' not in self.df.columns or 'z' not in self.df.columns:
            raise ValueError("Missing x,y,z data")

        #using a python library to check if points are within the region
        region = Polygon(roi)
        within_region = self.df.apply(lambda row: Point(row['x'], row['y']).within(region), axis=1)

        #since the allowed z values are much simpler I don't need to use the polygon library
        within_z = (self.df['z'] >= zBoundary[0]) & (self.df['z'] <= zBoundary[1])
        return within_region & within_z

    #2A)
    def check_strategy(self, team, side, roi, zBounds):
        # this dict will contain boolean for each round that Team2 played on T side that 
        # are True if the strategy was used and false otherwise
        boundaryData = self.check_boundary(roi,zBounds)
        roundEntries = {}

        # filter data to only have Team2 on T side 
        conditions = [(self.df['team'] == team), (self.df['side'] == side)]
        team2TSideData = self.filterDf(conditions)
        maxRound = team2TSideData['round_num'].max()
        minRound = team2TSideData['round_num'].min()
        roundEntries = {key: False for key in range(minRound, maxRound+1)}

        # filter data further to only have data where the boundary was entered
        conditions.append(boundaryData)
        self.sort('tick')
        team2TSideData = self.filterDf(conditions)

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
        
    #1C)
    def getWeaponClasses(self):
        return self.df['inventory'].apply(lambda inventory: [item['weapon_class'] for item in inventory] if inventory is not None else [])
    
    #2B)
    def checkGunsOnSite(self,team,side,site,weaponList):
        # filter data to only have Team2 on T side 
        conditions = [(self.df['team'] == team), (self.df['side'] == side)]
        team2TSideData = self.filterDf(conditions)

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
        conditions = [(self.df['team'] == team), 
                    (self.df['side'] == side), 
                    (self.df['area_name'] == site)]
        self.sort('tick')
        weaponClasses = self.getWeaponClasses()
        team2TSideData = self.filterDf(conditions)
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
                            if([element for element in weaponList if element in weapons]):
                                gunCount +=1
                                saveTick = (filteredEntries[filteredEntries['player'] == p])['tick'].values[0]
                                if(secondLowestTick < saveTick):
                                    secondLowestTick = saveTick
                                if (gunCount >= 2):
                                    roundEntries[i] = secondLowestTick - lowestTick[i]    
                                continue    
        return roundEntries
    
    def generateHeatmap(self, team, side, areaName):
        conditions = [(self.df['team'] == team), 
                    (self.df['side'] == side), 
                    (self.df['area_name'] == areaName)]
        self.sort('tick')
        team2CTSideData = self.filterDf(conditions)

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