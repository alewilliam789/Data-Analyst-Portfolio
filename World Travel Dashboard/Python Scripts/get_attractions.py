from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import pandas as pd


# load data and clean
file_name = "Country_URL_Lookup.csv"
df = pd.read_csv(file_name)
df = df.iloc[:, 0:2]
df = df.set_index("Country Name")
# Send to dictionary
country_dict = pd.DataFrame.to_dict(df, orient="index")
# Makes sure Chrome webdriver is downloaded, up to date, and in right path and open.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Loop through countrties
for key in country_dict:
    # Checks to see if country url is empty and passes if necessary
    try:
        # Grabs URL from dictionary, splits to get site name, and searches
        url = country_dict[key]["URL"]
        website = url.split('.')
        driver.get(url)

        # Checks to see if crazy tourist
        if "thecrazytourist" in website:
            # Grabs attraction text using h2 tag
            attractions = driver.find_elements(By.TAG_NAME, "h2")
            # grabs all pictures using img tag
            pictures = driver.find_elements(By.TAG_NAME, "img")

            # Use i to create dictionary keys and limit the results
            i = 1
            for attraction in attractions:
                if i <= 4:
                    # Creates each attraction key and adds the text from website
                    country_dict[key][f"Attraction {i}"] = attraction.text
                    # Makes sure text has been added and it's right
                    print(country_dict[key][f"Attraction {i}"])
                    i += 1
                else:
                    # When done break loop
                    break
            # Use j to create dictionary keys and limit the results
            j = 1
            for picture in pictures:
                if j <= 4:
                    # Create key and add image url to key
                    country_dict[key][f"Attraction {j} Image"] = picture.get_attribute("src")
                    # Make sure url has been added and right
                    print(country_dict[key][f'Attraction {j} Image'])
                    j += 1
                else:
                    # Break loop when done
                    break
        else:
            # If not crazy tourist pass
            pass
        # Check to see if website is planetware
        if "planetware" in website:

            # Find all attraction text using h2
            attractions = driver.find_elements(By.TAG_NAME, "h2")
            # Use i to create keys and limit amount of attractions
            i = 1
            for attraction in attractions:
                if i <= 4:
                    # Create key and add text
                    country_dict[key][f"Attraction {i}"] = attraction.text
                    # Check to make sure it is added and correct
                    print(country_dict[key][f"Attraction {i}"])
                    i += 1
                else:
                    break
                # Grab images using figure tag
                sections = driver.find_elements(By.TAG_NAME, "figure")
                # Use j to create keys and limit amount of pictures
                j = 1
            for section in sections:
                if j <= 4:
                    # Find images using img tag
                    picture = section.find_element(By.TAG_NAME, "img")
                    # Finally get url using src tag
                    country_dict[key][f"Attraction {j} Picture"] = picture.get_attribute("src")
                    # Check to see if it's added and correct
                    print(country_dict[key][f"Attraction {j} Picture"])
                    j += 1
                else:
                    # Break loop when done
                    break
        else:
            # If not planetware pass
            pass
        # Check to see if website is culture trip
        if "theculturetrip" in website:
            # Find text using h2 tag
            attractions = driver.find_elements(By.TAG_NAME, "h2")
            # Use i to create keys and limit attractions
            i = 1
            for attraction in attractions:
                if i <= 4:
                    # Create key and add attraction
                    country_dict[key][f"Attraction {i}"] = f"{i}. " + attraction.text
                    # Check to see if added and correct
                    print(country_dict[key][f"Attraction {i}"])
                    i += 1
                else:
                    # Break loop when done
                    break
        else:
            # If not culture trip pass
            pass

        time.sleep(5)
    # If no url then pass result
    except AttributeError:
        pass

driver.close()

# Loop through and create list that has url, attractions, and attraction picture urls for each country instead of nested
# dict
country_storage = {}
for key in country_dict:
    country_storage[key] = []
    for j in country_dict[key].keys():
        country_storage[key].append(country_dict[key][j])

# Send to a df to download as a csv for Power BI
df = pd.DataFrame.from_dict(country_storage, orient="index")
df = df.reset_index()
df = df.rename(columns={"index": "Country Name", 0: "URL", 1: "Attraction 1", 2: "Attraction 2", 3: "Attraction 3",
                        4: "Attraction 4", 5: "Attraction 5", 6: "Attraction 1 Picture", 7: "Attraction 2 Picture",
                        8: "Attraction 3 Picture", 9: "Attraction 4 Picture", 10: "Attraction 5 Picture"})
df.to_csv("Country_Attraction_Lookup.csv")

