#Read the superDFs concatenate them and perform regressions
# This requires the latest version of Pandas
import pandas as pd
from tkinter import *
import tkinter.filedialog
print("Select the files to analyse")

root = Tk()
filez = tkinter.filedialog.askopenfilenames(parent=root,title='Choose a file')
fileList = list(root.tk.splitlist(filez))
for i in range (0 , len(fileList)):
    print(fileList[i])

#filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#print(filename)

# SuperDF = pd.read_csv(filename)
# SuperDF.columns = ["WardCode","Register","ListSize","Prevalence_perc", "Year"]
# print("Select Pollution File")
#
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# print(filename)
# PollutionDF = pd.read_csv(filename)
# PollutionDF.columns = ["WardCode", "Year","Ward","Monitor","Longitude","Latitude","NO2","PM10","DUST"]
# SuperDF = pd.merge(SuperDF, PollutionDF, left_on='WardCode', right_on='WardCode', how='inner')
#
# print(SuperDF)
#SuperDF.to_csv("SuperDF.csv")


