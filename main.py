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
    get_extra_listings = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.match-passendheid')))
    get_extra_listings.click()
    listings = driver.find_elements(By.CLASS_NAME, 'list-item')
    for listing in listings:
        if 'Gereageerd' in listing.text:
            listings.remove(listing)
            print('ALREADY APPLIED!!')

    print(f'Found {len(listings)} available listings')
    time.sleep(2)
    return listings


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
    can_respond = True
    eligible_listings = get_eligible_listings()
    print(eligible_listings[0].text, '\n')
    print('try applying...')
    eligible_listings[0].click()
    apply_for_listing()
    print('applied for listing!')
    print(f'Current number of applications: {num_of_applications}')
print('loop ended')

total = check_my_applications()
print(f'Total applications: {total}')

time.sleep(10000)
