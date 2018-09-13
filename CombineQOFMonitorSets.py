#This program will read the aggregated QOF File for a year.
# Then it will read the Monitors file for the pollution data from the same year.
# Then it will merge them both based on WardCode
import pandas as pd
import requests
import json
from tkinter  import Tk
from tkinter.filedialog import askopenfilename
print("Select the Aggregated LondonQOF file to merge")
year = input("Year =")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

filename = askopenfilename(title='Select the LondonQOFAggregated-yyyy file you want to use') # show an "Open" dialog box and return the path to the selected file

SuperDF = pd.read_csv(filename)
SuperDF.columns = ["WardCode","Ward","Register","ListSize","Prevalence_perc", "Year"]
print("Select Pollution File")

filename = askopenfilename(title='Select the MonitorWardsFile-yyyy file you want to use') # show an "Open" dialog box and return the path to the selected file
print(filename)
PollutionDF = pd.read_csv(filename)
PollutionDF.columns = ["WardCode", "Year","Ward","Monitor","Longitude","Latitude","NO2","PM10","DUST"]
SuperDF = pd.merge(SuperDF, PollutionDF, left_on='WardCode', right_on='WardCode', how='inner')

print(SuperDF)

combinedFileName = "CombinedFile-" + year
SuperDF.to_csv(combinedFileName)


