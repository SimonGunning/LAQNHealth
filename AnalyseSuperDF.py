#Read the superDFs concatenate them and perform regressions
# This requires the latest version of Pandas
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


import pandas as pd
from tkinter import *
import tkinter.filedialog
print("Select the files to analyse")

root = Tk()
filez = tkinter.filedialog.askopenfilenames(parent=root,title='Choose a file')
fileList = list(root.tk.splitlist(filez))
frames =[]
for i in range (0 , len(fileList)):
    ADF = pd.read_csv(fileList[i])
    frames.append(ADF)
    ADF.iloc[0:0]
result = pd.concat(frames, ignore_index=True)
result.to_csv("thebus.csv")

# # Load the diabetes dataset
# diabetes = datasets.load_diabetes()
# # Use only one feature
# diabetes_X = diabetes.data[:, np.newaxis, 2]
# # Split the data into training/testing sets
# diabetes_X_train = diabetes_X[:-20]
# diabetes_X_test = diabetes_X[-20:]
# # Split the targets into training/testing sets
# diabetes_y_train = diabetes.target[:-20]
# diabetes_y_test = diabetes.target[-20:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(result["Prevalence_perc"], result["NO2"])

# Make predictions using the testing set
#diabetes_y_pred = regr.predict(diabetes_X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
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


