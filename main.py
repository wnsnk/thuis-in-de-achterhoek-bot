from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
from dotenv import load_dotenv
import os
from modules.exceptions import MaxRetryError, ExpectedResultDoesNotMatchError, AlreadyRespondedToListingError
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
    driver.get(f'{URL}aanbod/te-huur#?gesorteerd-op=reactiedatum-')
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
            continue
        else:
            available_listings.append(listing)
    print(f'Found {len(available_listings)} available listings.')
    if len(available_listings) != 0:
        return available_listings
    else:
        # TODO Find a good way to retry this
        get_eligible_listings()
        time.sleep(1)


def apply_for_listing():
    global num_of_applications
    print('Applying...')
    scroll_to_respond_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.ng-scope:nth-child(5)')))
    scroll_to_respond_button.click()
    respond_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.reageer-button')))
    # Button for removing application has the same CSS Selector.
    # This piece of code makes sure it doesn't accidentally remove your application.
    if respond_button.get_attribute('value') == 'Reageer':
        respond_button.click()
        num_of_applications += 1
        time.sleep(2)
        print('applied for listing!')
    else:
        raise AlreadyRespondedToListingError(
            'Already responded to this listing.')

# TODO Write retry function?


log_in()
print('logged in, checking applications...')
num_of_applications = check_my_applications()
print(
    f'Current number of applications: {num_of_applications}/{MAX_RESPONSES}')
time.sleep(2)
while num_of_applications < MAX_RESPONSES:
    eligible_listings = get_eligible_listings()

    print(eligible_listings[0].text)
    # program sometimes does not register clicking eligible_listings[0]. It will retry 6 times.
    clicked = False
    retries = 0
    max_retries = 6
    while not clicked:
        eligible_listings[0].click()
        time.sleep(3)
        if driver.current_url == f'{URL}aanbod/te-huur#?gesorteerd-op=reactiedatum-':
            print('did not click')
            time.sleep(1)
            retries += 1
            print(f'Retries: {retries}/{max_retries}')
            if retries == 3:
                print('Trying to reload eligible listings.')
                eligible_listings = get_eligible_listings()
                time.sleep(3)
                print(eligible_listings[0].text)
            if retries >= max_retries:
                print('Something went wrong.')
                raise MaxRetryError(f'Program failed after {retries} retries')

        else:
            clicked = True

    apply_for_listing()
    print(
        f'Current number of applications: {num_of_applications}/{MAX_RESPONSES}')
    print('----------------------------------------------------------------')
    time.sleep(1)
print('No more applications left.')
print(f'Total applications should be: {num_of_applications}')
print('Checking...')
recheck_applications = check_my_applications()
print(f'Total applications: {recheck_applications}')

if num_of_applications != recheck_applications:
    raise ExpectedResultDoesNotMatchError(
        'Something has gone wrong. Please check applications manually.')


time.sleep(10000)
