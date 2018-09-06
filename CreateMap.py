import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
from matplotlib import pyplot as plt
from tkinter  import Tk
from tkinter.filedialog import askopenfilename
print("Select the Aggregated QOF file from the AggregateQOF process")
year = input("Year =")
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
LondonQOFDF = gpd.GeoDataFrame(LondonQOF)
LondonQOFDF = pd.merge(wardDF, LondonQOFDF, left_on='GSS_CODE', right_on='WardCode', how='inner')
# fill with median
medianPP = LondonQOFDF['Prevalence_perc'].median()
print(LondonQOFDF)

LondonQOFDF = LondonQOFDF.to_crs({'init': 'epsg:4326'})
base = wardDF.plot(color='grey', edgecolor='black')

LondonQOFDF.plot(ax=base,column='Prevalence_perc', cmap='Greys', legend=True)
newMonitors.plot(ax=base, column='NO2', cmap='YlOrRd', legend=True)

#sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=10, vmax=100))
#sm._A = []
#cbar = plt.colorbar(sm)
plt.title("London Ward Asthma prevalence is shown in grey. Pollution monitors are in red", fontsize=16)
top3 = LondonQOFDF.nlargest(3,'Prevalence_perc')['WardCode']
Top3 = "Top 3 prevalence " + str(top3)

plt.text(0.02, 0.1, Top3, fontsize=14, transform=plt.gcf().transFigure)
plt.annotate("source bla bla" ,xy=(1,1), fontsize=12, color="#555555")
plt.axis("off")

plt.show()
