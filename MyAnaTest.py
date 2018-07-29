# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 18:24:34 2018

@author: gunning
"""
import geopandas as gpd
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
#print(gpd.datasets.get_path('C:\\Users\\gunning\\Anaconda3\\Lib\\site-packages\\geopandas\\datasets\\naturalearth_lowres\\ccg.dbf'))
ccg = gpd.read_file('C:\\Users\\gunning\\Anaconda3\\Lib\\site-packages\\geopandas\\datasets\\naturalearth_lowres\\ccg.dbf')
print(ccg.head(5))

sLength = len(ccg['objectid'])
ccg['e'] = pd.Series(np.random.randn(sLength), index=ccg.index)
print(ccg.head(5))
ccg.plot(column = "e")
plt.title("CCG map")

#plt.xlabel('position')
#plt.ylabel('value')

plt.show()#print(world)
