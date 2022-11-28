from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Makes sure Chrome webdriver is downloaded, up to date, and in right path and open.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Pulls google search up
driver.get("https://www.google.com/")
driver.find_element(By.NAME, "q").clear()
m = driver.find_element(By.NAME, "q")
query = 'Smart and Final'
# Type in search box
m.send_keys(query)
# Give slight wait to make sure we don't get blocked
# perform Google search with Keys.ENTER
m.send_keys(Keys.ENTER)

time.sleep(3)
m.send_keys(Keys.RETURN)

time.sleep(3)

