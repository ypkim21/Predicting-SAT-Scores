import pandas as pd

import matplotlib.pyplot as plt

from address import AddressParser

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# reads csv file for SAT dataset
df = pd.read_csv(filename)

# selects data that isn't omitted
df = df[~df.eq("*").any(1)]

# drops any null values
df = df.dropna()


df = df.astype({'Reading Average':'float', 'Math Average':'float',
                'Writing Average':'float'})
df = df.astype({'Reading Average':'int32', 'Math Average':'int32',
                'Writing Average':'int32'})

# reads dataset containing school directory (to link to city)
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# reads csv file for schools with addresses
cities_df = pd.read_csv(filename)

# merges dataframes
final_df = pd.merge(df, cities_df, on="AUN")
final_df = final_df.drop_duplicates(subset="School Name")

final_df.rename(columns={"LEALocationCity":"city", "Reading Average":"crit_read_mean",
"Math Average":"math_mean", "Writing Average":"writing_mean"}, inplace=True)

final_df['city'] = final_df['city'].astype('str') + ", pennsylvania"
final_df['city'] = final_df['city'].str.lower()

print(final_df[['city', 'crit_read_mean', 'math_mean', 'writing_mean']])

cols = ['city', 'crit_read_mean', 'writing_mean', 'math_mean']

final_df[cols].to_csv("penn_data.csv", index=False)