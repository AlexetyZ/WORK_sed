import requests
from bs4 import BeautifulSoup
from requests import Session
from pprint import pprint
import createDocs as CD

session = Session()

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'ru,en;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': '_ym_uid=1711123323551877635; _ym_d=1711123323; _ym_isad=1; XSRF-TOKEN=eyJpdiI6InBxbUxCRGNINGZaeW1pVkozNW5Ubnc9PSIsInZhbHVlIjoibEtmdmxGemhTTzVVam8yb2RaWEdvUWNtTnQwUThVMEpaSlA5dGhacDVTMVRLNWJGN2dEaXJYZ3Q1MzlET2toVFJuMktRU3lLTExFbm95cTZQTDNHUEt5T0ptZVpvOEs5R2tSUktKMGkvSFBGZTFKSmNyczVIVitkakpDMkxmQzUiLCJtYWMiOiJlYjQzNjQ3ODlmYjM2MDY4YjZiOTcwMjZmZTg4M2FjYTVlYTJmYTk2YTM4Y2UwMmNjMjNmNjA2NTVmZTU0ZDk3IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6ImN0SlR1MUs4Z1BDR1BmaHk2WGhUVUE9PSIsInZhbHVlIjoiLzgzaEYyZ1RSdVRuS3p4eFRwa28zUFRETDhZUjVvbHorM0J5ZlJNYXBOSklyeVYweUFreEV0MFRVVWFhVmppd0IzbUd1SkZpL0hYVkd6U1ZuWENTbG5tamViZGZaQnpEVWsxL3o5akkrQ0hmNjhiWHVoZFlCamtTa3dNK25rVjAiLCJtYWMiOiJhNmM5OWZjNTQ3NGJjZWYyYTljNGQyZjgyMDQwN2QzMmFiMzM0ODUxNDhkODE1MjNhMTdhYWFiZDg3Y2ViNjI4IiwidGFnIjoiIn0%3D',
    'Referer': 'http://komitet-zdorov.duma.gov.ru/about/sostav-komiteta',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.807 YaBrowser/23.11.1.807 (corp) Yowser/2.5 Safari/537.36',
    'X-Client-IP': '127.0.0.1',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XSRF-TOKEN': 'eyJpdiI6InBxbUxCRGNINGZaeW1pVkozNW5Ubnc9PSIsInZhbHVlIjoibEtmdmxGemhTTzVVam8yb2RaWEdvUWNtTnQwUThVMEpaSlA5dGhacDVTMVRLNWJGN2dEaXJYZ3Q1MzlET2toVFJuMktRU3lLTExFbm95cTZQTDNHUEt5T0ptZVpvOEs5R2tSUktKMGkvSFBGZTFKSmNyczVIVitkakpDMkxmQzUiLCJtYWMiOiJlYjQzNjQ3ODlmYjM2MDY4YjZiOTcwMjZmZTg4M2FjYTVlYTJmYTk2YTM4Y2UwMmNjMjNmNjA2NTVmZTU0ZDk3IiwidGFnIjoiIn0=',
}


def getKomList(url):
    params = {
        'hash': 'eyJwYXRoIjoiL2Fib3V0L3Nvc3Rhdi1rb21pdGV0YSJ9',
    }
    response = requests.get(
        url,
        params=params,
        # cookies=cookies,
        headers=headers,
        verify=False,
    ).json()
    return sorted(list(response['data']['components'].values())[0]['data']['data'], key=lambda x: x['title'])


def save_in_doc(kom_list, komitetName):
    """

    :param kom_list: желательно из функции getKomList();
    :param komitetName: писать название комитета без слова "Комитет" в начале, например "'Государственной Думы по охране здоровья'"
    :return:
    """
    result = []
    for p in kom_list:
        if p['position']:
            position = ' '.join([p['position'], komitetName])
        else:
            position = f'Член комитета {komitetName}'
        image = save_picture(p['image'])
        result.append([image, p['title'], position])
    CD.createTable(*result)
    CD.save_doc(f'комиитет {komitetName}.docx')


def save_picture(url):
    fileName = url.split('/')[-1]
    request = session.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.807 YaBrowser/23.11.1.807 (corp) Yowser/2.5 Safari/537.36'})
    with open(f'downloadedFiles/{fileName}.jpg', 'wb') as file:
        file.write(request.content)
    return f'<image>downloadedFiles/{fileName}.jpg'





def main():
    url = 'http://komitet-zdorov.duma.gov.ru/api/route'
    save_in_doc(getKomList(url), 'Государственной Думы по охране здоровья')
    #
    # url = 'http://komitet-zdorov.duma.gov.ru/api/files/c28de5bd-0339-4ac2-8863-b54491ed16a3'
    # save_picture(url)


if __name__ == '__main__':
    main()
