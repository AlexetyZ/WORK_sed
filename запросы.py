import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import os
import re


# selen

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from config import SED_Zaytsev_password, SED_Semenova_password, SED_Zaytsev_ID, SED_Semenova_ID, SED_Udalova_password, SED_Udalova_ID


class Req:
    def __init__(self):
        self.session = requests.Session()
        self.user = fake_useragent.UserAgent().random
        self.header = {
            'user-agent': self.user
        }

        # for selen
        self.options = Options()
        self.options.set_preference("dom.webnotifications.enabled", False)
        self.akkaunt = 'Удалова Т.А'
        self.password = SED_Udalova_password
        self.SED_ID = SED_Udalova_ID

        # self.selen()
        nsogl = 'согл-216576326-1'
        self.login_request()
        self.req(nsogl)



    def req(self, nsogl):


        n = re.split('огл-', nsogl)[1]
        link = f'https://sed.rospotrebnadzor.ru/?DNSID=wqx7cahFJjk6x2QyA8VYkQg&frmsearch=get&search=&search=%F1%EE%E3%EB-{n}'
        try_find_sogl = self.session.get(link)
        soup_try_find_sogl = BeautifulSoup(try_find_sogl.text, 'lxml')
        link_to_doc = f"https://sed.rospotrebnadzor.ru/{soup_try_find_sogl.find('a', {'class': 'td_inner s-table__clamping main_doc_table-doc-number'}).get('href')}"
        doc = self.session.get(link_to_doc)
        soup_doc = BeautifulSoup(doc.text, 'lxml')

        print(re.search('На подписании', doc.text))


    def login_request(self):
        link = 'https://sed.rospotrebnadzor.ru/auth.php?group_id=3204'
        apply_link = 'https://sed.rospotrebnadzor.ru/document.php?all=1&c_user_status=0&dcv_status=1&category=6&DNSID=wXwaCw5PYykCpa7Zla8AjhQ'
        revision_link = 'https://sed.rospotrebnadzor.ru/document.php?all=1&c_user_status=1&category=6&DNSID=w9gfvomxjNRwo_HbkP_MOCg'
        registred_link = 'https://sed.rospotrebnadzor.ru/document.php?all=1&c_user_status=2&c_user_status_type=1&category=6&DNSID=w9gfvomxjNRwo_HbkP_MOCg'

        data = {
            'DNSID': 'wqx7cahFJjk6x2QyA8VYkQg',
            'group_id': '32043',
            'user_id': self.SED_ID,
            'password': self.password,
            'x': '1',

        }

        response = self.session.post(link, data=data, headers=self.header)
    def selen(self):
        self.browser = webdriver.Firefox(options=self.options)
        self.browser.get('https://sed.rospotrebnadzor.ru/auth.php?uri=%2F')
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="organization_show"]')))
        self.browser.find_element(By.XPATH, '//*[@id="organization_show"]').click()
        org = self.browser.find_element(By.XPATH, '//*[@id="organizations"]')
        org.send_keys('Управление Роспотребнадзора по Нижегородской области')
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
        org.send_keys(Keys.DOWN)
        org.send_keys(Keys.ENTER)

        spec = self.browser.find_element(By.XPATH, '//*[@id="logins"]')
        spec.send_keys(self.akkaunt)
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
        spec.send_keys(Keys.DOWN)
        spec.send_keys(Keys.ENTER)
        password = self.browser.find_element(By.XPATH, '//*[@id="password_input"]')
        password.send_keys(self.password)
        self.browser.find_element(By.XPATH,
                                  '/html/body/div[5]/div/div[2]/form/table/tbody/tr[8]/td[2]/input[1]').click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[2]/span[1]')))


if __name__ == "__main__":
    print("jkhasc")
    Req()
