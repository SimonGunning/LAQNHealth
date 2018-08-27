#Read the superDFs concatenate them and perform regressions
# This requires the latest version of Pandas
import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.filedialog
print("Select the files to analyse")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

result = pd.read_csv(filename)
result = result.dropna(subset=['NO2'])

#prevNO2 = pd.DataFrame([result["Prevalence_perc"],result["NO2"]])
print(result)
x_train = result["Prevalence_perc"].values.reshape(-1, 1)
y_train= result["NO2"].values.reshape(-1, 1)
# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(x_train, y_train)
print("Rsqared = " + str(regr.score(x_train,y_train)))
print("Intercept = " + str(regr.intercept_))

# Make predictions using the testing set
#diabetes_y_pred = regr.predict(diabetes_X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
colors = (0,0,0)
area = np.pi*3

plt.scatter(x_train, y_train, s=area, c=colors, alpha=0.5)
plt.title('Scatter plot pythonspot.com')
plt.xlabel('x')
plt.ylabel('y')
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


