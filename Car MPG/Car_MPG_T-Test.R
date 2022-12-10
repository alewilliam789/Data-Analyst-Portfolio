#Install packages
library(rvest)
library(tidyverse)
#Scrape html from fueleconomy.gov
car_2022 = read_html("https://www.fueleconomy.gov/feg/byclass/Large_Cars2022.shtml")

#Section off div which contains the car sections
divers = car_2022 %>% html_elements("div")

#Grab each element using class name for gas cars or hybrids
gasmpgClass = divers %>% html_elements("[class='mpgSummary fuel1']")

#Grab text from those elements and store in character vector
gasmpg_2022 = gasmpgClass %>% html_text()

#Remove the newline and tab characters that clutter up string
gasmpg_2022 = str_remove_all(gasmpg_2022,"[\r\n]")
gasmpg_2022 = str_remove_all(gasmpg_2022,"[\r\t]")

#Take the mpg numbers from the text
gasmpg_2022 = substr(gasmpg_2022,14,15)

#Turn character vector into numeric
gasmpg_2022 = as.integer(gasmpg_2022)


# Finally we can answer the question of whether the average mpg for cars has gone up since the mtcars database
#Grab random sample for T-test. Used sample size of 40 to satisfy conditions
#conditions for t-test.
sample_2022 = sample(gasmpg_2022,size= 32)

#Plotted sample to reaffirm belief of skewed distribution.
sample_plot = hist(sample_2022, main = "Distribution of 2022 Car's MPG",breaks=5)
sample_box = boxplot(sample_1974, sample_2022)


#Grabbed mean mpg of cars in mtcars database.
#Hypothesis test assumption is that mtcars used a random sample
sample_1974 = as.integer(sample(mtcars[["mpg"]]))

#Determine if variance is equal
var.test(sample_1974, sample_2022)

#1-Sample T-test using the alternative assumption that the mpg of the 2022
t.test(sample_2022, sample_1974, var.equal = FALSE, alternative = 'greater')
