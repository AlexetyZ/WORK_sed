import pymysql
from REG_to_APPLY import Registration_sadik
from REGIT import Regit
from Otpravka_PRO import Otpravka
import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import os
import re
from config import SED_Zaytsev_password, SED_Semenova_password, SED_Zaytsev_ID, SED_Semenova_ID, SED_Udalova_password, SED_Udalova_ID
from sql import Database

class ChekNew:
    def __init__(self):
        self.conn = pymysql.connect(
            user='root',
            password='ntygazRPNautoz',
            host='127.0.0.1',
            port=3307,
            database='django'
        )

        # self.user = fake_useragent.UserAgent().random
        # self.header = {
        #     'user-agent': self.user
        # }
        #
        # # for selen
        # self.DNSID = self.get_dnsid()
        # self.akkaunt = 'Удалова Т.А'
        # self.password = SED_Udalova_password
        # self.SED_ID = SED_Udalova_ID

        self.get_connect()

    def get_connect(self):

        rang = self.get_info()

        # print(rang)
        # self.listrang(rang)
        self.raspred(rang)
        # self.get_sadik_info(31)

    def get_values(self):
        pass

    def listrang(self, rang):

        for o in rang:
        #     for i in o:
        #         print(i)

            id_o = o[0]
            print(f'id_o -0--- {id_o}')

            groups = o[1]
            print(f'groups -1--- {groups}')

            group_size = o[2]
            print(f'group_size -2--- {group_size}')

            date_start = o[3]
            print(f'date_start -3--- {date_start}')

            date_end = o[4]
            print(f'date_end -4--- {date_end}')

            reason = o[5]
            print(f'reason -5--- {reason}')

            fio_covid = o[6]
            print(f'fio_covid -6--- {fio_covid}')

            fio_post = o[7]
            print(f'fio_post -7--- {fio_post}')

            last_day = o[8]
            print(f'last_day -8--- {last_day}')

            identify_day = o[9]
            print(f'identify_day -9--- {identify_day}')

            address_spe = o[10]
            print(f'address_spe -10--- {address_spe}')



            status = o[11]
            print(f'status -11--- {status}')

            doc_number = o[12]
            print(f'doc_number -12--- {doc_number}')

            ord_date = o[13]
            print(f'ord_date -13--- {ord_date}')

            sadik_id = o[14]
            print(f'sadik_id -14--- {sadik_id}')

            print('')
            print('')
            print('')
            sadik = self.get_sadik_info(sadik_id)

            district = sadik[0][1]
            print(f'district -0-1-- {district}')

            properties = sadik[0][2]
            print(f'properties -0-2-- {properties}')

            only_name = sadik[0][3]
            print(f'only_name -0-3-- {only_name}')

            address = sadik[0][4]
            print(f'address -0-4-- {address}')

            fio_director = sadik[0][5]
            print(f'fio_director -0-5-- {fio_director}')

            e_mail = sadik[0][6]
            print(f'e_mail -0-6-- {e_mail}')

            inn = sadik[0][7]
            print(f'inn -0-7-- {inn}')

            sed_name = sadik[0][9]
            print(f'sed_name -0-9-- {sed_name}')



    def raspred(self, rang):
        ready = []
        applied = []
        registred = []
        lusting = {'ready': {'conteiner': ready, 'function': 'будем согласовывать'},
                   'applied': {'conteiner': applied, 'function': 'будем регистрировать'},
                   'registred': {'conteiner': registred, 'function': 'будем отправлять'}}
        for o in rang:
            status = o[11]

            for k, v in lusting.items():
                if status == k:
                    # print(f'{v["function"]}  {o[3]}')
                    v["conteiner"].append(o)
        if len(ready) > 0:
            print
            print('запуск отправки на согласование')
            Registration_sadik(ready)
        else:
            print('отправлять на согласование нечего')



        """Здесь должна быть функция проверки согласования документа руководителем"""

        '''Оставлено до лучших времен, ниже код проверки согласования'''

        # if len(applied) > 0:
        #     with requests.Session() as self.session:
        #         self.login_request()
        #         applied_list = list(applied)   # сделано для того, чтобы в случае удаления значения из списка applied не прерывался цикл
        #         for a in applied_list:
        #
        #             nsogl = a[12]   # значение номера согласования
        #             n = re.split('огл-', nsogl)[1]
        #             link = f'https://sed.rospotrebnadzor.ru/?DNSID={self.DNSID}&frmsearch=get&search=&search=%F1%EE%E3%EB-{n}'
        #             try_find_sogl = self.session.get(link)
        #             soup_try_find_sogl = BeautifulSoup(try_find_sogl.text, 'lxml')
        #
        #             link_to_doc = f"https://sed.rospotrebnadzor.ru/{soup_try_find_sogl.find('a', {'class': 'td_inner'}).get('href')}"
        #             doc = self.session.get(link_to_doc)
        #             soup_doc = BeautifulSoup(doc.text, 'lxml')
        #             text_page = str(soup_doc.text)
        #
        #             if re.search('52-13-27-', str(soup_try_find_sogl)):
        #                 Database().level_up_status(a[0], 'registred')
        #
        #
        #             if bool(re.search('На подписании', str(text_page))) == True:
        #                 print('еще не согласовано')
        #                 applied.remove(a)
        #             if bool(re.search('Не согласовано', str(text_page))) == True:
        #                 print('')
        #                 print(f"ВНИМАНИЕ!!!!! НЕ Согласовано! комментарий: {soup_doc.find('div', {'class': 'csdr-list__col csdr-list__notes-col'}).text}")
        #                 print('')
        #                 applied.remove(a)






                    #функция запроса согласования, если не согласовано - удаляем из списка applied
        # if len(applied) > 0:
        #     print('запуск регистраций документов')
        #     Regit(applied)
        # else:
        #     print('регистрировать нечего')



        if len(registred) > 0:
            print('запуск на отправку')
            Otpravka(registred)
        else:
            print('отправлять по почте нечего')

    def get_sadik_info(self, sadik_id):
        with self.conn.cursor() as cursor:
            cursor.execute(f"Select * FROM sadidi_sadik where id='{sadik_id}'")
            result = cursor.fetchall()
            return result

    def get_info(self):
        # self.cursor.execute("Select * FROM sadidi_ordinary where status='ready'")
        with self.conn.cursor() as cursor:
            cursor.execute("Select * FROM sadidi_ordinary")
            result = cursor.fetchall()
            return result



    def login_request(self):
        link = 'https://sed.rospotrebnadzor.ru/auth.php?group_id=3204'
        apply_link = 'https://sed.rospotrebnadzor.ru/document.php?all=1&c_user_status=0&dcv_status=1&category=6&DNSID=wXwaCw5PYykCpa7Zla8AjhQ'
        revision_link = 'https://sed.rospotrebnadzor.ru/document.php?all=1&c_user_status=1&category=6&DNSID=w9gfvomxjNRwo_HbkP_MOCg'
        registred_link = 'https://sed.rospotrebnadzor.ru/document.php?all=1&c_user_status=2&c_user_status_type=1&category=6&DNSID=w9gfvomxjNRwo_HbkP_MOCg'

        data = {
            "DNSID": self.DNSID,
            "group_id": "32043",
            "login": "%D3%E4%E0%EB%EE%E2%E0+%D2.%C0.",
            "user_id": self.SED_ID,
            "password": self.password,
            "x": "1"
        }

        response = self.session.post(link, data=data, headers=self.header)
        soup_resp = BeautifulSoup(response.text, 'lxml')
        print(soup_resp)

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

if __name__ == "__main__":
    ChekNew()
