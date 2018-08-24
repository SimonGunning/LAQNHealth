# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 18:24:34 2018

@author: gunning
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
from matplotlib import pyplot as plt
import pickle
#with open('parrot1.pickle', 'rb') as handle:
#    MonitorsDF = pickle.load(handle)
MonitorsDF = pd.read_csv('C:\\Users\\gunning\\Documents\\Anatest\\monlocs')
#MonitorsDF['geometry'] = MonitorsDF.apply(lambda z: Point(z.X, z.Y), axis=1)
MonitorsDF = gpd.GeoDataFrame(MonitorsDF)

wardDF = gpd.read_file('C:\\Users\\gunning\\Documents\\simon\\MSCProject\\\London-wards-2014\\London-wards-2014 (1)\\London-wards-2014_ESRI\\London_Ward.shp')

MonitorsDF = pd.merge(wardDF, MonitorsDF, left_on='GSS_CODE', right_on='WardCode', how='inner')

print(wardDF.head(5))

#sLength = len(wardDF['NAME'])
#wardDF['e'] = pd.Series(np.random.randn(sLength), index=wardDF.index)
#print(ccg.head(5))
base = wardDF.plot(color='white', edgecolor='black')
plt.title("Ward and NO2 map")

MonitorsDF.plot(ax=base,column='PM10', cmap='Blues')

#plt.xlabel('position')
#plt.ylabel('value')

plt.show()#print(world)
