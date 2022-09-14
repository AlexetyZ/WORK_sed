import os.path

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium.common import exceptions
from selenium.webdriver.support.select import Select
import pickle

from config import SED_Udalova_password, SED_Zhikova_password, SED_Zaytsev_password

import undetected_chromedriver
perols = {
    'Удалова Т.А': SED_Udalova_password,
    'Зайцев А.Д': SED_Zaytsev_password,
    'Жукова И.В': SED_Zhikova_password,
}


class SED_operations:
    def __init__(self):
        pass

    def Autorize(self, user):
        self.options = webdriver.ChromeOptions()
        exists_cookie = 0
        if os.path.exists('cookies.json'):
            exists_cookie = 1
        self.akkaunt = user
        password = perols[user]
        binary_yandex_driver_file = 'C://Users//user//PycharmProjects//WORK_sed//yandexdriver.exe' # path to YandexDriver
    
        browser_service = Service(executable_path=binary_yandex_driver_file)
    
        # options.add_argument('--headless')
        self.options.add_argument('--ignore-certificate-errors-spki-list')
        self.options.add_argument("disable-infobars")
        # host_dir = 'C:\\Users\\user\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default'
        # options.add_argument(f'user-data-dir={host_dir}')
        time.sleep(3)
        while True:
            try:
    
                self.browser = webdriver.Chrome(service=browser_service, options=self.options)
    
                time.sleep(1)
                self.browser.get('https://sed.rospotrebnadzor.ru/auth.php?uri=%2F')
                if exists_cookie == 1:
                    try:
                        with open('cookies.json', 'r', newline='') as inputdata:
    
                            cookies = json.load(inputdata)
                            for cookie in cookies:
                                self.browser.add_cookie(cookie)
    
                            self.browser.refresh()
                    except:
                        pass
                break
    
            except exceptions.InvalidCookieDomainException as ex:
                print(ex)
                self.browser.quit()
                time.sleep(1)
    
        self.browser.find_element(by=By.XPATH, value='//*[@id="primary-button"]').click()
    
        WebDriverWait(self.browser, 100000).until(EC.element_to_be_clickable((By.ID, 'details-button'))).click()
        time.sleep(2)
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, 'proceed-link'))).click()
        WebDriverWait(self.browser, 1000).until(
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
        spec.clear()
        spec.send_keys(self.akkaunt)
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
        spec.send_keys(Keys.DOWN)
        spec.send_keys(Keys.ENTER)
        passw = self.browser.find_element(By.XPATH, '//*[@id="password_input"]')
        passw.send_keys(password)
        self.browser.find_element(By.XPATH, '/html/body/div[5]/div[2]/form/table/tbody/tr[8]/td[2]/button').click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[3]/div[1]/div/div[4]/div/div/button/i')))
        if exists_cookie == 0:
            cookie = self.browser.get_cookies()
            with open('cookies.json', 'w', newline='') as file:
                json.dump(cookie, file)
            print(cookie)
        self.dnsid = self.browser.find_element(By.XPATH, value='//*[@id="pffrmsearch"]/input[1]').get_attribute('value')
        self.user = user
        return self

    def send_PVR(self):
        self.browser.get(f'https://sed.rospotrebnadzor.ru/document.card.php?category=4&DNSID={self.dnsid}')
        self.choose_case('15 27 Внутренняя переписка')
        self.add_signature(self.user)
        self.add_executor(self.user)
        self.add_inner_recipient('Шарабакина М.А', 'Никитина Ю. А', 'Ексина М.А', 'Агапова А.В')
        self.add_document_kind('Служебная записка')
        self.add_short_describe('Сведения ПВР')


        print('отправляем списки')


    def choose_case(self, case):
        self.browser.find_element(By.XPATH, value='//*[@id="maintable"]/tbody/tr[2]/td[2]/div/a').click()
        self.browser.find_element(By.XPATH, value='//*[@id="maintable"]/tbody/tr[2]/td[2]/div/div/div/div[2]/input').send_keys(case)
        WebDriverWait(self.browser, 50).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="maintable"]/tbody/tr[2]/td[2]/div/div/ul/li[2]'))).click()

    def add_signature(self, signature):
        self.browser.find_element(By.ID, value='inp_g_su_a_0').send_keys(signature)
        WebDriverWait(self.browser, 50).until(EC.visibility_of_element_located((By.ID, 'fio_0'))).click()

    def add_executor(self, executor):
        self.browser.find_element(By.ID, value='inp_SuPreparedBy').send_keys(executor)
        WebDriverWait(self.browser, 50).until(EC.visibility_of_element_located((By.ID, 'fio_0'))).click()

    def add_inner_recipient(self, *recipients):
        for n, recipient in enumerate(recipients):
            while True:
                try:
                    rec_input = self.browser.find_element(By.ID, value=f'inp_g_su_r_{n}')
                    break
                except:
                    self.browser.find_element(By.ID, value='add-recipient-button').click()
                    rec_input = self.browser.find_element(By.ID, value=f'inp_g_su_r_{n}')
            rec_input.send_keys(recipient)
            WebDriverWait(self.browser, 50).until(EC.visibility_of_element_located((By.ID, 'fio_0'))).click()

    def add_document_kind(self, kind):
        self.browser.find_element(By.ID, 'document_kind').click()
        Select(self.browser.find_element(By.ID, 'document_kind')).select_by_visible_text(kind)

    def add_short_describe(self, text):
        self.browser.find_element(By.ID, value='short_content').send_keys(text)




        

if __name__ == '__main__':
    SED_operations().Autorize()


