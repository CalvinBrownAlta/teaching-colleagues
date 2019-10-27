# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Parse pedestrian volumes from an Excel-based Turning Movement Count
#
# We have a folder full of Excel count data and companion PDFs. We need to parse each one to pull out a Pedestrian-specific volume number that we can then use to scale point sizes on a GIS map.
#
# Things to note:
# - Data does not start on Row 1
# - There are typically 4 columns with Ped data, but there could be non-standard intersections with more or fewer legs
#
# ### Use jupyter to prototype a solution:

# +
import pandas as pd
import os

data_folder = '/Users/calvindechicago/PycharmProjects/AltaWork/teaching-colleagues/Counts/Counts/Count Reports 6-17-19'
test_file = os.path.join(data_folder, "1 LICK MILL BLVD & TASMAN DR.xls")


# -

os.path.exists('/Users/calvindechicago/PycharmProjects/AltaWork/teaching-colleagues/Counts/Counts/Count Reports 6-17-19')

# Read the file starting at line 10
df = pd.read_excel(test_file, sheet_name="Vehicles", header=9)

# +
# Make a variable that will hold the total across all "Peds" columns
running_total = 0

# Get a list of all "Peds" column names
#ped_cols = [x for x in df.columns if "Peds" in x]

#Above list comprehension as a for loop
ped_cols = []
for x in df.columns: 
    if "Peds" in x:
        ped_cols.append(x)
# -

#see new value of ped_cols
print(ped_cols)

# +
# For each column, get the sum and add it to the running total
for col in ped_cols:
    col_total = df[col].sum()
    
    print(col)

    running_total += col_total
        
print(running_total)
# -

# ### Once you have a working solution, compartmentalize it within a function:
#
# Notice that I've left a few ``TODO`` items in there. Figure out how to add those in after you've reviewed the code

# +

print("=================")
print(type(df))
print("=================")
print("=================")
print("=================")
print(df.head(3))
print(df.tail(3))
print("=================")
print("Types")
print(df.dtypes)
print("=================")
print("Values")
print(df.values)
print("=================")
print("Columns")
print(df.columns)
print("=================")
print("Index")
print(df.index)
print("=================")
df.columns = df.columns.str.lower().str.replace(' ','_')
print("Columns")
print(df.columns)
print("=================")

# -

df.start_time = df.start_time.astype('datetime64[ns]')
print(df.dtypes)
print(df.start_time.dt.hour)

# +

#List Comprehension that iterates on starttime column
timebucket =[x for x in df.start_time.dt.hour if x > 4 and x < 7]
timebucket_morningrush =[x for x in df.start_time.dt.hour if x > 6 and x < 10]
print(timebucket)
print(timebucket_morningrush)
# -

# betweentime =[x for x in df.start_time if df.start_time.between_time('0:45', '0:15')]
# df = df.set_index('datetime')
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.indexer_between_time.html#pandas.DatetimeIndex.indexer_between_time
# great pandas time tutorial
# https://www.youtube.com/watch?v=yCgJGsg0Xa4


btimetest = df.index.between_time('5:45', '6:15')
btimetest


# +
# Now do all the above as a function

def get_ped_total(excel_count_file):
    # Read the file starting at line 10
    df = pd.read_excel(excel_count_file, sheet_name="Vehicles", header=9)

    # Make a variable that will hold the total across all "Peds" columns
    daily_total = 0

    # Get a list of all "Peds" column names
    ped_cols = [x for x in df.columns if "Peds" in x]

    # For each column, get the sum and add it to the daily total
    for col in ped_cols:
        col_total = df[col].sum()

        daily_total += col_total
        
    # TODO: parse out a few time buckets (i.e. AM peak, midday, PM peak)
    # ...
    
    # TODO: modify the return value so that the function returns the daily total along with the time bucket totals
    # ...
    
    return daily_total


# -

# ### Now we're ready to iterate over all Excel files and pull results out

for f in os.listdir(data_folder):
    xls_path = os.path.join(xlsx_folder, f)
    total = get_ped_total(xls_path)
    
    print(total, f)

Macintosh HD⁩ ▸ ⁨Users⁩ ▸ ⁨calvindechicago⁩ ▸ ⁨PycharmProjects⁩ ▸ ⁨AltaWork⁩ ▸ ⁨teaching-colleagues⁩ ▸ ⁨Counts⁩ ▸ ⁨Counts⁩ ▸ ⁨Count Reports 6-17-19⁩


# # ``TODO``
#
# - Iterate over all files, getting full day and time bucket data
# - Wrangle all results into a ``pandas.DataFrame``. Each location (/excel file) becomes a row in this table.
# - Save this dataframe to ``.csv``
