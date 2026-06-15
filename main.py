from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
# Source - https://stackoverflow.com/a/32887994
# Posted by Saurabh Shrivastava, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-15, License - CC BY-SA 4.0

from selenium.webdriver.common.action_chains import ActionChains


import time
from dotenv import load_dotenv
import os

load_dotenv()

URL = 'https://www.thuisindeachterhoek.nl/'
username = os.getenv('THUIS_IN_DE_ACHTERHOEK_USERNAME')
password = os.getenv('THUIS_IN_DE_ACHTERHOEK_PASSWORD')
driver = webdriver.Firefox()
actions = ActionChains(driver)

driver.get(URL)
# driver.implicitly_wait(30)

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, '#CybotCookiebotDialogBodyButtonDecline'))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, '.login-plugin-container'))).click()


def log_in():
    username_entry = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'username')))
    username_entry.click()
    actions.send_keys(username)
    actions.perform()
    password_entry = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'password'))).click()
    actions.send_keys(password)
    # actions.perform()
    actions.send_keys(Keys.RETURN)
    actions.perform()


log_in()
time.sleep(10000)
