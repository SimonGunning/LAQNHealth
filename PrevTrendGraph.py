#Read the final Pollution Health dataset. Aggregate
# on Years and show the plot of the mean prevalence level
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
    prev = (grouped["Register"].sum() / grouped["ListSize"].sum()) * 100

prev.plot(color="green")
plt.xlabel('Years')
plt.ylabel("% Asthma Prevalence")
plt.title('Asthma prevalence over time')
plt.show()
