import pandas as pd
import numpy as np

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# reads csv file for city dataset
df = pd.read_json(filename)


columns_file = askopenfilename()

cols_dict = {}

with open(columns_file, mode='r') as file:
    lines = file.readlines()

for line in lines:
    key, value = line.split(",")
    key = key.strip()
    value = value.strip()
    cols_dict[key] = value

df.dropna()

new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header #set the header row as the df header

df.rename(columns=cols_dict, inplace=True)

cols = [column for column in cols_dict]

for col in cols:
    df[col] = pd.to_numeric(df[col])

fips_codes = []

terms = [" cdp", " town city", " city", " town", " borough"]

df['NAME'] = df['NAME'].str.lower()

for i in range(0, len(df)):
    city, state = df["NAME"].iloc[i].split(",")

    for term in terms:
        if city.__contains__(term):
            index = city.index(term)
            break
    
    city = city[:index]
    
    df["NAME"].iloc[i] = "{},{}".format(city, state)

df = df[(df[cols] > 0).all(axis=1)]

df = df.dropna()

df = df.drop(["state", "place"], axis=1)

df.rename({"NAME":"city"}, inplace=True)

df.to_csv("cities.csv", index=False)