from heapq import merge
import pandas as pd

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, askopenfilenames

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# reads csv file for city dataset
df = pd.read_csv(filename)

# reads csv files for schools
school_data = askopenfilenames()

# reads txt file for column names
columns_file = askopenfilename()

cols_dict = {}

with open(columns_file, mode='r') as file:
    lines = file.readlines()

for line in lines:
    key, value = line.split(",")
    key = key.strip()
    value = value.strip()
    cols_dict[key] = value

print(cols_dict)

# creates dataframe for each file
dataframes = [pd.read_csv(file) for file in school_data]

# merged dataframes
merged_dataframes = [pd.merge(df, dataframe, on="city") for dataframe in dataframes]

# concatenate merged dataframes
final_df = pd.concat(merged_dataframes, axis=0)

final_df = final_df.dropna()

final_df.rename(cols_dict, inplace=True)

final_df.to_csv("city_and_sat.csv", index=False)