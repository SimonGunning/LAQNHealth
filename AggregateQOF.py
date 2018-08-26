# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 18:24:34 2018

@author: gunning
"""
import pandas as pd
from shapely.geometry import Point
import numpy as np
import pickle

LondonQOF = pd.read_csv('C:\\Users\\gunning\\Documents\\Anatest\\londonQOF1')
print(LondonQOF.columns.values)
print(LondonQOF["Year"][2])
year = LondonQOF["Year"][2]

#LondonQOFAggregated = pd.DataFrame(columns=['Postcode', 'Ward', 'PracticeCode', 'RegionName', 'Y1Prevalence', 'Y2Prevalence'])
#LondonQOFAggregated1 = pd.DataFrame(columns=['SumPrev'])
#LondonQOFAggregated2 = pd.DataFrame(columns=['SumPost'])

#print(LondonQOF.head(5))
LondonQOF.set_index('WardCode')
LondonQOF.apply(pd.to_numeric, errors='ignore')

LondonQOF[['Register','ListSize']] = LondonQOF[['Register','ListSize']].apply(pd.to_numeric, errors='coerce')
print(LondonQOF.dtypes)

#print(LondonQOF.groupby("WardCode").groups)
grouped = LondonQOF.groupby('WardCode')

for name,group in grouped:
#     print(name)
#     print(group)
#    print(grouped["Y2Prevalance"].sum())
#    print("type of thing" + str(type(grouped["Y1Prevalence"].sum())))
    LondonQOFAggregated1 = grouped["Register"].sum()
    LondonQOFAggregated2 = grouped["ListSize"].sum()

#    print(group["PracticeCode"])
LondonQOFAggregated1 = pd.merge(LondonQOFAggregated1.to_frame(), LondonQOFAggregated2.to_frame(), left_index=True, right_index=True, how='inner')
#
LondonQOFAggregated1['Prevalence_perc'] = LondonQOFAggregated1['Register']/LondonQOFAggregated1['ListSize']
LondonQOFAggregated1['Year'] = year

print(LondonQOFAggregated1.head(3))

LondonQOFAggregated1.to_csv("LondonQOFAggregated1.csv")


