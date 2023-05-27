import pandas as pd
from shapely.geometry import Point, Polygon
import numpy as np
class Tester():
    #1A)
    def __init__(self):
        self.df = self.generateRandomDataFrame(5)

    def generateRandomDataFrame(self, num_rows):
        random_data = {
            'round_num': np.random.randint(1, 2, size=num_rows),
            'tick': np.random.randint(0, 100, size=num_rows),
            'side': np.random.choice(['T'], size=num_rows),
            'team': np.random.choice(['Team2'], size=num_rows),
            'hp': np.random.randint(1, 100, size=num_rows),
            'armor': np.random.randint(1, 100, size=num_rows),
            'is_alive': np.random.choice([True, False], size=num_rows),
            'x': np.random.randint(-5000, 5000, size=num_rows),
            'y': np.random.randint(-5000, 5000, size=num_rows),
            'z': np.random.randint(0, 500, size=num_rows),
           'inventory': [
                [{'ammo_in_magazine': np.random.randint(0, 30),
                  'ammo_in_reserve': np.random.randint(0, 100),
                  'weapon_class': np.random.choice(['Rifle', 'SMG']),
                  'weapon_name': np.random.choice(['P250', 'AK-47', 'UMP'])}]
                if np.random.rand() < 0.9 else None for _ in range(num_rows)],
            'total_utility': np.random.uniform(0.0, 100.0, size=num_rows),
            'equipment_value_freezetime_end': np.random.randint(0, 2000, size=num_rows),
            'area_name': np.random.choice(['BombsiteB'], size=num_rows),
            'seconds': np.random.randint(0, 60, size=num_rows),
            'clock_time': [f'{np.random.randint(0, 12):02d}:{np.random.randint(0, 60):02d}' for _ in range(num_rows)],
            't_alive': np.random.randint(0, 5, size=num_rows),
            'ct_alive': np.random.randint(0, 5, size=num_rows),
            'bomb_planted': np.random.choice([True, False], size=num_rows),
            'map_name': np.random.choice(['de_dust2', 'de_inferno', 'de_mirage', 'de_overpass'], size=num_rows),
            'utility_used': np.random.uniform(0.0, 10.0, size=num_rows),
            'player': ['Player' + str(i) for i in range(1, num_rows + 1)]
        }

        random_df = pd.DataFrame(random_data)
        return random_df
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

