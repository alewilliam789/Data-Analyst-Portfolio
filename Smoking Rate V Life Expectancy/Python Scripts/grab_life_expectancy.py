from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

# Makes sure Chrome webdriver is downloaded, up to date, and in right path and open.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Site has multiple pages with only changes to page #
i = 1

# Create empty dictionary to fill out with data
le_dict = {"Country": [], "Life Expectancy (Years)": []}

for element in range(3):
    # Pulls google search up
    driver.get(f'http://www.geoba.se/population.php?pc=world&type=015&year=2018&st=country&asde=&page={i}')

    le_table = driver.find_elements(By.TAG_NAME, "tr")
    # Pop off headers and extraneous rows
    le_table = le_table[2:-5]

    # Loop through each line to get data
    for country_line in le_table:
        # Split each text by spaces into list
        country = country_line.text.split(' ')
        # Remove first and last entries
        country = country[1:-1]
        le_dict["Life Expectancy (Years)"].append(float(country[-1]))

        # Get name length
        country_length = len(country) - 1
        # Get only list with name
        name = country[0:country_length]
        le_dict["Country"].append(" ".join(name))

    # Add to i so you can get next page
    i += 1
# Input into df to perform analysis on
df = pd.DataFrame.from_dict(le_dict)
df = df.sort_values("Country", ascending=True)
df.to_csv('life_expectancy.csv')
