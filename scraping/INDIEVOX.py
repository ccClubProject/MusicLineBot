import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def scrape_indievox_events():
    # Initialize WebDriver with options
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()

    # First URL
    url_table = 'https://www.indievox.com/activity/list?type=table&startDate=2024%2F06%2F13&endDate='
    driver.get(url_table)
    driver.implicitly_wait(5)

    # Scroll down the page to load all events
    for i in range(3):
        driver.find_element(By.CSS_SELECTOR, 'html').send_keys(Keys.END)
        time.sleep(3)

    # Find all event elements
    event_elements = driver.find_elements(By.CSS_SELECTOR, '#activityListTab tr')

    # Extract event information
    event_data = []
    for event in event_elements:
        details = event.find_elements(By.TAG_NAME, 'td')
        if len(details) >= 3:
            date = details[0].text
            name = details[1].text
            location = details[2].text
            event_data.append((name, date, location))

    # Find all event links
    links = driver.find_elements(By.CLASS_NAME, "fcLightBlue")
    link_urls = [link.get_attribute("href") for link in links]

    # Close the driver
    driver.close()

    # Combine event information with links
    for i in range(len(event_data)):
        event_data[i] = (*event_data[i], link_urls[i])

    # Re-initialize WebDriver
    driver = webdriver.Chrome(options=option)

    # Second URL
    url_card = 'https://www.indievox.com/activity/list?type=card&startDate=2024%2F06%2F14&endDate='
    driver.get(url_card)
    driver.implicitly_wait(5)

    # Scroll down the page to load all images
    for i in range(30):
        driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
        time.sleep(2)

    # Find all event images
    imgs = driver.find_elements(By.CSS_SELECTOR, ".wrap img")
    img_urls = [img.get_attribute("src") for img in imgs]

    # Close the driver
    driver.close()

    # Combine event information with image URLs
    for i in range(len(event_data)):
        event_data[i] = (*event_data[i], img_urls[i])

    # Create DataFrame
    df = pd.DataFrame(event_data, columns=['EventTime', 'EventName', 'Venue', 'PageURL', 'ImageURL'])

    return df
