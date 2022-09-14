import locale
import re

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from config import SED_Zhikova_password
from sql import Database


class Regit:
    def __init__(self, rang):
        self.akkaunt = 'Жукова И.В'
        self.password = SED_Zhikova_password
        self.rang = rang

        self.options = Options()
        self.options.set_preference("dom.webnotifications.enabled", False)

        # self.options.add_argument("--headless")  # если это включено, то будет в режиме фантома
        self.browser = webdriver.Firefox(options=self.options)
        self.browser.fullscreen_window()

        self.Controller()
        self.Start_to_reg()
        self.Kill_firefox()

    def Kill_firefox(self):
        os.system('Taskkill /IM firefox.exe /F')

    def Controller(self):

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
            self.Kill_firefox()
        if autorization == 1:
            pass

    def Autorization(self):
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

    def Start_to_reg(self):
        print('начал регистрировать')

        a = self.browser.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[1]/div/div[2]/div/div/ul[1]/li/a').get_attribute('href')
        DNSID = a.replace('https://sed.rospotrebnadzor.ru/?DNSID=', '')

        self.browser.get(f'https://sed.rospotrebnadzor.ru/document.php?unnumbered=1&signed=1&category=9&DNSID={DNSID}')

        for i in self.rang:
            id_o = i[0]
            nsogl = i[12]
            n = re.split('огл-', nsogl)[1]
            self.browser.get(
                f'https://sed.rospotrebnadzor.ru/?DNSID={DNSID}&frmsearch=get&search=&search=%F1%EE%E3%EB-{n}')
            # time.sleep(300)
            time.sleep(1)
            number = self.browser.find_element(By.XPATH,
                                               '/html/body/div[6]/div[3]/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[1]/td[5]/a/div').text

            if re.search("52-13-27", number):
                print(f'{nsogl} уже зарегистрировано, меняем статус')
                Database().level_up_status(id_o, 'applied')
            # elif:
            #     print(f'{nsogl} еше не подписано!')
            #     # Database().level_up_status(id_o, 'applied')
            #     continue
            if number == "Нет":

                href = self.browser.find_element(By.XPATH,
                                                 '/html/body/div[6]/div[3]/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[1]/td[5]/a').get_attribute(
                    'href')
                self.browser.get(href)
                try:

                    self.browser.find_element(By.XPATH,
                                              '/html/body/div[6]/div[3]/div[2]/div[3]/div[1]/div/div[6]/div[1]/div[1]/div[1]/a[1]/div/div/i').click()
                except:
                    continue

                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[3]/div[2]/div[3]/div[1]/div/form/div[8]/div/table/tbody/tr[2]/td[2]/div/a'))) # элемент удалить № 27
                self.browser.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div[3]/div[1]/div/form/div[8]/div/table/tbody/tr[2]/td[2]/div/a').click()
                time.sleep(0.5)
                n_dela_input = self.browser.find_element(By.XPATH,
                                          '/html/body/div[6]/div[3]/div[2]/div[3]/div[1]/div/form/div[8]/div/table/tbody/tr[2]/td[2]/div/div/div/div[2]/input')
                n_dela_input.click()
                # n_dela_input.send_keys('№ 27 Постановление главного санитарного врача на территории')

                self.browser.find_element(By.XPATH,
                                          '/html/body/div[6]/div[3]/div[2]/div[3]/div[1]/div/form/div[8]/div/table/tbody/tr[2]/td[2]/div/div/ul/li[14]').click()
                self.browser.find_element(By.XPATH, '//*[@id="save_view"]').click()

                time.sleep(1)

                for down in range(20):
                    self.browser.find_element(By.TAG_NAME, 'html').send_keys(Keys.DOWN)
                time.sleep(1)

                self.Action()

                # try:
                #     self.Action()
                # except:
                #     print('не получилось 1 раз')
                #     self.browser.refresh()
                #     time.sleep(1)
                #     try:
                #         self.Action()
                #     except Exception as ex:
                #         print('не получилось 2 раз')
                #         print(ex)

                pages = int(self.browser.find_element(By.CSS_SELECTOR,
                                                      'html.modern body div.body-content div.s-page div.s-page__page.s-page__page_custom div.s-page__body div.s-viewer div.s-viewer__inner div.card_separator div#pages_list h3.s-viewer__title div.s-viewer__all-pages a.show_all_pages strong').text)
                print(pages)
                self.Stamp_1_pages(pages)
                # try:
                #
                #     self.Stamp_1_pages(pages)
                # except Exception as ex:
                #     # self.Stamp_1_pages(pages)
                #     print(f'Не удалось определить количество страниц {ex}')
                #     pass

                # print(self.browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[2]/div[3]/div[4]/div/div[1]/div[2]/h3[1]/div[2]/a/strong').text)
                # inp = input(f'{i-lrow_postan} далее?')
                self.browser.find_element(By.XPATH, f'div.vdr:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > button:nth-child(1) > i:nth-child(1)').click()
                time.sleep(1)
                self.browser.switch_to.alert.accept()
                Database().level_up_status(id_o, 'applied')
        self.Kill_firefox()

    def refresh_stamp(self, pages):
        time.sleep(1)
        self.browser.find_element(By.XPATH, f'//*[@id="delStamp_{int(pages - 1)}"]').click()
        time.sleep(1)
        self.browser.switch_to.alert.accept()
        self.Stamp_1_pages(pages)

    def Stamp_1_pages(self, pages):
        if int(pages) == 1:
            print(int(pages))
            time.sleep(2)
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[6]/div[3]/div[2]/div[3]/div[4]/div/div[1]/div[2]/div/div/div[1]/div/div/div/div[1]/div[4]/div/div[1]/button')))
            time.sleep(1)
            self.browser.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div[3]/div[4]/div/div[1]/div[2]/div/div/div[1]/div/div/div/div[1]/div[4]/div/div[1]/button').click()

            '#digital-signature-509320-placeholder-0 > div:nth-child(1) > div:nth-child(1)'
            self.browser.find_element(By.ID, f'digital-signature-509320-stamp-button-{int(pages - 1)}').click()
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'#digital-signature-509320-placeholder-0 > div:nth-child(1) > div:nth-child(1)')))
            stamp = self.browser.find_element(By.CSS_SELECTOR, f'#digital-signature-509320-placeholder-0 > div:nth-child(1) > div:nth-child(1)')
            action_chains = ActionChains(self.browser)
            time.sleep(1)
            summary = self.browser.find_element(By.XPATH,
                                                '/html/body/div[6]/div[3]/div[2]/div[3]/div[1]/div/div[8]/div/table/tbody/tr[14]/td[2]').text
            if summary.startswith('Постановление на введение'):
                print(summary)
                action_chains.drag_and_drop_by_offset(stamp, 390, 385)
            else:
                print('отмена')
                action_chains.drag_and_drop_by_offset(stamp, 350, 385)
                action_chains.drag_and_drop_by_offset(stamp, 350, 385)

            action_chains.perform()

            time.sleep(1)

            for down in range(28 * int(pages)):
                self.browser.find_element(By.TAG_NAME, 'html').send_keys(Keys.DOWN)

            action_chains = ActionChains(self.browser)
            time.sleep(1)
            if summary.startswith('Постановление на введение'):
                # print(summary)
                action_chains.drag_and_drop_by_offset(stamp, 0, 490)
            else:

                action_chains.drag_and_drop_by_offset(stamp, 0, 470)
            action_chains.perform()

        if int(pages) != 1:
            time.sleep(2)
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="addStamp_0"]')))
            time.sleep(1)
            self.browser.find_element(By.XPATH,
                                      '/html/body/div[5]/div[5]/div[2]/div[3]/div[4]/div/div[1]/div[2]/h3[1]/div/a').click()
            time.sleep(1)
            self.browser.find_element(By.XPATH, f'//*[@id="addStamp_{int(pages - 1)}"]').click()
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'#stamp_placeholder > img:nth-child(1)')))
            time.sleep(1)
            stamp = self.browser.find_element(By.CSS_SELECTOR, f'#stamp_placeholder > img:nth-child(1)')
            action_chains = ActionChains(self.browser)
            time.sleep(1)
            action_chains.drag_and_drop_by_offset(stamp, 307, 349)
            for down in range(22 * int(pages)):
                self.browser.find_element(By.TAG_NAME, 'html').send_keys(Keys.DOWN)
            time.sleep(1)

            action_chains.perform()

            # self.refresh_stamp(pages)

    def Action(self):
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div[3]/div[2]/div[3]/div[4]/div/div[1]/div[2]/div/div/div[1]/div/div/div/div[1]/div[4]/div/div[1]/button')))
        self.browser.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div[3]/div[4]/div/div[1]/div[2]/div/div/div[1]/div/div/div/div[1]/div[4]/div/div[1]/button').click()
        time.sleep(1)
        self.browser.find_element(By.XPATH, '//*[@id="number-and-date-32043-stamp-button-0"]').click()
        number = self.browser.find_element(By.CSS_SELECTOR, 'div.stamp-placeholder:nth-child(1)')
        action_chains = ActionChains(self.browser)
        time.sleep(1)
        # action_chains.click_and_hold(number)
        action_chains.drag_and_drop_by_offset(number, 205, 330)
        action_chains.perform()
        self.browser.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div[3]/div[4]/div/div[1]/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[1]/div/div[2]/button[1]').click()
        time.sleep(20)


    def Kill_firefox(self):
        os.system('Taskkill /IM firefox.exe /F')

# if __name__=='__main__':
#     Regit()
