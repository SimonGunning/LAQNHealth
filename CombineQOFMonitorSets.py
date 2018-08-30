#This program will read the aggregated QOF File.
# Then it will read the Monitors file for the pollution data
# Then it will merge them both based on WardCode
import pandas as pd
import requests
import json
from tkinter  import Tk
from tkinter.filedialog import askopenfilename
print("Select the Aggregated LondonQOF file to merge")
year = input("Year =")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

SuperDF = pd.read_csv(filename)
SuperDF.columns = ["WardCode","Register","ListSize","Prevalence_perc", "Year"]
print("Select Pollution File")

filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)
PollutionDF = pd.read_csv(filename)
PollutionDF.columns = ["WardCode", "Year","Ward","Monitor","Longitude","Latitude","NO2","PM10","DUST"]
SuperDF = pd.merge(SuperDF, PollutionDF, left_on='WardCode', right_on='WardCode', how='inner')

print(SuperDF)


SuperDF.to_csv("SuperDF.csv")


