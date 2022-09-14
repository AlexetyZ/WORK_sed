#! / usr / bin / python
# - * - кодировка: latin-1 - * -
import os
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

import datetime
from collections import OrderedDict
import re
import pymorphy2
import jinja2
from docxtpl import DocxTemplate
from sql import Database




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


class PrintD:
    def __init__(self):
        id_o = 6
        properties = 'МБДОУ'
        only_name = '"Детский сад № 112 "Жемчужинка"'
        inn = '5255136545'
        address = "г.Нижний Новгород, ул. Лескова, дом 11А"
        groups = "№1, №2"
        date_start = '2022-02-16'
        date_end = '2022-02-23'

        self.doc_print_ORVI(id_o=id_o, properties=properties, only_name=only_name, inn=inn, address=address, groups=groups, date_start=date_start, date_end=date_end)

    def doc_print_ORVI(self, id_o, properties, only_name, inn, address, groups, date_start, date_end):

        day = datetime.datetime.now().strftime('%d')
        month = datetime.datetime.now().strftime('%B')
        month_RP = Decline().wordskl(month, 'gent')
        year = datetime.datetime.now().strftime('%Y')

        tadate = f'{day} {month_RP} {year}'

        known_properties = {"ГБДОУ": {"property_ful": 'государственное бюджетное дошкольное образовательное учреждение', "group_kind": 'группе', "group_kind_P": 'группах', "person_kind": 'воспитанник', "person_kind_P": 'воспитанников'}, "ГБОУ": {"property_ful": 'государственное бюджетное общеобразовательное учреждение', "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик', "person_kind_P": 'учеников'}, "ГБПОУ НО": {"property_ful": 'государственное бюджетное профессиональное образовательное учреждение Нижегородской области', "group_kind": 'группе', "group_kind_P": 'группах', "person_kind": 'студент', "person_kind_P": 'студентов'}, "ГКОУ": {"property_ful": 'государственное казенное общеобразовательное учреждение', "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик', "person_kind_P": 'учеников'}, "МАДОУ": {"property_ful": 'муниципальное автономное дошкольное образовательное учреждение', "group_kind": 'группе', "group_kind_P": 'группах', "person_kind": 'воспитанник', "person_kind_P": 'воспитанников'}, "МАОУ": {"property_ful": 'муниципальное автономное общеобразовательное учреждение', "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик', "person_kind_P": 'учеников'}, "МБДОУ": {"property_ful": 'муниципальное бюджетное дошкольное образовательное учреждение', "group_kind": 'группе', "group_kind_P": 'группах', "person_kind": 'воспитанник', "person_kind_P": 'воспитанников'}, "МБОУ": {"property_ful": 'муниципальное бюджетное общеобразовательное учреждение', "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик', "person_kind_P": 'учеников'}, "ЧОУ РО": {"property_ful": 'частное общеобразовательное учреждение религиозной организации', "group_kind": 'классе', "group_kind_P": 'классах', "person_kind": 'ученик', "person_kind_P": 'учеников'}}
        print(groups)
        if re.search(",", groups):
            group_kind_PP = known_properties[properties]['group_kind_P']

        else:
            group_kind_PP = known_properties[properties]['group_kind']

        person_kind_RP = known_properties[properties]['person_kind_P']

        jinja_env = jinja2.Environment()

        doc = DocxTemplate(f"{os.path.dirname(__file__)}\шаблоны\закрытие учреждения по ОРВИ.docx")
        doc.render({'tadate': tadate,
                    'properties': properties,
                    'only_name': only_name,
                    'inn': inn,
                    'address': address,
                    'groups': groups,
                    'group_kind_PP': group_kind_PP,
                    'person_kind_RP': person_kind_RP,
                    'date_start': date_start,
                    'date_end': date_end,}, jinja_env
                   )

        doc.save(f"{os.path.dirname(__file__)}\напечатанные\{id_o}.doc")



Database().assign_number()



# if __name__ == "__main__":
#     PrintD()
