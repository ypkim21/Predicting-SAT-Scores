from numpy import mean
from numpy import std
from numpy import absolute
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold

import pandas as pd
import matplotlib.pyplot as plt

from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import numpy as np

import os

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, askdirectory


def show_plot(x, y, xlabel, ylabel, title, filename, include_line=False):
    plt.scatter(x, y)
    
    if include_line == True:
        plt.plot(x, x)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename)
    plt.clf()
    plt.cla()


def get_columns():
    # reads txt file for column names
    columns_file = askopenfilename()

    cols_dict = {}

    with open(columns_file, mode='r') as file:
        lines = file.readlines()

    for line in lines:
        if (line[0] == "#"):
            continue

        key, value = line.split(",")
        key = key.strip()
        value = value.strip()
        cols_dict[key] = value

    return cols_dict

filename = askopenfilename()

df = pd.read_csv(filename)

# place to get columns
cols_dict = get_columns()
cols = [column for column in cols_dict]

# df = df.groupby('city', as_index=False).mean()

df = df.reset_index()

df['composite_mean'] = df['crit_read_mean'] + df['math_mean'] + df['writing_mean']

# place to save to directory
directory = askdirectory()

# saves descriptive statistics
path = os.path.join(directory, "description.csv")

df.describe().to_csv(path)

# performs standardization
x = df[cols].values #returns a numpy array
standard_scaler = preprocessing.StandardScaler()
x_scaled = standard_scaler.fit_transform(x)
df[cols] = pd.DataFrame(x_scaled)

# simple plots for each variable and composite score
for column in cols:
    show_plot(df[column], df['composite_mean'], cols_dict[column], "Composite Score", "",
    os.path.join(directory, "plots\\{}".format(cols_dict[column] + ".png")))

X_train, X_test, y_train, y_test = train_test_split(df[cols], df["composite_mean"], test_size=0.2, random_state=0)

regressor = LinearRegression()
regressor.fit(X_train, y_train)

coefficients = regressor.coef_
intercept = regressor.intercept_

y_pred = regressor.predict(X_test)

pred_df = pd.DataFrame({'actual': y_test, 'predicted': y_pred})

mse = metrics.mean_squared_error(y_test, y_pred)
mae = metrics.mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)
r_2_score = metrics.r2_score(y_test, y_pred)
adjust_r2 = 1 - ( 1-r_2_score ) * ( len(y_test) - 1 ) / ( len(y_test) - X_test.shape[1] - 1 )

show_plot(pred_df['predicted'], pred_df['actual'], "Predicted Scores", "Actual Scores", "Residual Plot", os.path.join(directory, "residual_plot.png"), include_line=True)

summary = """
Intecept: {}
Coefficients: {}
MAE: {}
MSE: {}
RMSE: {}
R_2 Score: {}
Adjusted R_2 Score: {}
""".format(intercept, coefficients, mae, mse, rmse, r_2_score, adjust_r2)

# define model evaluation method
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
# evaluate model
scores = cross_val_score(regressor, X_test, y_test, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
# force scores to be positive
scores = absolute(scores)
summary += 'Mean MAE: {} ({})'.format(mean(scores), std(scores))

with open(os.path.join(directory, "summary.txt"), mode="w") as file:
    file.write(summary)
