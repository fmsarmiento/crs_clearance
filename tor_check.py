from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd, time
from tor_config import *
from telegram.ext import Updater
from datetime import datetime

def sendNotification(msg, CHAT_ID, TOKEN):
    for accts in CHAT_ID:
        try:
            updater = Updater(token=TOKEN, use_context=True)
            updater.bot.send_message(chat_id=accts, text=msg)
        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%d-%m %H:%M:%S')}: An error occured with notification sending: {e}")

# 1. Constants - We need to always do this
website = 'https://crs.upd.edu.ph/'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={userAgent}')
print("Your user agent for this run is: ",userAgent)
options.headless = headless_mode
options.add_argument('window-size=1920x1080')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(website)
# driver.maximize_window()

# 2. Login
time.sleep(1)
username_input = driver.find_element(By.XPATH, '//input[contains(@id,"txt_login")]')
username_input.send_keys(username)
time.sleep(1)
password_input = driver.find_element(By.XPATH, '//input[contains(@id,"pwd_password")]')
password_input.send_keys(password)
time.sleep(1)
login_button = driver.find_element(By.XPATH,'//form[contains(@id,"login-form")]//input[contains(@value,"Login")]')
login_button.click()
time.sleep(3)

# Checking for University Clearance
driver.get("https://crs.upd.edu.ph/clearance_mgmt")
time.sleep(2)
credentials = driver.find_elements(By.XPATH, '//table[contains(@class,"form")]//td')
print(f"DATE APPLIED: {credentials[0].text} | STATUS: {credentials[1].text} | DATE CLEARED: {credentials[2].text} | CLEARED AS OF: {credentials[3].text}")
if do_notify:
    sendNotification(f"[CRS UNIVERSITY CLEARANCE UPDATE]\nDATE APPLIED: {credentials[0].text} | STATUS: {credentials[1].text} | DATE CLEARED: {credentials[2].text} | CLEARED AS OF: {credentials[3].text}",mailto, token)
    if "NOT YET CLEARED" not in credentials[2].text: sendNotification(f"[CRS UNIVERSITY CLEARANCE UPDATE] CRS clearance updated. Check it now!",mailto, token)
driver.quit()