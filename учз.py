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
        request = self.session.get(url, headers=headers)
        soup = BeautifulSoup(request.text, 'lxml')
        dnsid = soup.find('input', {'type': 'hidden'}).get('value')
        return dnsid

    def login_request(self):
        link = 'https://sed-dsp.rospotrebnadzor.ru/auth.php?group_id=3204'

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

    def findDocuments(self, docNumber: str) -> list:
        link = f'https://sed-dsp.rospotrebnadzor.ru/?DNSID={self.dnsid}&frmsearch=get&search=&search={self.encode_string(docNumber)}'
        responce = self.session.get(link, headers=self.header)
        hrefs = []
        soup_resp_a = BeautifulSoup(responce.text, 'lxml').find_all('a',
                                                                    {'class': 'td_inner document-list__number-outbox'})
        for a in soup_resp_a:
            hrefs.append('/'.join(['https://sed-dsp.rospotrebnadzor.ru', a.get('href')]))
        return hrefs

    def getFirstDocument(self, docNumber: str) -> BeautifulSoup:
        link = self.findDocuments(docNumber)[0]
        responce = self.session.get(link, headers=self.header)
        soup_resp = BeautifulSoup(responce.text, 'lxml')
        return soup_resp

    def get_registration_info(self, docNumber: str):

        def get_results(page):
            fio = None
            res = 'Нет листа согласования'
            comment = None
            sogls = page.find_all('div', {'class': 'csdr-list__row-wrapper csdr-list__row-wrapper-redirects'})
            for sogl in sogls:
                fio = sogl.find('span', {'class': 'csdr-list__user-name'}).text.strip()
                res = sogl.find('div', {'class': 'csdr-list__result-info'}).find('span').text.strip().split('\n')[0]
                comment = sogl.find('div', {'class': 'csdr-list__col csdr-list__notes-col'}).text.strip()
                print(f"{fio}, {res}, {comment}")
                if res == 'Не согласовано':
                    return {'status': f'{res} {fio}', 'number': None, 'comment': comment}

            return {'status': f'{res} {fio}', 'number': None, 'comment': comment}


        docPage = self.getFirstDocument(docNumber)

        try:
            registrationInfo = docPage.find('a', {'class': 's-agree-subcomment__link'}).text
            return {'status': 'Зарегистрировано', 'number': registrationInfo.strip(), 'comment': None}
        except:

            try:
                current_version_url = docPage.find('div', {'class': 's-agree-tabs__versions'}).find_all('a')[0].get('href')
            except:
                current_version_url = None


            #
            print(current_version_url)
            if not current_version_url:
                return get_results(docPage)

            current_version_response = self.session.get(f'https://sed-dsp.rospotrebnadzor.ru{current_version_url}', headers=self.header)
            current_version_page = BeautifulSoup(current_version_response.text, "lxml")
            return get_results(current_version_page)

    def get_info_for_task(self, docNumber):
        docPage = self.getFirstDocument(docNumber)
        number = docPage.find('span', {'class', 'main-document-field'}).text.strip()
        theme = docPage.find('td', {'class', 'b3 highlightable document_short_content s-table__shortcontent'}).text.strip()
        author =


    def encode_string(self, string):
        from urllib.parse import unquote, quote
        return quote(string, encoding='cp1251')





if __name__ == '__main__':
    print(SedRequests().get_registration_info('согл-218624192-1'))
    # print(SedRequests().encode_string('01/35171-2023-27'))

