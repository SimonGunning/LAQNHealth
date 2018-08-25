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

LondonQOF = pd.read_csv('C:\\Users\\gunning\\Documents\\Anatest\\londonQOF1')
print(LondonQOF.columns.values)
#LondonQOFAggregated = pd.DataFrame(columns=['Postcode', 'Ward', 'PracticeCode', 'RegionName', 'Y1Prevalence', 'Y2Prevalence'])
LondonQOFAggregated1 = pd.DataFrame(columns=['SumPrev'])
LondonQOFAggregated2 = pd.DataFrame(columns=['SumPost'])

#print(LondonQOF.head(5))
LondonQOF.set_index('WardCode')
LondonQOF.apply(pd.to_numeric, errors='ignore')
print(LondonQOF.dtypes)

LondonQOF[['Y1Prevalence','Y2Prevalance']] = LondonQOF[['Y1Prevalence','Y2Prevalance']].apply(pd.to_numeric, errors='coerce')
print(LondonQOF.dtypes)

#print(LondonQOF.groupby("WardCode").groups)
grouped = LondonQOF.groupby('WardCode')

for name,group in grouped:
#     print(name)
#     print(group)
#    print(grouped["Y2Prevalance"].sum())
#    print("type of thing" + str(type(grouped["Y1Prevalence"].sum())))
    LondonQOFAggregated1 = grouped["Y1Prevalence"].sum()
    LondonQOFAggregated2 = grouped["Y2Prevalance"].sum()

#    print(group["PracticeCode"])
LondonQOFAggregated1 = pd.merge(LondonQOFAggregated1.to_frame(), LondonQOFAggregated2.to_frame(), left_index=True, right_index=True, how='inner')
#grouped = LondonQOF.groupby(LondonQOF.index)["Y1Prevalence"].sum()
print(LondonQOFAggregated1.head(3))




