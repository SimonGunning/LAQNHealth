# Combines the monitors file with the the Aggregated QOF file and maps them to a map produced from the shapefile
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
from matplotlib import pyplot as plt
from tkinter  import Tk
from tkinter.filedialog import askopenfilename
year = input("Year = ")
pollutant = input("Pollutant = ")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title = "Select Monitors file") # show an "Open" dialog box and return the path to the selected file
Monitors = pd.read_csv(filename)
MonitorsGPD = gpd.GeoDataFrame(Monitors)
#exclude monitors outside London
MonitorsGPD = MonitorsGPD.loc[MonitorsGPD['Longitude'] > -0.6]
MonitorsGPD = MonitorsGPD.loc[MonitorsGPD['Longitude'] < 0.3]
MonitorsGPD = MonitorsGPD.loc[MonitorsGPD['Latitude'] > 51.3]

geometry = [Point(xy) for xy in zip(MonitorsGPD.Longitude, MonitorsGPD.Latitude)]
crs = {'init': 'epsg:4326'}
newMonitors = gpd.GeoDataFrame(MonitorsGPD, crs=crs, geometry=geometry)
# get the ward map base file
wardDF = gpd.read_file('C:\\Users\\simon\\OneDrive\\Documents\\MSC\\QOFInputFiles\\London-wards-2014\\London-wards-2014 (1)\\London-wards-2014_ESRI\\London_Ward.shp',crs=crs)
wardDF = wardDF.to_crs({'init': 'epsg:4326'})
#get the QOF File
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title = "Select QOF file") #get QOF data
LondonQOF = pd.read_csv(filename)
LondonQOF['Prevalence_perc'] = LondonQOF['Prevalence_perc'] * 100
LondonQOFDF = gpd.GeoDataFrame(LondonQOF)
LondonQOFDF = pd.merge(wardDF, LondonQOFDF, left_on='GSS_CODE', right_on='WardCode', how='inner')
# fill with median
medianPP = LondonQOFDF['Prevalence_perc'].median()
print(LondonQOFDF)

LondonQOFDF = LondonQOFDF.to_crs({'init': 'epsg:4326'})
base = wardDF.plot(color='grey', edgecolor='black')

LondonQOFDF.plot(ax=base,column='Prevalence_perc', cmap='Greys', legend=True)
newMonitors.plot(ax=base, column=pollutant, cmap='YlOrRd', legend=True)

#sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=10, vmax=100))
#sm._A = []
#cbar = plt.colorbar(sm)
Title = year + " London Ward Asthma prevalence shown in grey. Pollution monitors are in red"
plt.title(Title, fontsize=16)
top3 = LondonQOFDF.nlargest(3,'Prevalence_perc')['Ward']
Top3 = "Top 3 wards with highest disease prevalence " + str(top3)
plt.text(0.02, 0.1, Top3, fontsize=11, transform=plt.gcf().transFigure)
top3Monitors = newMonitors.nlargest(3,pollutant)['Ward']
Top3Monitors = "Top 3 monitors with highest pollution levels " + str(top3Monitors)
plt.text(0.4, 0.1, Top3Monitors, fontsize=11, color = 'red', transform=plt.gcf().transFigure)
ptext = pollutant + " ug/m3"
plt.text(0.7, 0.6, ptext, fontsize=11, rotation = 'vertical', color = 'red', transform=plt.gcf().transFigure)
plt.text(0.85, 0.6, "Disease incidence %", fontsize=11, rotation = 'vertical', color = 'black', transform=plt.gcf().transFigure)

plt.axis("off")
plt.show()
