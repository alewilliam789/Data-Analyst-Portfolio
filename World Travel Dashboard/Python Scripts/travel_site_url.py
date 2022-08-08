from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from random import randint


# Function to grab url results from page
def country_url(search_results, country_dict, key, number=1):
    # Create empty strings for urls
    cr_url = ''
    pw_url = ''
    ct_url = ''
    # Loop for each result generated from the search
    for search_result in search_results:
        # Remove extra results that don't have direct url
        if "google" and "googleusercontent" not in str(search_result.get_attribute("href")).split("."):
            # Checks to see if url is crazy tourist
            if "thecrazytourist" in str(search_result.get_attribute("href")).split("."):
                # Assigns to c_url for comparison
                cr_url = str(search_result.get_attribute("href"))
            else:
                pass
            # Checks to see if url is planetware
            if 'planetware' in str(search_result.get_attribute("href")).split("."):
                # Assigns to pw_url for comparison
                pw_url = str(search_result.get_attribute("href"))
            else:
                pass
            # Checks to see if culture trip
            if 'theculturetrip' in str(search_result.get_attribute("href")).split("."):
                # Assigns to ct_url for comparison
                ct_url = str(search_result.get_attribute("href"))
            else:
                pass

        # If each string has a value, preferably want crazy tourist site
        if len(pw_url) and len(cr_url) and len(ct_url) > 0:
            country_dict[key] = cr_url
        # If only crazy tourist use url
        elif len(cr_url) > 0:
            country_dict[key] = cr_url
        # If only planetware use url
        elif len(pw_url) > 0:
            country_dict[key] = pw_url
        # If only culture trip use url
        elif len(ct_url) > 0:
            country_dict[key] = ct_url
        else:
            pass

    # Check to make sure there are search results
    if (pw_url and cr_url and ct_url == '') and number == 1:
        # Click on 2nd page with Selenium
        driver.find_element(By.LINK_TEXT, "2").click()
        # Pass number 2 to make sure there isn't an endless loop
        number = 2
        # Grab all search results from 2nd page
        country_search_results = driver.find_elements(By.TAG_NAME, "a")
        # Feed back into function to grab 2nd page url results
        country_dict = country_url(country_search_results, country_dict, key, number)
    else:
        pass

    return country_dict


# load data and clean
file_name = "Arrival_Numbers.csv"
df = pd.read_csv(file_name)
df = df.dropna(axis=1, thresh=((len(df.index)) / 2))
df = df.dropna(axis=0, how='any')

# Split to a numpy array so that I can store points for plotting.
mr_array = df.to_numpy()

# Create empty dictionary to store all the countries and information
Country_storage = {}

# Iterate to add new entries for available countries into dictionary
country_storage = {}
for row in mr_array:
    Country_data = row
    Country_name = Country_data[0]
    country_storage[Country_name] = None

# Makes sure Chrome webdriver is downloaded, up to date, and in right path and open.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Pulls google search up
driver.get("https://www.google.com")

# Loop through each country
for key in country_storage:
    # identify search box
    driver.find_element(By.NAME, "q").clear()
    m = driver.find_element(By.NAME, "q")
    # enter search text
    query = f"Top 10 things to see in {key}"
    # Type in search box
    m.send_keys(query)
    # Give slight wait to make sure we don't get blocked
    time.sleep(5)
    # perform Google search with Keys.ENTER
    m.send_keys(Keys.ENTER)
    # Pull all urls using a tag
    search_results = driver.find_elements(By.TAG_NAME, "a")
    # Feed into function to get results/dictionary
    country_storage = country_url(search_results=search_results, country_dict=country_storage, key=key)
    time.sleep(randint(1, 5))

driver.close()
# Create pandas dataframe and send it to a csv to use in Power BI
df = pd.DataFrame.from_dict(country_storage, orient="index", columns=["URL"])
df = df.reset_index()
df = df.rename(columns={"index": "Country Name"})
df.to_csv('Country_URL_Lookup.csv')
