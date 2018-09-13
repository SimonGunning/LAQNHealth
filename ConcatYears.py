#Read the combined files and  concatenates them
#  to produce a single file
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


import pandas as pd
from tkinter import *
import tkinter.filedialog
print("Select the files to analyse")

root = Tk()
filez = tkinter.filedialog.askopenfilenames(parent=root,title='Select the years that you want to concatenate')
fileList = list(root.tk.splitlist(filez))
frames =[]
for i in range (0 , len(fileList)):
    ADF = pd.read_csv(fileList[i])
    frames.append(ADF)
    ADF.iloc[0:0]
result = pd.concat(frames, ignore_index=True)
result.to_csv("HealthPollutionDS.csv")




