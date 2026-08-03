from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
from dotenv import load_dotenv

import os
from modules.exceptions import MaxRetryError, ExpectedResultDoesNotMatchError, AlreadyRespondedToListingError
from modules.listing_details import listingDetails
from modules.filters import sort_by, check_listing

URL = 'https://www.thuisindeachterhoek.nl/'
driver = webdriver.Firefox()
actions = ActionChains(driver)


def get_eligible_listings():
    '''Gets all available listings and removes results user already applied to.'''
    global retries
    max_retries = 3
    driver.get(f'{URL}aanbod/te-huur{sort_by()}')
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '#CybotCookiebotDialogBodyButtonDecline'))).click()
    # get_extra_listings = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, '.match-passendheid')))
    # get_extra_listings.click()
    # time.sleep(1)
    listings = driver.find_elements(By.CLASS_NAME, 'list-item')
    print(f'Total listings found: {len(listings)}')
    available_listings = []

    for listing in listings:
        listingHTML = listing.get_attribute('outerHTML')
        listing_details = listingDetails(listingHTML=listingHTML)
        filter_check = check_listing(
            listing_details=listing_details)
        if not filter_check:
            print('Listing removed from eligible listings: Removed by filters.')
            continue
        elif 'Gereageerd' in listing.text:
            print('Listing removed from eligible listings: Already responded to listing.')
            continue
        else:
            available_listings.append(listing)
    print(f'Found {len(available_listings)} available listings.')
    if len(available_listings) != 0:
        return available_listings
    # returns TypeError after retrying
    else:
        retries += 1
        if retries <= max_retries:
            print(
                f'Making sure there are no listings left...\nRetrying: {retries}/{max_retries}')
            available_listings = get_eligible_listings()
            time.sleep(1)
            return available_listings
        else:
            print('No more eligible listings left')
            return None


get_eligible_listings()
