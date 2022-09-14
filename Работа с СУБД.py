import re
import time

import pymysql
import openpyxl
import datetime
from sql import Database
from LittleHelpers.Provider import Find_in_egrul


def base():
    cursor.execute("SHOW tables")
    exite = cursor.fetchall()
    print(exite)


def create_table():
    cursor.execute("CREATE table indocker_db(id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, district varchar(250), property varchar(250), only_name varchar(250), full_name varchar(250), adress varchar(250), director_fio varchar(250), email varchar(250), inn bigint, sed_name varchar(250))")


def create_database():
    wb = openpyxl.load_workbook("данные.xlsx")
    sh = wb.worksheets[0]
    lenf = len(sh['B:B'])
    print(lenf)

    for i in range(2, lenf + 1):
        district = sh[f'B{i}'].value
        properties = sh[f'E{i}'].value
        only_name = sh[f'F{i}'].value
        address = sh[f'G{i}'].value
        fio_director = sh[f'X{i}'].value
        e_mail = sh[f'N{i}'].value
        inn = sh[f'O{i}'].value
        ogrn = '1020938367'
        sed_name = sh[f'Y{i}'].value

        print(sed_name)
        # cursor.execute(f"""INSERT INTO sadidi_sadik(district, properties, only_name, address, fio_director, e_mail,
        # inn, ogrn, sed_name) VALUES ('{district}', '{properties}', '{only_name}', '{address}', '{fio_director}', '{e_mail}',
        # '{inn}', '{ogrn}', '{sed_name}')""")
    con.commit()


def get_sadik_info(old_id):

    cursor1.execute(f"Select inn FROM sadidi_sadik where id='{old_id}'")
    result = cursor1.fetchall()
    inn = result[0][0]

    cursor.execute(f"Select id FROM sadidi_sadik where inn='{inn}'")
    result2 = cursor.fetchall()
    new_id = result2[0][0]
    return new_id

def get_sadik_egrul_name_(only_name):

    cursor1.execute(f"Select inn FROM sadidi_sadik where inn='{only_name}'")
    result = cursor1.fetchall()
    inn = result[0][0]

    ogrn_name = Find_in_egrul().find_egrul2(inn)
    return ogrn_name

def get_sadik_alter_name(alter_name):

    cursor1.execute(f"Select inn FROM sadidi_sadik where only_name='{alter_name}'")
    result = cursor1.fetchall()
    inn = result[0][0]
    same = Find_in_egrul().find_egrul2(inn)
    cursor.execute(f"Select only_name FROM sadidi_sadik where inn='{inn}'")
    result2 = cursor.fetchall()
    same_name = result2[0][0]
    return same_name


def add_ord(ords):
    for ord in ords:
        # print(ord)
        collective = ord[1]
        group_size = ord[2]
        date_start = ord[3]
        date_end = ord[4]
        reason = ord[5]
        fio_covid = ord[6]
        last_day = ord[7]
        identify_day = ord[8]
        sadik_id = get_sadik_info(ord[9])
        fio_post = ord[10]
        address_spec = ord[11]
        status = ord[12]
        doc_number = ord[13]
        ord_date = ord[14]




        try:
            cursor.execute(f"""INSERT INTO sadidi_ordinary(collective, group_size, date_start, date_end, reason, fio_covid, fio_post, last_day, identify_day, address_spec, status, doc_number, ord_date, sadik_id) VALUES ("{collective}", "{group_size}", "{date_start}", "{date_end}", "{reason}", "{fio_covid}", "{fio_post}", "{last_day}", "{identify_day}", "{address_spec}", "{status}", "{doc_number}", "{ord_date}", "{sadik_id}")""")
            con.commit()
        except:
            continue


def get_sadik_id(name):
    # print(name)
    cursor.execute(f"SELECT id FROM sadidi_sadik where only_name='{name}'")
    result = cursor.fetchall()[0][0]

    print(cursor.fetchall())
    return result


def get_sadik_name(id):
    # print(name)
    cursor1.execute(f"SELECT only_name FROM sadidi_sadik where id='{id}'")
    result = cursor1.fetchall()[0][0]

    return result


def get_info_from_mysql():
    cursor1.execute("SELECT * FROM sadidi_ordinary")
    # cursor.execute("SELECT count(*) FROM sadidi_ordinary where groups='полностью'")
    result = cursor1.fetchall()
    return result


def get_info_from_old_ordinary_databases():
    info = get_info_from_mysql()
    print(info)
    for i in info:
        print(i[9])
        new_only_name = get_sadik_name(int(i[9]))
        alter_only_name = get_sadik_alter_name(new_only_name)
        egrul_name = Find_in_egrul().find_egrul2()
        groups = i[1]
        group_size = i[2]
        date_start = i[3]
        date_end = i[4]
        address_spe = i[11]
        status = i[12]
        doc_number = i[13]

        print(f'Sadik ---- {new_only_name}              alter name-------{alter_only_name}')
        print(f'Закрытые коллективы ---- {groups}')
        print(f'Численность закрываемого коллектива ---- {group_size}')
        print(f'Дата начала ---- {date_start}')
        print(f'Дата окончания ---- {date_end}')
        print(f'Адрес учреждения ---- {address_spe}')
        print(f'Статус документа ---- {status}')
        print(f'Номер документа ---- {doc_number}')
        print('')
        print('')
        print('')


try:
    con = pymysql.connect(
        user='root',
        password='ntygazRPNautoz',
        host='127.0.0.1',
        port=3307,
        database='django'
    )
    cursor = con.cursor()
    # get_info_from_mysql()



    con1 = pymysql.connect(
        user='root',
        password='ntygazRPNautoz',
        host='127.0.0.1',
        port=3308,
        database='django'
    )
    cursor1 = con1.cursor()
    # get_info_from_mysql()


except Exception as ex:
    print(ex)
    if re.search("2003", ex, re.I) != None:
        pass
    print('контейнер БД не крутится')

inn = 5256047180
egrul_name = get_sadik_name_from_inn(inn)
print(egrul_name['c'])
# get_info_from_old_ordinary_databases()
# create_table()
# create_database()
# add_ord()
# ords = get_info_from_mysql()
# add_ord(ords)



