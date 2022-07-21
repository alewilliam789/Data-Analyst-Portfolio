import pandas as pd


def na_vacuum(df):
    df = df.dropna(axis=1, thresh=((len(df.index)) / 2))
    df = df.dropna(axis=0, how='any')
    return df




