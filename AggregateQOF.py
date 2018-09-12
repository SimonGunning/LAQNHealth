# -*- coding: utf-8 -*-
"""
@author: gunning

This program takes the output from the QOFProcessor. It sums the list and prevalence for
each practice in each ward. Then it outputs a file called LondonQOFAggregated-yyyy
"""
import pandas as pd
from tkinter  import Tk
from tkinter.filedialog import askopenfilename
#from shapely.geometry import Point
#import numpy as np
#import pickle
print("please select a QOFProcessor output file")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title = "Please select a QOFProcessor output file") # show an "Open" dialog box and return the path to the selected file
LondonQOF = pd.read_csv(filename)
print(LondonQOF.columns.values)
print(LondonQOF["Year"][2])
year = LondonQOF["Year"][2]
#print(LondonQOF.head(5))
LondonQOF.set_index('WardCode')
LondonQOF.apply(pd.to_numeric, errors='ignore')
LondonQOF[['Register','ListSize']] = LondonQOF[['Register','ListSize']].apply(pd.to_numeric, errors='coerce')
print(LondonQOF.dtypes)
#print(LondonQOF.groupby("WardCode").groups)
grouped = LondonQOF.groupby(['WardCode', 'Ward'])

for name,group in grouped:
    LondonQOFAggregated1 = grouped["Register"].sum()
    LondonQOFAggregated2 = grouped["ListSize"].sum()

LondonQOFAggregated1 = pd.merge(LondonQOFAggregated1.to_frame(), LondonQOFAggregated2.to_frame(), left_index=True, right_index=True, how='inner')
#
LondonQOFAggregated1['Prevalence_perc'] = LondonQOFAggregated1['Register']/LondonQOFAggregated1['ListSize']
LondonQOFAggregated1['Year'] = year

print(LondonQOFAggregated1.head(3))
LondonQOFAggregatedFName = "LondonQOFAggregated-" + str(year)
LondonQOFAggregated1.to_csv(LondonQOFAggregatedFName)


