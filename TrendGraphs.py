#Read the final Pollution Health dataset. Aggregate
# on Years and show the plot of the mean pollution level
# for each year
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
result = pd.read_csv(filename)
grouped = result.groupby('Year_x')

for name,group in grouped:
    NO2Summary = grouped["NO2"].mean()
    PM10Summary = grouped["PM10"].mean()
#    prev = grouped["ListSize"].sum() / grouped["Register"].sum()

NO2Summary.plot(color="blue")
PM10Summary.plot(color="red")
plt.legend()
plt.xlabel('Years')
plt.ylabel("ug/m3")
plt.title('Pollution levels of NO2 and PM10 over time')
plt.show()
