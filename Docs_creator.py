from docxtpl import DocxTemplate
import jinja2
import os


class Letter:
    jinja_env = jinja2.Environment()
    rend = {'адресат': 'адресат', 'должность_адресата': 'должность_адресата', "фио_адресата": "фио_адресата", 'адрес_адресата': 'адрес_адресата',
            'номер': 'номер', 'дата_номера': 'дата_номера', 'тема_письма': 'тема_письма',
            'пишет_с_целью': 'пишет_с_целью',
            'просим_о': 'просим_о', 'текст_письма': 'текст_письма', 'должность_подписанта': 'должность_подписанта',
            'фио_подписанта': 'фио_подписанта', 'фио_исполнителя': 'фио_исполнителя',
            'телефон_исполнителя': 'телефон_исполнителя'}

    def __init__(self, template: str = "C:\\Users\zaitsev_ad\PycharmProjects\WORK_sed\шаблоны\основные\Шаблон письма.docx"):
        self.template = template

    def create(self, **render_dict):
        doc = DocxTemplate(self.template)
        adressat = 'No adressat'
        dict_to_render = {}
        for tag, value in render_dict.items():
            if tag == 'адресат':
                adressat = value
            if value:
                dict_to_render[tag] = value
        doc.render(dict_to_render, self.jinja_env)
        doc.save(os.path.join("C:\\Users\zaitsev_ad\Desktop\some dir", f'Сопроводительное письмо {adressat}.docx'))


if __name__ == '__main__':
    Letter().create(
        адресат="Минздрав России",
        должность_адресата=None,
        фио_адресата=None,
        адрес_адресата=None,
        номер="                       ",
        дата_номера=None,
        тема_письма="О необходимости изменений в приказ Минздрава №90н",
        пишет_с_целью=None,
        доносит_о="просит рассмотреть внесение изменений в приказ",
        текст_письма=None,
        должность_подписанта="Статс-секретарь –\nзаместитель руководителя",
        фио_подписанта="М.С. Орлов",
        фио_исполнителя="Зайцев Алексей Дмитриевич",
        телефон_исполнителя="8-499-973-16-53",
    )
