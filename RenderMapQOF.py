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
# dtype = {'name': str,'review': str]
LondonQOF = pd.read_csv('C:\\Users\\gunning\\Documents\\Anatest\\LondonQOFAggregated1.csv')
LondonQOFDF = gpd.GeoDataFrame(LondonQOF)

wardDF = gpd.read_file('C:\\Users\\gunning\\Documents\\simon\\MSCProject\\\London-wards-2014\\London-wards-2014 (1)\\London-wards-2014_ESRI\\London_Ward.shp')

LondonQOFDF = pd.merge(wardDF, LondonQOFDF, left_on='GSS_CODE', right_on='WardCode', how='inner')

print(LondonQOFDF.head(5))

base = wardDF.plot(color='white', edgecolor='black')
plt.title("Ward and Asthma prevalence map")
plt.annotate("source bla bla" ,xy=(0.1, .08), fontsize=12, color="#555555")
plt.axis("off")
#fig, ax = plt.subplots(1, figsize=(10, 6))
#ax.annotate("Source: London Datastore, 2014",xy=(0.1, .08),  xycoords="figure fraction", horizontalalignment="left",
#verticalalignment="top", fontsize=12, color="#555555")

LondonQOFDF.plot(ax=base,column='Prevalence_perc', cmap='OrRd')
#fig, ax = plt(1, figsize=(10, 6))
sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=10, vmax=100))
sm._A = []
cbar = plt.colorbar(sm)

plt.show()#print(world)
