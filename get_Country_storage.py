def get_country_storage():
    import pandas as pd
    from data_cleaner import na_vacuum
    import numpy as np
    import datetime


    # load data and clean
    file_name = "Arrival_Numbers.csv"
    df = pd.read_csv(file_name)
    df = na_vacuum(df)

    # Split to a numpy array so that I can store points for plotting.
    mr_array = df.to_numpy()

    # Create empty dictionary to store all the countries and information
    Country_storage = {}

    # Iterate to add new entries for available countries into dictionary
    for row in mr_array:
        Country_data = row
        Country_name = Country_data[0]
        Country_storage[Country_name] = [Country_data[1:], [datetime.datetime(year, 1, 1) for year in range(1995,2020)], None, None, None]

    # Load data for latitude and longitude
    file_name2 = "Lat_Long.csv"
    df2 = pd.read_csv(file_name2)

    # Add latitude and longitude points to each country still in database
    for key in Country_storage:
        stringy = key[0:8]
        mask = np.column_stack(
            [df2["Country"].astype(str).str.contains(stringy, na=False) for country in df2['Country']])
        latty_long = df2
        latty_long = latty_long[mask]
        if len(latty_long) > 0:
            Country_storage[key][2] = latty_long.iat[0, 1]
            Country_storage[key][3] = latty_long.iat[0, 2]
        else:
            pass
        Country_storage[key][4] = key+'.html'

    delete = [key for key in Country_storage if Country_storage[key][2] is None]

    for key in delete:
        del Country_storage[key]

    return Country_storage
