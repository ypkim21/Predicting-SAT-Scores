import pandas as pd

import matplotlib.pyplot as plt

from address import AddressParser

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# reads csv file for SAT dataset
df = pd.read_csv(filename)

df = df.drop_duplicates("School Name")

# convert numerical sat data to numbers
df = df.dropna()

df = df.astype({'Reading':'float', 'Math':'float',
                'Writing':'float'})
df = df.astype({'Reading':'int32', 'Math':'int32',
                'Writing':'int32'})

# reads dataset containing school directory (to link to city)
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# reads csv file for schools with addresses
cities_df = pd.read_csv(filename)

# merges dataframes
final_df = pd.merge(df, cities_df, on="School Code")

final_df.rename(columns={"Town": "city", "Reading":"crit_read_mean", "Math":"math_mean", "Writing":"writing_mean"}, inplace=True)

print(final_df[['city', 'crit_read_mean', 'math_mean', "writing_mean"]].describe())

final_df['city'] = final_df['city'].astype('str') + ", massachusetts"
final_df['city'] = final_df['city'].str.lower()

cols = ['city', 'crit_read_mean', 'writing_mean', 'math_mean']

final_df[cols].to_csv("mass_data.csv", index=False)