import pandas as pd
from shapely.geometry import Point, Polygon

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
    
    #1C)
    def getWeaponClasses(self):
        return self.df['inventory'].apply(lambda inventory: [item['weapon_class'] for item in inventory] if inventory is not None else [])