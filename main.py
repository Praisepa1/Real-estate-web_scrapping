import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urljoin
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)

load_dotenv()

# URL of the Zillow Clone page
zillow_url = "https://appbrewery.github.io/Zillow-Clone/"
form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSdaNsFI_Vp_N65O3iBvstGNEOA8A-vZReladuP_64anUqKZ5A/viewform?usp=sf_link'

# Send an HTTP request to fetch the HTML content of the page
response = requests.get(zillow_url)
response.raise_for_status()  # Raise an error if the request fails

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Lists to store data for each category
links = []
prices = []
addresses = []

# Loop through each listing to extract link, price, and address
for listing in soup.select(".result-list-container"):  # Check if '.list-card-info' is correct
    # Extract all links
    link_tags = listing.select(".property-card-link")  # Using `select` to get all matches
    for link_tag in link_tags:
        link = link_tag['href'] if link_tag else None
        if link:
            link = urljoin(zillow_url, link)  # Convert to absolute URL if it's relative
        links.append(link)

    # Extract all prices
    price_tags = listing.select(".PropertyCardWrapper__StyledPriceLine")  # Using `select` for all matches
    for price_tag in price_tags:
        price = price_tag.get_text(strip=True) if price_tag else None
        if price:
            price = price.split("+")[0]  # Clean the price by removing '+'
            prices.append(price)

    # Extract all addresses
    address_tags = listing.select(".StyledPropertyCardDataArea-anchor address")  # Using `select` for all matches
    for address_tag in address_tags:
        address = address_tag.get_text(strip=True) if address_tag else None
        if address:
            address = address.replace("|", "").strip()  # Clean up the address
            addresses.append(address)

# Display the collected data
print("Links:", links)
print("Prices:", prices)
print("Addresses:", addresses)

# Open the Google Form and get the name attributes of each field
driver.get(form_url)


# Loop through each listing and submit the form
for address, price, link in zip(addresses, prices, links):
    # Open the Google Form
    driver.get(form_url)

    # Fill in the address field
    address_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_field.send_keys(address)

    # Fill in the price field
    price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field.send_keys(price)

    # Fill in the link field
    link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field.send_keys(link)

    # Submit the form
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    # This submits the form

    # Wait a bit to ensure the form submission is processed
    time.sleep(5)

# Close the browser when done
driver.quit()
