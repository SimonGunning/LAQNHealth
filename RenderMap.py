# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 18:24:34 2018

@author: gunning
"""
import geopandas as gpd
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import pickle
with open('parrot1.pickle', 'rb') as handle:
    MonitorsDF = pickle.load(handle)

wardDF = gpd.read_file('C:\\Users\\gunning\\Documents\\simon\\MSCProject\\\London-wards-2014\\London-wards-2014 (1)\\London-wards-2014_ESRI\\London_Ward.shp')

wardDF = pd.merge(wardDF, MonitorsDF, left_on='NAME', right_on='Ward')

print(wardDF.head(5))

#sLength = len(wardDF['NAME'])
#wardDF['e'] = pd.Series(np.random.randn(sLength), index=wardDF.index)
#print(ccg.head(5))
wardDF.plot(column='PM10')
plt.title("Ward and NO2 map")

#plt.xlabel('position')
#plt.ylabel('value')

plt.show()#print(world)
