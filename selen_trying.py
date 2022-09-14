import fake_useragent
import requests
from bs4 import BeautifulSoup
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from sql import Database

from config import SED_Zaytsev_password, SED_Semenova_password, SED_Zaytsev_ID, SED_Semenova_ID, SED_Udalova_password, SED_Udalova_ID

browser = webdriver.Firefox()
browser.get('https://sed.rospotrebnadzor.ru/auth.php?uri=%2F')
WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="organization_show"]')))
browser.find_element(By.XPATH, '//*[@id="organization_show"]').click()
org = browser.find_element(By.XPATH, '//*[@id="organizations"]')
org.send_keys('Управление Роспотребнадзора по Нижегородской области')
time.sleep(1)
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
org.send_keys(Keys.DOWN)
org.send_keys(Keys.ENTER)

spec = browser.find_element(By.XPATH, '//*[@id="logins"]')
spec.clear()
spec.send_keys('Удалова Т.А.')
time.sleep(1)
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
spec.send_keys(Keys.DOWN)
spec.send_keys(Keys.ENTER)
password = browser.find_element(By.XPATH, '//*[@id="password_input"]')
password.send_keys(SED_Udalova_password)

