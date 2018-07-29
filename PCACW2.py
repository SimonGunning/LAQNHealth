print(__doc__)
# PCA coursework
# 
import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets
from sklearn.decomposition import PCA

data = pd.read_csv("C:\\Users\\gunning\\Documents\\simon\\DSTA\\kaggle\\USPollution data\\uspollution\\pollution_us_2000_2016.csv", sep = ",")
data1 = data[['State','NO2 Mean','O3 Mean','SO2 Mean']]
#read State Totals
StateTotals = pd.read_csv("C:\\Users\\gunning\\Documents\\simon\\DSTA\\kaggle\\USPollution data\\AlabamaCalc.csv", sep = ",", encoding = 'unicode_escape')
# Normalise totals
#for index, row in StateTotals.iterrows():
#    x = StateTotals[['Total']].index = (StateTotals[['Total']].index - StateTotals[['Total']].min()) / (StateTotals[['Total']].max() - StateTotals[['Total']].min())
#   print(x)

#Create join on State with Asthma totals file to produce new dataframe
data3 = pd.merge(data1, StateTotals, on='State', how='inner', suffixes=['', '_'])

data4 = data3[['NO2 Mean','Total']]

#print(data4)
# To getter a better understanding of interaction of the dimensions
# plot the first 2 PCA dimensions
fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
X_reduced = PCA(n_components=2).fit_transform(data4)
#print(X_reduced)
ax.scatter(X_reduced[:, 0], X_reduced[:, 1],
           cmap=plt.cm.Set1, edgecolor='k', s=40)
ax.set_title("First 2 PCA directions")
ax.set_xlabel("1st eigenvector")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("2nd eigenvector")
ax.w_yaxis.set_ticklabels([])
#ax.set_zlabel("3rd eigenvector")
#ax.w_zaxis.set_ticklabels([])

plt.show()