#!/usr/bin/python
# coding: utf-8
import datetime
import os.path
import os
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
import requests
import fake_useragent
from bs4 import BeautifulSoup
from crypto import Crypto
from StringWorks import StringNormalizer
from urllib.parse import quote
from pprint import pprint
import re


from config import SED_Zaytsev_password, SED_Zaytsev_ID, SED_Ratnikov_password, SED_Ratnikov_ID, appeals_names




perols = {
    'Зайцев А.Д': Crypto().unpack_password(SED_Zaytsev_password),
    'Ратников Д.А': Crypto().unpack_password(SED_Zaytsev_password)
}

ids = {
    'Зайцев А.Д': SED_Zaytsev_ID,
    'Ратников Д.А': SED_Ratnikov_ID
}

class SED_operations:
    def __init__(self, dsp_contur: bool = True, headless: bool = False):
        self.dsp_contur = dsp_contur
        if self.dsp_contur is True:
            self.start_url = 'https://sed-dsp.rospotrebnadzor.ru/auth.php?uri=%2F'
        else:
            self.start_url = 'https://sed.rospotrebnadzor.ru/auth.php?uri=%2F'

        self.headless = headless

    def Autorize(self, user, dsp_contur: bool = True):
        self.options = webdriver.ChromeOptions()
        exists_cookie = 0
        if os.path.exists('cookies.json'):
            exists_cookie = 1
        self.akkaunt = user

        password = perols[user]
        binary_yandex_driver_file = 'C:\\Users\zaitsev_ad\PycharmProjects\WORK_sed\yandexdriver.exe' # path to YandexDriver
    
        browser_service = Service(executable_path=binary_yandex_driver_file)

        if self.headless:
            self.options.add_argument('--headless')
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

        if self.dsp_contur is False:
            self.browser.find_element(by=By.XPATH, value='//*[@id="primary-button"]').click()

            WebDriverWait(self.browser, 100000).until(EC.element_to_be_clickable((By.ID, 'details-button'))).click()
            time.sleep(2)
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, 'proceed-link'))).click()
        WebDriverWait(self.browser, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="organization_show"]')))
        self.browser.find_element(By.XPATH, '//*[@id="organization_show"]').click()
        org = self.browser.find_element(By.XPATH, '//*[@id="organizations"]')
        org.send_keys('Федеральная служба по надзору в сфере защиты прав потребителей')
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
        org.send_keys(Keys.DOWN)
        time.sleep(1)
        org.send_keys(Keys.ENTER)
    
        spec = self.browser.find_element(By.XPATH, '//*[@id="logins"]')
        spec.clear()
        spec.send_keys(self.akkaunt)
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
        spec.send_keys(Keys.DOWN)
        spec.send_keys(Keys.ENTER)
        passw = self.browser.find_element(By.ID, 'password_input')
        passw.send_keys(str(password))
        # time.sleep(101010)
        self.browser.find_element(By.XPATH, '//*[@id="login_form"]/table/tbody/tr[8]/td[2]/button').click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'body-content')))
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
        try:
            self.browser.find_element(By.ID, value='remover_g_su_a_0').click()
        except:
            pass
        self.browser.find_element(By.ID, value='inp_g_su_a_0').send_keys(signature)
        WebDriverWait(self.browser, 50).until(EC.visibility_of_element_located((By.ID, 'fio_0'))).click()

    def add_executor(self, executor):
        try:
            self.browser.find_element(By.ID, value='remover_SuPreparedBy').click()
        except:
            pass
        self.browser.find_element(By.ID, value='inp_SuPreparedBy').send_keys(executor)
        WebDriverWait(self.browser, 50).until(EC.visibility_of_element_located((By.ID, 'fio_0'))).click()

    def create_outgoing_document(self):
        self.browser.get(f"https://sed-dsp.rospotrebnadzor.ru/document.card.php?DNSID={self.dnsid}&category=6&r_category=1&new_version=1")

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

    def add_files(self, *files):
        for file in files:
            self.browser.find_element(By.XPATH,
                                      '/html/body/div[7]/div[3]/div[2]/div[1]/div[3]/div[2]/div/form/div[3]/div/table/tbody/tr[35]/td[2]/div/div[1]/div/div/div/input').send_keys(file)
            time.sleep(1)
    def add_document_kind(self, kind):
        self.browser.find_element(By.ID, 'document_kind').click()
        Select(self.browser.find_element(By.ID, 'document_kind')).select_by_visible_text(kind)

    def add_kind_medo(self, kind):
        medo_input = self.browser.find_element(By.XPATH, '//*[@id="maintable"]/tbody/tr[20]/td[2]/div/div/div/div[2]/input')
        medo_input.clear()
        medo_input.send_keys(kind)
        self.browser.find_element(By.XPATH, '//*[@id="maintable"]/tbody/tr[20]/td[2]/div/div/ul/li[2]').click()

    def add_short_describe(self, text):
        self.browser.find_element(By.ID, value='short_content').send_keys(text)

    def save_doc(self):
        self.browser.find_element(By.ID, value='save_view').click()

    def create_sogl_list(self):
        self.browser.execute_script("""createCsdrList();""")

    def add_participants(self, *participants):
        WebDriverWait(self.browser, 20).until(EC.number_of_windows_to_be(2))
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.find_element(By.XPATH, value='/html/body/div[2]/div[1]/div/form/div[2]/button[1]').click()
        # WebDriverWait(self.browser, 500).until(EC.visibility_of_element_located((By.XPATH,
        #                                                                          '/html/body/div[2]/div[1]/div/form/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div/div/input')))
        #
        # for n, participant in enumerate(participants):
        #     while True:
        #         try:
        #             rec_input = self.browser.find_element(By.XPATH, value=f"/html/body/div[2]/div[1]/div/form/div[1]/div[2]/div[2]/div[{n+1}]/div/div[1]/div/div/div/div[1]/div/div/input")
        #
        #             break
        #         except:
        #             self.browser.find_element(By.CSS_SELECTOR, value='body > div.pop-calendar-scrollable-parent.agreement-sheet.agreement-sheet--edit > div.agreement-sheet-table > div > form > div.agreement-sheet-list.agreement-sheet__list > div:nth-child(2) > div.agreement-sheet-block__users > div.agreement-sheet-block__controls.agreement-sheet-block__row > button').click()
        #             rec_input = self.browser.find_element(By.XPATH, value=f"/html/body/div[2]/div[1]/div/form/div[1]/div[2]/div[2]/div[{n+1}]/div/div[1]/div/div/div/div[1]/div/div/input")
        #
        #     rec_input.send_keys(participant)
        #     WebDriverWait(self.browser, 50).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/form/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div[2]/div/div[1]'))).click()

    def get_dnsid(self):
        with requests.Session() as session:
            user = fake_useragent.FakeUserAgent().random
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent': user
            }
            url = 'https://sed.rospotrebnadzor.ru/auth.php?uri=/'
            request = session.get(url, headers=headers)
            soup = BeautifulSoup(request.text, 'lxml')
            dnsid = soup.find('input', {'type': 'hidden'}).get('value')

            return dnsid

    def execute(self):
        script = """(async () => {var result = confirm('yes or no?');return result;})();"""
        print(self.browser.execute_async_script(script))
        input('отпусти мистикса')


class SedRequests:
    def __init__(self):
        self.session = requests.Session()
        self.user = fake_useragent.FakeUserAgent().random
        self.header = {
            'user-agent': self.user
        }
        self.dnsid = self.get_dnsid()
        self.login_request()

    def get_dnsid(self):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.0.2199 Yowser/2.5 Safari/537.36'
        }
        url = 'https://sed-dsp.rospotrebnadzor.ru/auth.php?uri=/'
        request = self.session.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(request.text, 'lxml')
        dnsid = soup.find('input', {'type': 'hidden'}).get('value')
        return dnsid

    def login_request(self):
        link = 'https://sed-dsp.rospotrebnadzor.ru/auth.php?group_id=7356'

        data = {
            "DNSID": self.dnsid,
            "group_id": "7356",
            "login": "%C7%E0%E9%F6%E5%E2+%C0.%C4.",
            "user_id": SED_Zaytsev_ID,
            "password": Crypto().unpack_password(SED_Zaytsev_password),
            "x": "1"
        }

        response = self.session.post(link, data=data, headers=self.header)
        # soup_resp = BeautifulSoup(response.text, 'lxml')
        return response.status_code

    def findDocuments(self, docNumber: str, exactly: bool = False) -> list:
        link = f'https://sed-dsp.rospotrebnadzor.ru/?DNSID={self.dnsid}&frmsearch=get&search=&search={str(self.encode_string(docNumber))}'
        # link = f'https://sed-dsp.rospotrebnadzor.ru/?DNSID={self.dnsid}&frmsearch=get&search=&search={docNumber}'
        # print(str(self.encode_string(docNumber)))
        responce = self.session.get(link, headers=self.header)
        # print(responce.text)
        hrefs = []
        soup_resp_a = BeautifulSoup(responce.text, 'lxml').find_all('a', {'class': 'td_inner'})

        for a in soup_resp_a:
            if exactly:
                if a.find('span', {'class': 'markfound'}):
                    hrefs.append('/'.join(['https://sed-dsp.rospotrebnadzor.ru', a.get('href')]))
            else:
                hrefs.append('/'.join(['https://sed-dsp.rospotrebnadzor.ru', a.get('href')]))
        return hrefs

    def getFirstDocument(self, docNumber: str, responce_only: bool = False):
        try:
            link = self.findDocuments(docNumber)[0]
        except:
            raise Exception(f'docNumber: {docNumber}')
        responce = self.session.get(link, headers=self.header)
        # print(exec("document_og"))
        if responce_only:
            return responce
        soup_resp = BeautifulSoup(responce.text, 'lxml')
        return soup_resp

    def get_registration_info(self, docNumber: str):

        def get_results(page):
            fio = None
            res = 'Нет листа согласования'
            comment = None

            res_consistions = ['Не согласовано', 'На согласовании']

            try:
                number = page.find('span', {'class': 'main-document-field'}).text.strip()
            except:
                number = None
            sogls = page.find_all('div', {'class': 'csdr-list__row-wrapper csdr-list__row-wrapper-redirects'})
            for consist in res_consistions:
                for sogl in sogls:
                    fio = sogl.find('span', {'class': 'csdr-list__user-name'}).text.strip()
                    res = sogl.find('div', {'class': 'csdr-list__result-info'}).find('span').text.strip().split('\n')[0]
                    comment = sogl.find('div', {'class': 'csdr-list__col csdr-list__notes-col'}).text.strip()
                    print(f"{fio}, {res}, {comment}")
                    if res == consist:
                        return {'status': f'{res} {fio}', 'number': number, 'comment': f"{comment}"}

            return {'status': f'{res} {fio}', 'number': number, 'comment': f"{comment}"}


        docPage = self.getFirstDocument(docNumber)

        try:
            # print(docPage)
            registrationInfo = docPage.find('span', {'class': 'document-subtitle__num'}).text

            return {'status': 'Зарегистрировано', 'number': registrationInfo.strip(), 'comment': None}
        except:

            try:
                versions_a_hrefs = docPage.find('div', {'class': 's-agree-tabs__versions'})
                if docNumber[-2:] == f"-{len(versions_a_hrefs.find_all('button'))}":
                    return get_results(docPage)
                current_version_url = versions_a_hrefs.find_all('a')[0].get('href')
            except:
                current_version_url = None
            if not current_version_url:
                return get_results(docPage)

            current_version_response = self.session.get(f'https://sed-dsp.rospotrebnadzor.ru{current_version_url}', headers=self.header)
            current_version_page = BeautifulSoup(current_version_response.text, "lxml")
            return get_results(current_version_page)

    def findIdbyNumber(self, number):

        return str(self.findDocuments(number)[0]).split('id=')[1].split('&')[0]


    def docAgreedSignators(self, docNumber):
        agreedSignators = []
        def findSignators(page):
            res_consistions = ['Согласовано', 'Подписано']
            sogls = page.find_all('div', {'class': 'csdr-list__row-wrapper csdr-list__row-wrapper-redirects'})
            for sogl in sogls:
                fio = sogl.find('span', {'class': 'csdr-list__user-name'}).text.strip()
                res = sogl.find('div', {'class': 'csdr-list__result-info'}).find('span').text.strip().split('\n')[0]
                if res in res_consistions:
                    agreedSignators.append(fio)


        docPage = self.getFirstDocument(docNumber)
        versions_a_hrefs = docPage.find('div', {'class': 's-agree-tabs__versions'})

        if versions_a_hrefs:
            version_hrefs = versions_a_hrefs.find_all('a')
            for version in version_hrefs:
                current_version_response = self.session.get(f'https://sed-dsp.rospotrebnadzor.ru{version.get("href")}',
                                                            headers=self.header)
                current_version_page = BeautifulSoup(current_version_response.text, "lxml")
                findSignators(current_version_page)

        findSignators(docPage)
        return set(agreedSignators)

    def get_info_for_task(self, docNumber):
        docPage = self.getFirstDocument(docNumber)
        number = docPage.find('span', {'class', 'main-document-field'}).text.strip()
        theme = docPage.find('td', {'class', 'b3 highlightable document_short_content s-table__shortcontent'}).text.strip()

    def encode_string(self, string):
        from urllib.parse import unquote, quote
        return quote(string, encoding='cp1251')

    def download_sed_doc(self, docNumber):
        link_part = self.findDocuments(docNumber)[0].split('?')[1]
        link = f'https://sed-dsp.rospotrebnadzor.ru/web/?url=print/onlyDocument&{link_part}&with_note=1'

        resp = self.session.get(link, headers=self.header)
        with open(f'{os.path.dirname(__file__)}/downloads/{StringNormalizer().removeSlashes(docNumber)}.pdf', 'wb') as file:
            file.write(resp.content)

    def get_not_read_list(self, limit: int = 0):
        page = 0
        hasNextPage = True
        docsList = []
        while hasNextPage:
            print(page)
            link0 = f'https://sed-dsp.rospotrebnadzor.ru/document.php?DNSID={self.dnsid}&forceuser=1&in_work=1&control_execution_block=review&control_execution_link=all&isJson=1&whole_period=1&ajax=1&page={page}&DNSID={self.dnsid}'
            link = f'https://sed-dsp.rospotrebnadzor.ru/document.php?DNSID={self.dnsid}&forceuser=1&in_work=1&control_execution_block=review&control_execution_link=all&isJson=0&whole_period=1&ajax=1&page={page}&DNSID={self.dnsid}'
            resp = self.session.get(link, headers=self.header)
            soup = BeautifulSoup(resp.text, 'lxml')
            allDocs = [{
                'number_inner': self.normalizeString(doc.find('b', {'class': 'num-hyphens'}).text),
                'recipient_name': self.normalizeString(doc.find('span', {'class': 's-doc__recipient-name'}).text),
                'author_name': self.normalizeString(doc.find('span', {'class': 's-doc__author'}).text),
                'theme': self.normalizeString(doc.find('div', {'class': 's-table__clamping s-table__shortcontent'}).text),
            } for doc in soup.find_all('tr', {'class': 'document-list__tr r0 s-doc__not-read document-list__tr--has-pages'})]
            docsList.extend(allDocs)
            page += 1
            if limit:
                if len(docsList) == limit:
                    break
            hasNextPage = self.session.get(link0, headers=self.header).json()['data']['pagesOptions']['hasNextPage']
        return docsList

    def normalizeString(self, string: str):
        string = string.replace('\n', ' ').strip()
        while '  ' in string:
            string = string.replace('  ', ' ')
        return string

    def getUsers(self, text):
        url = f'https://sed-dsp.rospotrebnadzor.ru/getusers.php?DNSID={self.dnsid}&&fio={self.encode_string(text)}&offset=0&responseType=json'
        responce = self.session.get(url, headers=self.header)
        # print(responce.json())
        return responce.json()

    def get_complain_info(self, number):
        doc = self.getFirstDocument(number, responce_only=False)
        main = doc.find_all('span', {'class': 'main-document-field'})
        infos = doc.find_all('tr', {'class': 'og_authors_0 tr_b3'})
        fio = infos[0].find_next('td', {'class': "b3 highlightable break-word"}).text
        email = infos[5].find_all('td', {'class': 'b3'})[1].text
        doc_reg_date = datetime.datetime.strptime(main[1].text.strip(), '%d.%m.%Y').strftime('%Y-%m-%d')
        return {'number': number, 'fio': fio, 'email': email, 'date': doc_reg_date}

    def createNewDoc(self, theme, signator: str, implementer: str, addressats: list, pageCount=1, annex=0, reply=None, petition=None):
        # cookies = {
        #     '_ga': 'GA1.2.2114253625.1701265012',
        #     'last_login_u_id': '957306',
        #     'auth_token': 'fc2854cad0b48c578400e9698bf6e352ae567d41',
        #     'menu_item_6': '1',
        #     'SED.menuItems': '["s-menu-user"]',
        # }
        addressats = [self.getUsers(addressat)['list'][0]['id'] for addressat in addressats]
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Encode': 'windows-1251',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarytBNEPK9hEbuFirYw',
            # 'Cookie': '_ga=GA1.2.2114253625.1701265012; last_login_u_id=957306; auth_token=fc2854cad0b48c578400e9698bf6e352ae567d41; menu_item_6=1; SED.menuItems=["s-menu-user"]',
            'Origin': 'https://sed-dsp.rospotrebnadzor.ru',
            'Referer': f'https://sed-dsp.rospotrebnadzor.ru/document.card.php?DNSID={self.dnsid}&category=6&r_category=1&new_version=1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.4.999 (corp) Yowser/2.5 Safari/537.36',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        params = [
            ('DNSID', self.dnsid),
            ('category', '6'),
            ('r_category', '3' if petition else '1'),
            ('new_version', '1'),
            ('DNSID', self.dnsid),
        ]
        if reply:
            params.append(('reply', reply))

        data = f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="ignore_nc_orgs"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="fill_time"\r\n\r\n31850\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="active_fill_time"\r\n\r\n27706\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="comment"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="nomenclature_unit_id"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="out_date[0]"\r\n\r\n{datetime.datetime.now().strftime("%d.%M.%Y")}\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="to[a][0]"\r\n\r\n{self.getUsers(signator)["list"][0]["id"]}\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="inv_to[a][0]"\r\n\r\n0\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="acting_author[0]"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="acting_post_hier[0]"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="out_phone[0]"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="prepared_by"\r\n\r\n{self.getUsers(implementer)["list"][0]["id"]}\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="inv_prepared_by"\r\n\r\n0\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="inv_to[r][0]"\r\n\r\n0\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="sheet_count"\r\n\r\n{pageCount}+{annex}+1\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="document_kind"\r\n\r\n{128 if petition else 4}\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="delivery_type"\r\n\r\n{61 if petition else 12}\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="short_content"\r\n\r\n{f"{theme}".encode("cp1251").decode("cp1252")}\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="memo"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="info"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="info_date"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="info_author"\r\n\r\n0\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="inv_info_author"\r\n\r\n0\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="mu_files_in[dir]"\r\n\r\nIzvNJ82go9\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="multikey"\r\n\r\n1-1701355784\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="override_pages"\r\n\r\n0\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="page_action_comment"\r\n\r\n\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="save_view"\r\n\r\n1\r\n' \
               f'------WebKitFormBoundarytBNEPK9hEbuFirYw\r\nContent-Disposition: form-data; name="recipientIds"\r\n\r\n'+'{'+', '.join([f'"recipientIds_{n}":"{addressat}"' for n, addressat in enumerate(addressats)])+'}\r\n------WebKitFormBoundarytBNEPK9hEbuFirYw--\r\n'
        # files = {
        #     'ignore_nc_orgs': "",
        #     'comment': "",
        #     'nomenclature_unit_id': "",
        #     'out_date[0]': "",
        #     'to[a][0]': "",
        #     'inv_to[a][0]': "73608",
        #     'acting_author[0]': "0",
        #     'acting_post_hier[0]': "",
        #     'out_phone[0]': "",
        #     'prepared_by': "957306",
        #     'inv_prepared_by': "0",
        #     'sourceId[r][0]': "0",
        #     'inv_to[r][0]': "0",
        #     'sourceId[r][1]': "40283890",
        #     'inv_to[r][1]': "0",
        #     'sheet_count': "1+0+1",
        #     'document_kind': "4",
        #     'delivery_type': "12",
        #     'short_content': "",
        #     'memo': "",
        #     'info': "",
        #     'info_date': "",
        #     'info_author': "",
        #     'inv_info_author': "",
        #     'mu_files_in[dir]': "Xh6WhN7gLI",
        #     'multikey': "1-26583716",
        #     'override_pages': "0",
        #     'page_action_comment': "",
        #     'save_view': "1",
        #     'recipientIds': '{"recipientIds_0":"3","recipientIds_1":"411162"}',
        # }
        response = requests.post(
            'https://sed-dsp.rospotrebnadzor.ru/document.card.php',
            params=params,
            allow_redirects=False,
            # cookies=cookies,
            cookies=self.session.cookies.get_dict(),
            headers=headers,
            data=data,
            # json=files
        )
        print(response.headers)
        location = response.headers['Location']
        return self.getDocumentByHref(location).find('span', {'class': 'main-document-field'}).text, location.split('id=')[1]

    def getDocumentByHref(self, href):
        link = '/'.join(['https://sed-dsp.rospotrebnadzor.ru', href])
        responce = self.session.get(link, headers=self.header)
        soup_resp = BeautifulSoup(responce.text, 'lxml')
        return soup_resp

def get_agreed_signators():
    aggreed = SedRequests().docAgreedSignators('согл-220661483-1')
    result = None
    if aggreed:
        signators = ', '.join(aggreed)
        result = f'В предыдущих версиях согласовано: {signators}'
    print(result)




if __name__ == '__main__':


    get_agreed_signators()

    # sed = SedRequests()
    # limit = 3
    # pprint(sed.get_not_read_list(limit=limit))



    # pprint(sed.get_complain_info('09-5496-2024-05'))

    # print(sed.createNewDoc(
    #     theme='О рассмотрении обращения',
    #     signator='Попова А.Ю',
    #     implementer="Зайцев А.Д",
    #     addressats=['Обращения граждан'],
    #     reply="09-33018-2023-06"
    # ))
    #

    # print(sed.findIdbyNumber('09-44246-2023-05'))
    # print(sed.getUsers('Обращение граждан')['list'][0]['id'])
    # print(sed.encode_string('О рассмотрении обращения'))
    # print(sed.get_not_read_list())

    # acceptors = sed.docAgreedSignators("согл-219150489-3")
    # print(f"В предыдущих версиях согласовали: {', '.join(acceptors)}")


    # print(sed.get_not_read_list())

    # print(SedRequests().encode_string('01/35171-2023-27'))

