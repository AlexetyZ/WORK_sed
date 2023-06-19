import fake_useragent
from учз import SED_operations
import os
from pathlib import Path
import glob
import requests
from bs4 import BeautifulSoup

def create_doc_to_MZ():
    from_Zaytsev = SED_operations().Autorize('Зайцев А.Д')
    from_Zaytsev.create_outgoing_document()
    from_Zaytsev.add_signature("Орлов М.С")
    from_Zaytsev.add_inner_recipient("Минздрав России")
    from_Zaytsev.add_document_kind('Служебное письмо')
    from_Zaytsev.add_kind_medo('Служебное письмо Аппарата Правительства Российской Федерации, полномочных представителей Правительства Российской Федерации, государственного органа, органа исполнительной власти субъекта Российской Федерации, организации')
    from_Zaytsev.add_short_describe('Об обязательствах и ответственности при взаимодействии в рамках приказа Минздрава России 90н')
    from_Zaytsev.add_files(
        "S:\Зайцев_АД\письмо в минздрав\об элмк по всем\В минздрав по ЭЛМК.docx"
    )
    from_Zaytsev.save_doc()


    # try:

    # from_Zaytsev.add_participants("Игонина Е.П", 'Костина М.А')
    # except Exception as ex:
    #     print(ex)

    input("я все, отпусти Мистера Мистикса")
    # from_Zhukova = SED_operations().Autorize('Жукова И.В')


def experiment_doc():
    from_Zaytsev = SED_operations().Autorize('Зайцев А.Д')
    from_Zaytsev.create_outgoing_document()
    from_Zaytsev.add_signature("Орлов М.С")
    from_Zaytsev.add_inner_recipient("Минздрав России")
    from_Zaytsev.add_document_kind('Служебное письмо')
    from_Zaytsev.add_kind_medo('Служебное письмо Аппарата Правительства Российской Федерации, полномочных представителей Правительства Российской Федерации, государственного органа, органа исполнительной власти субъекта Российской Федерации, организации')
    from_Zaytsev.add_short_describe('Об обязательствах и ответственности при взаимодействии в рамках приказа Минздрава России 90н')
    from_Zaytsev.add_files(
        *get_files_from_dir()
    )
    from_Zaytsev.save_doc()


    # try:

    # from_Zaytsev.add_participants("Игонина Е.П", 'Костина М.А')
    # except Exception as ex:
    #     print(ex)

    input("я все, отпусти Мистера Мистикса")
    # from_Zhukova = SED_operations().Autorize('Жукова И.В')

def get_files_from_dir():
    dir_path = "C:\\Users\zaitsev_ad\Desktop\some dir"
    files_list = [os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path)]
    soprovod = glob.glob(os.path.join(dir_path, f'Сопроводительное письмо*'))[0]
    files_list.remove(soprovod)
    files_list.insert(0, soprovod)

    return files_list


def get_dnsid():
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


if __name__ == '__main__':
    result = get_dnsid()
    print(result)
