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
        EC.element_to_be_clickable((By.NAME, 'password')))
    password_entry.click()
    actions.send_keys(password)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    time.sleep(2)


def go_to_overview():
    driver.get(f'{URL}mijn-omgeving/mijn-overzicht')


def check_my_applications():
    '''Returns the num of current applications for houses.'''
    driver.get(
        f'{URL}mijn-omgeving/woning-zoeken/mijn-reacties/advertenties-online')
    time.sleep(2)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'reactie')))
    responses = driver.find_elements(By.CLASS_NAME, 'reactie')
    responses.pop()  # removes "see relevant offers"
    return len(responses)


def get_eligible_listings():
    '''Gets all available listings and removes results user already applied to.'''
    driver.get(f'{URL}aanbod/te-huur')
    time.sleep(1)
    get_extra_listings = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.match-passendheid')))
    get_extra_listings.click()
    time.sleep(1)
    listings = driver.find_elements(By.CLASS_NAME, 'list-item')
    print(f'Total listings found: {len(listings)}')
    available_listings = []
    for listing in listings:
        if 'Gereageerd' in listing.text:
            print('ALREADY APPLIED!!')
        else:
            available_listings.append(listing)
    print(f'Found {len(available_listings)} available listings')
    time.sleep(2)
    return available_listings


def apply_for_listing():
    global num_of_applications
    scroll_to_respond_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.ng-scope:nth-child(5)')))
    scroll_to_respond_button.click()
    respond_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.reageer-button')))
    # TODO: BUTTON FOR DELETEN APPLICATION HAS THE SAME CSS SELECTOR, CHECK IF 'Reageer' in button.text?
    respond_button.click()
    num_of_applications += 1
    time.sleep(2)


log_in()
print('logged in, checking applications...')
num_of_applications = check_my_applications()
time.sleep(2)
while num_of_applications < MAX_RESPONSES:
    eligible_listings = get_eligible_listings()
    print(eligible_listings[0].text)
    eligible_listings[0].click()
    # TODO Program sees extra listings (good) but doesn't click on them. returns TimeoutException
    print('Applying...')

    apply_for_listing()
    print('applied for listing!')
    print(f'Current number of applications: {num_of_applications}')
    print('----------------------------------------------------------------')
    time.sleep(1)
print('No more applications left.')
print(f'Total applications should be: {num_of_applications}')
print('Checking...')
recheck_applications = check_my_applications()
print(f'Total applications: {recheck_applications}')

if num_of_applications != recheck_applications:
    print('Something has gone wrong...')

time.sleep(10000)
