from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from dotenv import load_dotenv
import os

load_dotenv()

URL = 'https://www.thuisindeachterhoek.nl/'
MAX_RESPONSES = 3
can_respond = False
username = os.getenv('THUIS_IN_DE_ACHTERHOEK_USERNAME')
password = os.getenv('THUIS_IN_DE_ACHTERHOEK_PASSWORD')
driver = webdriver.Firefox()
actions = ActionChains(driver)


def log_in():
    driver.get(URL)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '#CybotCookiebotDialogBodyButtonDecline'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.login-plugin-container'))).click()
    time.sleep(1)
    username_entry = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'username')))
    username_entry.click()

    actions.send_keys(username)
    actions.perform()
    password_entry = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'password'))).click()
    actions.send_keys(password)
    actions.send_keys(Keys.RETURN)
    actions.perform()


def go_to_overview():
    driver.get(f'{URL}mijn-omgeving/mijn-overzicht')


def check_my_applications():
    '''Returns the num of current applications for houses.'''
    my_applications_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.dashboard-menu:nth-child(3) > li:nth-child(2)')))
    my_applications_button.click()
    time.sleep(2)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'reactie')))
    responses = driver.find_elements(By.CLASS_NAME, 'reactie')
    responses.pop()  # removes "see relevant offers"
    return len(responses)


def get_eligible_listings():
    '''Gets all available listings and removes results user already applied to.'''
    driver.get(f'{URL}aanbod/te-huur')
    get_extra_listings = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.match-passendheid')))
    get_extra_listings.click()
    listings = driver.find_elements(By.CLASS_NAME, 'list-item')
    for listing in listings:
        if 'Gereageerd (mijn voorlopige positie' in listing.text:
            listings.remove(listing)
            print('ALREADY APPLIED!!')

    print(f'Found {len(listings)} available listings')
    return listings


log_in()
num_of_applications = check_my_applications()
if num_of_applications < MAX_RESPONSES:
    can_respond = True
    eligible_listings = get_eligible_listings()
    # get urls from listing and apply
    # update num of applications

time.sleep(10000)
