import pandas as pd

# data cleaner module for data cleaning functions

# Removes all NaN rows first to make sure all data is complete
# Removes any NA columns

def na_vacuum(df):
    df = df.dropna(axis=1, thresh=((len(df.index)) / 2))
    df = df.dropna(axis=0, how='any')
    return df

def fill_blanks(df):
    df =



