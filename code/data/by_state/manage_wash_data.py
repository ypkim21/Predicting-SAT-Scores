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
df = df[~df.eq("-").any(1)]

# drops any null values
df = df.dropna()

# convert numerical sat data to numbers
df = df.astype({'crit_read_mean':'float', 'math_mean':'float',
                'writing_mean':'float'})
df = df.astype({'crit_read_mean':'int32', 'math_mean':'int32',
                'writing_mean':'int32'})

# reads dataset containing school directory (to link to city)
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# reads csv file for schools with addresses
cities_df = pd.read_csv(filename)

ap = AddressParser()

cities_df['PhysicalAddress'] = cities_df['PhysicalAddress'].map(lambda address: ap.parse_address(address).city)

final_df = pd.merge(df, cities_df, on="High School")

final_df.rename(columns={"High School": "sname", "PhysicalAddress":"city"}, inplace=True)

final_df.drop_duplicates(subset="sname")

final_df.dropna()

final_df.drop(['ai_code'], axis=1, inplace=True)

print(final_df[['city', 'crit_read_mean', 'math_mean', 'writing_mean']])

final_df['city'] = final_df['city'].astype('str') + ", washington"
final_df['city'] = final_df['city'].str.lower()

cols = ['city', 'crit_read_mean', 'writing_mean', 'math_mean']

final_df[cols].to_csv("wash_data.csv", index=False)