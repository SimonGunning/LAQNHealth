# Now try spatial regression
# build spatial adjacency matrix
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import geopandas as gpd
import pysal as ps

from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.filedialog
print("Select the POLLUTANT to analyse")
pollutant = input("CHOOSE: NO2, PM10 OR DUST =")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title = "please select the full dataset") # show an "Open" dialog box and return the path to the selected file
result = pd.read_csv(filename)
result = result.dropna(subset=[pollutant])

#there are now no NaNs for this pollutant
x = result["Prevalence_perc"].values.reshape(-1, 1)
x = x * 100
y = result[pollutant].values.reshape(-1, 1)
#
filename = askopenfilename(title = "please select the .shp file") # show an "Open" dialog box and return the path to the selected file
geo=gpd.read_file(filename).set_index("GSS_CODE")
gdf=gpd.GeoDataFrame(result, geometry=geo.geometry)

queen_w=ps.queen_from_shapefile(filename, 'GSS_CODE')
queen_neighs=queen_w.neighbors['E05000129']
q=geo.loc[queen_neighs].plot()
q.set_xticks([])
q.set_yticks([])
title=plt.title('Queen Adjacency')
plt.show()
# reduce the adjacency matrix to match the data
#print("warcos")
#print(result["WardCode"])
geo=geo[geo.index.isin(["E05000030", "E05000039"])]
geo.reset_index().to_file('Data/SF_BlockGroups10_Cleaned.shp')
#gdf=gpd.GeoDataFrame(data, geometry=geo.geometry)
w=ps.queen_from_shapefile('Data/SF_BlockGroups10_Cleaned.shp', 'GSS_CODE')
print(w.cardinalities.values())
#row standardise the adjacency matrix
y=gdf[pollutant]
yNA = y.values
print("yNA is ")
print(yNA)
w.transform='r'
print("typ x is ")
print(type(x))
print("typ y is ")
print(type(y))
print("typ w is ")
print(type(w))
#mi = ps.Moran(Y, w)
#pd.Series(index=['Morans I','Z-Score','P-Value'],data=[mi.I, mi.z_norm, mi.p_norm])

Y=result[pollutant].as_matrix().reshape((len(result),1))
X=result["Prevalence_perc"].as_matrix().reshape((len(result),1))

ols=ps.spreg.OLS(X, Y, w=w, nonspat_diag=False, spat_diag=True)
print(ols.summary)


mi = ps.Moran(ols.u, w, two_tailed=False)
pd.Series(index=['Morans I','Z-Score','P-Value'],data=[mi.I, mi.z_norm, mi.p_norm])
