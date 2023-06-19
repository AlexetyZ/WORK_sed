import fake_useragent
import requests
from bs4 import BeautifulSoup
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from sql import Database
from crypto import Crypto
import re
import logging
from config import SED_Zaytsev_password, SED_Semenova_password, SED_Zaytsev_ID, SED_Semenova_ID, SED_Udalova_password, SED_Udalova_ID, erknm_accounts


logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s',
                    filename=f'logging/{datetime.date.today().strftime("%d.%m.%Y")}.log', encoding='utf-8',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class erknm:
    def __init__(self, headless: bool = False):
        self.options = webdriver.FirefoxOptions()
        # prefs = {'profile.default_content_setting_values': {'images': 2,
        #                                                     'plugins': 2, 'popups': 2, 'geolocation': 2,
        #                                                     'notifications': 2, 'auto_select_certificate': 2,
        #                                                     'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
        #                                                     'media_stream_mic': 2, 'media_stream_camera': 2,
        #                                                     'protocol_handlers': 2,
        #                                                     'ppapi_broker': 2, 'automatic_downloads': 2,
        #                                                     'midi_sysex': 2,
        #                                                     'push_messaging': 2, 'ssl_cert_decisions': 2,
        #                                                     'metro_switch_to_desktop': 2,
        #                                                     'protected_media_identifier': 2, 'app_banner': 2,
        #                                                     'site_engagement': 2,
        #                                                     'durable_storage': 2}}
        # self.options.add_experimental_option('prefs', prefs)
        self.options.add_argument("--disable-native-events")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")

        if headless is True:
            self.options.add_argument("--headless")  # если это включено, то будет в режиме фантома

        # host_dir = 'C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
        # self.options.add_argument('user-data-dir=' + host_dir)
        self.browser = webdriver.Firefox(options=self.options)
        self.browser.set_script_timeout(250)

        logger.info('Начало авторизации')
        # self.Controller(partial(self.autorize))

    def Controller(self, function, extraArgs=''):  # 'Эта функция гарантирует выполнение процессов, давая им 5 попыток.

        popit = 5
        # autorization = 0
        while popit != 0:
            try:

                res = function(*extraArgs)
                if re.search('add_knm', str(function)):
                    return res
                logger.info(f'{str(function)} прошла с {6 - popit} раза')

                # autorization = 1
                break
            except Exception as ex:
                logger.warning(f"Ошибка авторизации: {function} {ex}")

                popit -= 1
                if popit == 0:
                    logger.info(
                        f'{str(function)} не удалась, имеется непредвиденная ошибка, было предпринято 5 попыток')

                    self.browser.quit()
                    return f'{str(function)} не удалась, имеется непредвиденная ошибка, было предпринято 5 попыток'

    def go_to_rpn_inspect_next_year(self):
        next_year = datetime.datetime.now().year + 1

        self.browser.get(f'https://inspect.rospotrebnadzor.ru/{next_year}/')
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "form_search")))

    def get_xl_list_ogrn_for_rpn_inspect(self, ogrn):
        """
        @param ogrn_list:
        @return:
        """

        self.browser.find_element(by=By.ID, value='ogrn').clear()
        self.browser.find_element(by=By.ID, value='ogrn').send_keys(ogrn)
        time.sleep(1)
        self.browser.find_element(by=By.XPATH, value='//*[@id="form_search"]/form/table/tbody/tr[5]/td[2]/input').click()







    def autorize(self):
        self.browser.get('https://private.proverki.gov.ru/private/auth')
        time.sleep(10)
        try:
            WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/main/div/form/div[2]/button[2]'))).click()
        except Exception as ex:
            logger.exception('не получилось, не фартануло')
            try:
                self.browser.find_element(by=By.XPATH, value='//*[@id="details-button"]').click()
                time.sleep(1)
                self.browser.find_element(by=By.XPATH, value='//*[@id="proceed-link"]').click()
                time.sleep(2)
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/main/div/form/div[2]/button[2]'))).click()

            except Exception as ex:

                logger.warning(f'{ex=}')

        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]'))).send_keys(
            str(erknm_accounts['Alexety']['login']))
        self.browser.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(
            str(Crypto().unpack_password(erknm_accounts['Alexety']['password'])))
        # time.sleep(1828293)
        self.browser.find_element(by=By.XPATH, value='/html/body/esia-root/div/esia-login/div/div[1]/form/div[4]/button').click()
        print('контрольная точка 1')


        try:
            time.sleep(3)
            WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div[2]/table/tbody/tr[1]/td[3]/button'))).click()

        except:
            print('не было выбора орагнизации')

        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/header/div/div[2]/button[1]')))
        # ekrnm_button_class = self.browser.find_element(by=By.XPATH,
        #                                                value='//*[@id="root"]/div/header/div/div[2]/button[1]')

        # time.sleep(4456456)
        # while ekrnm_button_class.get_attribute(
        #         'data-active') is None:
        #     ekrnm_button_class.click()
        #
        # self.browser.get('https://private.proverki.gov.ru/private/knms')
        # print('перешли на вкладку КНМ')



        # time.sleep(100000)
        # WebDriverWait(self.browser, 20).until(
        #     EC.visibility_of_element_located((By.ID, 'addButton')))
        self.wait_loader(logger.info('Autorization successfull completed!'))

    def wait_loader(self, func):
        # print('jhsdbf')
        while True:
            time.sleep(2)

            try:
                self.browser.find_element(by=By.CLASS_NAME, value='_LoaderWrap_ksq0q_1')
                # print('еще есть загрузчик')
                time.sleep(2)
            except:
                break
        func


if __name__ == '__main__':
    erknm(headless=True).autorize()
