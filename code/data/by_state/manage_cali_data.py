import pandas as pd

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, asksaveasfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# reads csv file for SAT dataset
df = pd.read_csv(filename)

# selects data that are data by school
df = df[df.rtype == 'S']

# selects data that isn't omitted
df = df[~df.eq("*").any(1)]

# drops any null values
df = df.dropna()

df = df.drop_duplicates(subset="cds")

# convert numerical sat data to numbers
df = df.astype({'avgscrmath':'float', 'avgscrwrit':'float',
                'avgscrread':'float'})
df = df.astype({'avgscrmath':'int32', 'avgscrwrit':'int32',
                'avgscrread':'int32'})

# reads dataset containing school directory (to link to city)
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

school_df = pd.read_csv(filename, encoding = "ISO-8859-1")

# renames columns (for merging)
school_df.rename(columns={"CDS Code": "cds"}, inplace=True)

school_df = school_df.drop_duplicates("cds")

# merges city with school
city_df = pd.merge(school_df, df, on="cds")

# creates histograms for reference
print(city_df[['sname', 'Street City', 'avgscrmath', 'avgscrwrit', 'avgscrread']])

city_df.rename(columns={"Street City": "city", "avgscrread":"crit_read_mean",
"avgscrwrit":"writing_mean", "avgscrmath":"math_mean"}, inplace=True)

city_df['city'] = city_df['city'].astype('str') + ", california"
city_df['city'] = city_df['city'].str.lower()

cols = ['city', 'crit_read_mean', 'writing_mean', 'math_mean']

print(city_df[cols].describe())

city_df[cols].to_csv("cali_data.csv", index=False)