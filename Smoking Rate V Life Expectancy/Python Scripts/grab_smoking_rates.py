def grab_smoking_rates():
    import pandas as pd

    # Input into df to perform analysis on
    df = pd.read_csv("C:\\Users\\Alex\\PycharmProjects\\SmokerPercentageVLifeExpectancy\\smoking_rates.csv")

    # Sort in alphabetical order
    df = df.sort_values("Country", ascending=True)
    return df
