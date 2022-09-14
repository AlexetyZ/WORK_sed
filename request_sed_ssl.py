import requests
import fake_useragent
from bs4 import BeautifulSoup
from config import SED_Zaytsev_password, SED_Zaytsev_ID
from requests_html import HTMLSession

session = requests.Session()
link = 'https://sed.rospotrebnadzor.ru/auth.php?group_id=3204'
user = fake_useragent.UserAgent().random
# session.cert = "C:\\Users\\user\\PycharmProjects\\ERKNM_plan_bot.pem"
header = {
            'user-agent': user
        }
session.cert = ["E:\\688110273549054209909165602398494243592907465057.cer", "E:\\xwfsbygq.000\primary.key"]
print(user)
data = {
    'DNSID': 'wqx7cahFJjk6x2QyA8VYkQg',
    'group_id': '32043',
    'user_id': SED_Zaytsev_ID,
    'password': SED_Zaytsev_password,
    'x': '1',
}

response = session.post(link, data=data, headers=header)
soup_response = BeautifulSoup(response.text, 'lxml')
print(soup_response)