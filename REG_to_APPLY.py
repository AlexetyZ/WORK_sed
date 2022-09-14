import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

import time
import os

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from config import SED_Udalova_password, SED_Zhikova_password

from collections import OrderedDict
import re
import pymorphy2
import jinja2
from docxtpl import DocxTemplate
from sql import Database

"""Данный класс принимает кортеж из направленных элементов (элемент - совокупность данных об одном случае закрытия конкретного учреждения)"""


class Registration_sadik():
    def __init__(self, rang):

        self.akkaunt = 'Удалова Т.А.'
        self.rang = rang
        self.path = os.path.dirname(__file__)
        self.password = SED_Udalova_password
        self.start_menu()

    def start_menu(self):

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
        self.Controller()
        # self.Autorization()

    def choise_nachalnik(self):
        N = input('Введине первую букву фамилии начальника (нижний регистр)')
        if N == 'н':
            self.nachalnik = 'Назарова М.М.'
        if N == 'б':
            self.nachalnik = 'Бернюкова И.В.'
        if N == 'ж':
            self.nachalnik = 'Жовин П.Г.'
        return self.nachalnik

    def Controller(self):

        popit = 5
        autorization = 0
        while popit != 0:
            try:
                self.Autorization()
                print(f'авторизация прошла с {6 - popit} раза')
                autorization = 1
                break
            except Exception as ex:

                popit -= 1
                if popit == 0:
                    print(f'Авторизация не удалась, имеется непредвиденная ошибка, было предпрпинято 5 попыток: {ex}')
        if autorization == 0:
            print('Не ликуем')
        if autorization == 1:
            print('Ликуем')
            self.Registration()

    def Autorization(self):

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
        password = self.browser.find_element(By.XPATH, '//*[@id="password_input"]')
        password.send_keys(self.password)
        self.browser.find_element(By.XPATH, '/html/body/div[5]/div[2]/form/table/tbody/tr[8]/td[2]/button').click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[3]/div[1]/div/div[4]/div/div/button/i')))

    def Registration(self):

        a = self.browser.find_element(By.XPATH, '/html/body/div[6]/header/div/div[1]/a').get_attribute('href')
        # print(f'{a=}')
        DNSID = a.replace('https://sed.rospotrebnadzor.ru/?DNSID=', '')

        self.browser.get(f'https://sed.rospotrebnadzor.ru/document.card.php?DNSID={DNSID}&category=6&r_category=9')
        print('Все готово')

        for o in self.rang:
            self.browser.get(f'https://sed.rospotrebnadzor.ru/document.card.php?DNSID={DNSID}&category=6&r_category=9')

            sadik_id = int(o[14])
            sadik = Database().get_sadik_info(sadik_id)

            id_o = o[0]
            properties = sadik[0][2]
            only_name = sadik[0][3]
            address = o[10]
            sut = 'введение карантина'
            groups = o[1]
            date_start = o[3]
            date_end = o[4]
            print(o[10])
            # time.sleep(500)

            inn = sadik[0][7]
            sed_name = sadik[0][9]

            self.doc_print_ORVI(id_o, properties, only_name, inn, address, groups, date_start, date_end)
            print('Документ напечатан')

            time.sleep(2)
            self.browser.find_element(By.XPATH, '//*[@id="remover_g_su_a_0"]').click()  # Удалить Бернюкову
            time.sleep(0.5)
            # time.sleep(100000)

            self.browser.find_element(By.XPATH, '//*[@id="inp_g_su_a_0"]').send_keys(self.nachalnik)
            time.sleep(1)
            self.browser.find_element(By.XPATH, '//*[@id="inp_g_su_a_0"]').send_keys(Keys.ENTER)

            # self.browser.find_element_by_xpath(
            #     '/html/body/div[5]/div[5]/div[2]/div[3]/div[1]/div/form/div[4]/div/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/div/span[2]/a[8]').click()
            time.sleep(0.5)
            self.browser.find_element(By.CSS_SELECTOR, '#inp_g_su_r_0').send_keys(sed_name)
            time.sleep(1)
            self.browser.find_element(By.CSS_SELECTOR, '#inp_g_su_r_0').send_keys(Keys.ENTER)

            for i in range(10):
                self.browser.find_element(By.TAG_NAME, 'html').send_keys(Keys.DOWN)
            self.browser.find_element(By.ID, 'document_kind').click()
            Select(self.browser.find_element(By.ID, 'document_kind')).select_by_visible_text('Постановление')

            for i in range(3):
                self.browser.find_element(By.ID, 'document_kind').send_keys(Keys.DOWN)
            self.browser.find_element(By.ID, 'document_kind').send_keys(Keys.ENTER)
            self.browser.find_element(By.ID, 'short_content').send_keys('Постановление на ', sut, ' ',
                                                                                      only_name)
            self.browser.find_element(By.XPATH,
                                      '/html/body/div[6]/div[3]/div[2]/div[3]/div[1]/div/form/div[4]/div/table/tbody/tr[28]/td[2]/div/div[1]/div/div/input').send_keys(
                f'{self.path}\напечатанные\{id_o}.doc')

            for i in range(4):
                self.browser.find_element(By.TAG_NAME, 'html').send_keys(Keys.DOWN)
            time.sleep(1)
            try:
                self.browser.find_element(By.ID, 'save_view').click()
            except:
                try:
                    self.browser.find_element(By.ID, 'save_view').click()
                except:
                    self.browser.find_element(By.ID, 'save_view').click()

            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '.s-agreesheet__add-buttons > input:nth-child(1)')))
            # self.browser.find_element_by_xpath
            try:
                self.browser.find_element(By.CSS_SELECTOR,
                                          '.s-agreesheet__add-buttons > input:nth-child(1)').click()  # Создать согласование
            except:
                try:
                    time.sleep(1)
                    self.browser.find_element(By.CSS_SELECTOR,
                                              '.s-agreesheet__add-buttons > input:nth-child(1)').click()  # Создать согласование
                except:
                    time.sleep(2)
                    self.browser.find_element(By.CSS_SELECTOR,
                                              '.s-agreesheet__add-buttons > input:nth-child(1)').click()  # Создать согласование
            time.sleep(1)
            self.browser.switch_to.window(self.browser.window_handles[1])
            try:
                self.browser.find_element(By.XPATH, '/html/body/div[5]/div/form/div[2]/button[1]').click()
            except:
                time.sleep(5)
                self.browser.find_element(By.CSS_SELECTOR, 'button.agreement-sheet__button:nth-child(1)').click()

            self.browser.switch_to.window(self.browser.window_handles[0])
            try:
                time.sleep(2)
                self.browser.find_element(By.XPATH,
                                          '/html/body/div[6]/div[3]/div[2]/div[3]/div[1]/div/div[6]/div[4]/div[2]/span/input').click()
            except:
                time.sleep(2)
                self.browser.find_element(By.XPATH,
                                          '/html/body/div[6]/div[3]/div[2]/div[3]/div[1]/div/div[6]/div[4]/div[2]/span/input').click()

            time.sleep(2)

            self.browser.switch_to.alert.accept()
            number = self.browser.find_element(By.XPATH, '//*[@id="maintable"]/tbody/tr[1]/td[2]/input').get_attribute('value')
            Database().assign_number(id_o, number)
            Database().level_up_status(id_o, 'ready')

        print('Регистрация в сэд закончена!')

        self.browser.quit()
        self.Kill_firefox()
        pass

    def doc_print_ORVI(self, id_o, properties, only_name, inn, address, groups, date_start, date_end):

        day = datetime.datetime.now().strftime('%d')
        month = datetime.datetime.now().strftime('%B')
        month_RP = Decline().wordskl(month, 'gent')
        year = datetime.datetime.now().strftime('%Y')

        date_start = datetime.datetime.strptime(str(date_start), "%Y-%m-%d").strftime('%d.%m.%Y')

        date_end = datetime.datetime.strptime(str(date_end), "%Y-%m-%d").strftime('%d.%m.%Y')

        tadate = f'{day} {month_RP} {year}'

        known_properties = {"ГБДОУ": {"property_ful": 'государственное бюджетное дошкольное образовательное учреждение',
                                      "group_kind": 'группе', "group_kind_P": 'группах', "person_kind": 'воспитанник',
                                      "person_kind_P": 'воспитанников'},
                            "ГБОУ": {"property_ful": 'государственное бюджетное общеобразовательное учреждение',
                                     "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик',
                                     "person_kind_P": 'учеников'}, "ГБПОУ НО": {
                "property_ful": 'государственное бюджетное профессиональное образовательное учреждение Нижегородской области',
                "group_kind": 'группе', "group_kind_P": 'группах', "person_kind": 'студент',
                "person_kind_P": 'студентов'},
                            "ГКОУ": {"property_ful": 'государственное казенное общеобразовательное учреждение',
                                     "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик',
                                     "person_kind_P": 'учеников'},
                            "МАДОУ": {"property_ful": 'муниципальное автономное дошкольное образовательное учреждение',
                                      "group_kind": 'группе', "group_kind_P": 'группах', "person_kind": 'воспитанник',
                                      "person_kind_P": 'воспитанников'},
                            "МАОУ": {"property_ful": 'муниципальное автономное общеобразовательное учреждение',
                                     "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик',
                                     "person_kind_P": 'учеников'},
                            "МБДОУ": {"property_ful": 'муниципальное бюджетное дошкольное образовательное учреждение',
                                      "group_kind": 'группе', "group_kind_P": 'группах', "person_kind": 'воспитанник',
                                      "person_kind_P": 'воспитанников'},
                            "МБОУ": {"property_ful": 'муниципальное бюджетное общеобразовательное учреждение',
                                     "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик',
                                     "person_kind_P": 'учеников'},
                            "ЧОУ РО": {"property_ful": 'частное общеобразовательное учреждение религиозной организации',
                                       "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик',
                                       "person_kind_P": 'учеников'}}
        print(groups)
        if re.search(",", groups):
            group_kind_PP = known_properties[properties]['group_kind_P']

        else:
            group_kind_PP = known_properties[properties]['group_kind']

        person_kind_RP = known_properties[properties]['person_kind_P']

        jinja_env = jinja2.Environment()

        doc = DocxTemplate(f"{os.path.dirname(__file__)}\шаблоны\{self.nachalnik} закрытие учреждения по ОРВИ.docx")
        doc.render({'tadate': tadate,
                    'properties': properties,
                    'only_name': only_name,
                    'inn': inn,
                    'address': address,
                    'groups': groups,
                    'group_kind_PP': group_kind_PP,
                    'person_kind_RP': person_kind_RP,
                    'date_start': date_start,
                    'date_end': date_end, }, jinja_env
                   )

        doc.save(f"{os.path.dirname(__file__)}\напечатанные\{id_o}.doc")

    def Kill_firefox(self):
        os.system('Taskkill /IM firefox.exe /F')


class Decline:
    def __init__(self):
        pass

    def wordskl(self, word, padezh):
        def sklonenie():
            d = OrderedDict()
            split = str.split(word)
            lenspl = len(split)

            if lenspl > 1:

                # print(split[1])
                for i in range(0, lenspl):
                    morph = pymorphy2.MorphAnalyzer()
                    parse_name = morph.parse(split[i])[0]

                    if parse_name.tag.case == 'nomn':
                        n = parse_name.inflect({padezh})[0]
                    else:
                        n = split[i]
                    d[n] = n
                N = list(d.values())

                data = N[0]
                for f in range(1, lenspl):
                    data = data + " " + N[f]
                return data
            else:
                morph = pymorphy2.MorphAnalyzer()
                parse_name = morph.parse(word)[0]
                n = parse_name.inflect({padezh})[0]
                return n

        if re.findall('"', word):
            skl = re.split('"', word)
            word = skl[0]
            return f'{sklonenie()} "{skl[1]}"'

        else:
            return sklonenie()
