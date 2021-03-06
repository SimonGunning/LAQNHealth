#Read the superDFs concatenate them and perform regressions
# This requires the latest version of Pandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import geopandas as gpd
import pysal as ps

from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.filedialog
print("Select the POLLUTANT to analyse")
pollutant = input("CHOOSE: NO2, PM10 OR DUST =")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title = "please select the full dataset") # show an "Open" dialog box and return the path to the selected file
result = pd.read_csv(filename)
result = result.dropna(subset=[pollutant])

#there are now no NaNs for this pollutant
x = result["Prevalence_perc"].values.reshape(-1, 1)
x = x * 100
y = result[pollutant].values.reshape(-1, 1)
# Split the data into training/testing sets
x_train = x[:-20]
x_test = x[-20:]
# Split the targets into training/testing sets
y_train = y[:-20]
y_test = y[-20:]
#print(y_train)
#print(y_test)
#print(x_train)
#print(x_test)

# Create linear regression object
regr = linear_model.LinearRegression(normalize=True)
# Train the model using the training sets
regr.fit(x, y)
disease_y_pred = regr.predict(x)
print("Results of standard Linear Regression")
print("Rsqared = " + str(regr.score(x_train,y_train)))
print("Intercept = " + str(regr.intercept_))
# The coefficients
print('Coefficients: \n', regr.coef_)
# instantiate a logistic regression model, and fit with X and y
print("Results of Logistic Regression")
logModel = linear_model.LogisticRegression()
logModel = logModel.fit(x, y)
print(logModel)
# check the accuracy on the training set
print("log score")
print(logModel.score(x, y))



colors = (0,0,0)
area = np.pi*3
plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.plot(x, disease_y_pred, color='blue', linewidth=3)
plt.title('Scatter plot of disease prevalence datapoints plotted against pollution measurements')
plt.xlabel('disease incidence %')
plt.ylabel('pollution ug/m3 as an annual mean')
plt.show()



# The mean squared error
#print("Mean squared error: %.2f"
#      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# Explained variance score: 1 is perfect prediction
#print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

# Plot outputs
#plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
#plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)

#plt.xticks(())
#plt.yticks(())

#plt.show()


