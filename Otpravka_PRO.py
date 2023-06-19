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
from selenium.webdriver.chrome.service import Service

from config import SED_Zaytsev_password, SED_Semenova_password, SED_Zaytsev_ID, SED_Semenova_ID, SED_Udalova_password, SED_Udalova_ID


class Otpravka():
    def __init__(self, rang):
        self.options = Options()
        self.options.set_preference("dom.webnotifications.enabled", False)
        self.options.add_argument("--headless")  # если это включено, то будет в режиме фантома

        self.akkaunt = 'Удалова Т.А'
        self.password = SED_Udalova_password
        self.SED_ID = SED_Udalova_ID

        self.rang = rang

        # 'C:\\Users\\user\\Documents\\документы\\Взятые номера согласований.xlsx' = 'C:\\Users\\user\\Documents\\документы\\Взятые номера согласований.xlsx'
        # 'C:\\Users\\user\\Documents\\документы\\Номера постановлений.xlsx' = 'C:\\Users\\user\\Documents\\документы\\Номера постановлений.xlsx'

        # self.session = requests.Session()
        # self.user = fake_useragent.UserAgent().random
        #
        # self.header = {
        #     'user-agent': self.user
        # }
        # self.login_request()

        # self.Controller()

    def Controller(self):
        self.options = webdriver.ChromeOptions()
        binary_yandex_driver_file = 'C://Users//user//PycharmProjects//WORK_sed//yandexdriver.exe'  # path to YandexDriver
        browser_service = Service(executable_path=binary_yandex_driver_file)

        # options.add_argument('--headless')
        self.options.add_argument('--ignore-certificate-errors-spki-list')
        self.options.add_argument("disable-infobars")

        # choise nachalnik or get default

        # self.choise_nachalnik()
        self.nachalnik = 'Бернюкова И.В.'

        # self.options.add_argument("--headless")  # если это включено, то будет в режиме фантома

        while True:
            try:
                self.browser = webdriver.Chrome(service=browser_service, options=self.options)
                time.sleep(1)
                self.browser.get('https://sed.rospotrebnadzor.ru/auth.php?uri=%2F')
                break

            except Exception as ex:
                print(ex)
                time.sleep(1)

        self.browser.find_element(by=By.XPATH, value='//*[@id="primary-button"]').click()

        WebDriverWait(self.browser, 100000).until(EC.element_to_be_clickable((By.ID, 'details-button'))).click()
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, 'proceed-link'))).click()


        popit = 5
        autorization = 0
        while popit != 0:
            try:

                self.Autorization()
                print(f'авторизация прошла с {6 - popit} раза')
                autorization = 1
                break
            except:

                popit -= 1
                if popit == 0:
                    print('Авторизация не удалась, имеется непредвиденная ошибка, было предпрпинято 5 попыток')
        if autorization == 0:
            print('Не ликуем, необходимо залезть под капот и починить')
        if autorization == 1:
            self.Sending()

    def Autorization(self):

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
        spec.clear()
        spec.send_keys(self.akkaunt)
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
        spec.send_keys(Keys.DOWN)
        spec.send_keys(Keys.ENTER)
        password = self.browser.find_element(By.XPATH, '//*[@id="password_input"]')
        password.send_keys(self.password)
        self.browser.find_element(By.XPATH, '/html/body/div[5]/div[2]/form/table/tbody/tr[8]/td[2]/button').click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[3]/div[1]/div/div[4]/div/div/button/i')))

    def Sending(self):

        a = self.browser.find_element(By.XPATH,
                                      '/html/body/div[6]/div[3]/div[1]/div/div[4]/div/div/ul[1]/li/a').get_attribute(
            'href')
        DNSID = a.replace('https://sed.rospotrebnadzor.ru/document.php?all=1&category=6&DNSID=', '')

        for i in self.rang:

            sadik_id = int(i[14])
            sadik = Database().get_sadik_info(sadik_id)
            id_o = i[0]
            nsogl = i[12]
            email = sadik[0][6]
            komu = sadik[0][3]


            href_nsogl = nsogl.replace('согл', '')

            url = f'https://sed.rospotrebnadzor.ru/?DNSID={DNSID}&frmsearch=get&search=&search=%F1%EE%E3%EB{href_nsogl}'
            self.browser.get(url)


            N_doc = self.browser.find_element(By.XPATH, value='//*[@id="mtable"]/tbody/tr[1]').get_attribute('data-docid')

            npost = self.browser.find_element(By.CSS_SELECTOR,
                                           'tr.document-list__tr:nth-child(1) > td:nth-child(5) > a:nth-child(1) > div:nth-child(1)').text

            self.browser.get(
                f'https://sed.rospotrebnadzor.ru/web/?url=document-send&id={N_doc}&category=9&DNSID={DNSID}')
            # self.browser.switch_to.window(self.browser.window_handles[1])
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
            try:
                self.browser.find_element(By.CSS_SELECTOR, '#email').click()
                self.browser.find_element(By.CSS_SELECTOR, '#email').send_keys(email, ', ntygaz@gmail.com')
            except:
                print('Перезапуск поиска e-mail')
                self.browser.find_element(By.CSS_SELECTOR, '#email').click()
                time.sleep(2)
                self.browser.find_element(By.CSS_SELECTOR, '#email').send_keys(email, ', ntygaz@gmail.com')

            for vniz in range(15):
                self.browser.find_element(By.TAG_NAME, 'html').send_keys(Keys.DOWN)
            time.sleep(0.5)
            self.browser.find_element(By.XPATH, '//*[@id="card"]').click()
            self.browser.find_element(By.XPATH, '//*[@id="signed_document"]').click()
            self.browser.find_element(By.XPATH, '//*[@id="subject"]').click()
            self.browser.find_element(By.XPATH, '//*[@id="subject"]').send_keys(Keys.SPACE)
            self.browser.find_element(By.XPATH, '//*[@id="subject"]').send_keys(Keys.SPACE)
            self.browser.find_element(By.XPATH, '//*[@id="subject"]').send_keys(komu)

            self.browser.find_element(By.XPATH, '//*[@id="message"]').clear()
            self.browser.find_element(By.XPATH, '//*[@id="message"]').click()
            self.browser.find_element(By.XPATH, '//*[@id="message"]').send_keys(
                "ВНИМАНИЕ! Просьба, не отвечать на данное сообщение и ничего не писать на этот адрес. Домен no-reply@rospotrebnadzor.ru работает только на рассылку готовых документов.\nДля ответа или отправки просьба направлять на адреса: ntygaz@yandex.ru, vy050@mts-nn.ru. Спасибо, что приняли данный текст во внимание!")
            self.browser.find_element(By.XPATH, '/html/body/div[5]/form/div[2]/div/div[1]/input').click()

            Database().assign_number(id_o, npost)
            Database().level_up_status(id_o, 'registred')
            print('письмо доставлено, строка ', i)
            print(' ')

        print('Доставка завершена')
        self.Kill_firefox()

    # def login_request(self):
    #     link = 'https://sed.rospotrebnadzor.ru/auth.php?group_id=3204'
    #     apply_link = 'https://sed.rospotrebnadzor.ru/document.php?all=1&c_user_status=0&dcv_status=1&category=6&DNSID=wXwaCw5PYykCpa7Zla8AjhQ'
    #     revision_link = 'https://sed.rospotrebnadzor.ru/document.php?all=1&c_user_status=1&category=6&DNSID=w9gfvomxjNRwo_HbkP_MOCg'
    #     registred_link = 'https://sed.rospotrebnadzor.ru/document.php?all=1&c_user_status=2&c_user_status_type=1&category=6&DNSID=w9gfvomxjNRwo_HbkP_MOCg'
    #
    #     data = {
    #         'DNSID': 'wqx7cahFJjk6x2QyA8VYkQg',
    #         'group_id': '32043',
    #         'user_id': self.SED_ID,
    #         'password': self.password,
    #         'x': '1',
    #
    #     }
    #
    #     response = self.session.post(link, data=data, headers=self.header)



    def Kill_firefox(self):
        os.system('Taskkill /IM firefox.exe /F')
    # def get_href(self, url):
    #     get = self.session.get(url, headers=self.header)
    #     get_soup = BeautifulSoup(get.text, 'lxml')
    #     # print(get_soup)
    #
    #     N_doc = get_soup.find('tbody').find_all('tr')[0].get('data-docid')
    #     return N_doc


if __name__ == '__main__':
    Otpravka().Autorization()