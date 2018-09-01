import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
from matplotlib import pyplot as plt
from tkinter  import Tk
from tkinter.filedialog import askopenfilename
print("Select the Combined QOF and Monitor file form the .. process")
year = input("Year =")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title = "Select Monitors file") # show an "Open" dialog box and return the path to the selected file
Monitors = pd.read_csv(filename)
MonitorsGPD = gpd.GeoDataFrame(Monitors)
geometry = [Point(xy) for xy in zip(Monitors.Longitude, Monitors.Latitude)]
crs = {'init': 'epsg:4326'}
monitors = gpd.GeoDataFrame(MonitorsGPD, crs=crs, geometry=geometry)
# get the ward map base file
wardDF = gpd.read_file('C:\\Users\\simon\\OneDrive\\Documents\\MSC\\QOFInputFiles\\London-wards-2014\\London-wards-2014 (1)\\London-wards-2014_ESRI\\London_Ward.shp',crs=crs)
wardDF = wardDF.to_crs({'init': 'epsg:4326'})
#get the QOF File
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title = "Select QOF file") #get QOF data
LondonQOF = pd.read_csv(filename)
LondonQOFDF = gpd.GeoDataFrame(LondonQOF)
LondonQOFDF = pd.merge(wardDF, LondonQOFDF, left_on='GSS_CODE', right_on='WardCode', how='inner')
LondonQOFDF = LondonQOFDF.to_crs({'init': 'epsg:4326'})

base = wardDF.plot(color='white', edgecolor='black')
LondonQOFDF.plot(ax=base,column='Prevalence_perc', cmap='Greys')
monitors.plot(ax=base,column='NO2', cmap='Reds')

#sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=10, vmax=100))
#sm._A = []
#cbar = plt.colorbar(sm)

plt.show()
