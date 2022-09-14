import re

from sql import Database
print(f'всего действующих постановлений {len(Database().get_info())}')
print("")
districts = ['Ленинский', 'Автозаводский', 'Богородский']

known_properties = {"ГБДОУ": "Детский сад",
                        "ГБОУ": "Школа",
                        "ГБПОУ НО": "Колледж",
                        "ГКОУ": "Школа",
                        "МАДОУ": "Детский сад",
                        "МАОУ": "Школа",
                        "МБДОУ": "Детский сад",
                        "МБОУ": "Школа",
                        "ЧОУ РО": "Школа"}
for distr in districts:
    print(distr)
    print_all = Database().get_current_date_ordinaries(distr)

    # print(print_all)

    full_ordered_schools = []
    full_ordered_sadiks = []
    full_ordered_college = []


    full_ordered_schools_covid = []
    full_ordered_sadiks_covid = []
    full_ordered_college_covid = []


    partially_ordered_schools = []
    partially_ordered_sadiks = []
    partially_ordered_college = []


    partially_ordered_schools_covid = []
    partially_ordered_sadiks_covid = []
    partially_ordered_college_covid = []





    for i in print_all:
        sadik_info = Database().get_sadik_info(i[9])
        district = sadik_info[0][1]

        for p in known_properties:
            if p == sadik_info[0][2]:
                kind_org = known_properties[p]

        covid = i[5]

        if re.search('полн', i[1]):
            zakritie = 'полностью'




        else:
            zakritie = len(re.findall(',', i[1])) + 1

        if zakritie == 'полностью' and kind_org == 'Школа':
            full_ordered_schools.append(i)
            if covid == 1:
                full_ordered_schools_covid.append(i)

        if zakritie == 'полностью' and kind_org == 'Детский сад':
            full_ordered_sadiks.append(i)
            if covid == 1:
                full_ordered_sadiks_covid.append(i)

        if zakritie == 'полностью' and kind_org == 'Колледж':
            full_ordered_college.append(i)
            if covid == 1:
                full_ordered_college_covid.append(i)

        if zakritie != 'полностью' and kind_org == 'Школа':
            partially_ordered_schools.append(i)
            if covid == 1:
                partially_ordered_schools_covid.append(i)

        if zakritie != 'полностью' and kind_org == 'Детский сад':
            partially_ordered_sadiks.append(i)
            if covid == 1:
                partially_ordered_sadiks_covid.append(i)

        if zakritie != 'полностью' and kind_org == 'Колледж':
            partially_ordered_college.append(i)
            if covid == 1:
                partially_ordered_college_covid.append(i)


    print(f'Полностью закрытых школ - {len(full_ordered_schools)}')
    print(f'Из них с ковидом - {len(full_ordered_schools_covid)}')
    summ = 0
    for sadik in full_ordered_schools:
        summ += int(sadik[2])
    print(f'Количество учащихся на карантине {summ}')


    print(f'Полностью закрытых Детских садов - {len(full_ordered_sadiks)}')
    print(f'Из них с ковидом - {len(full_ordered_sadiks_covid)}')
    summ = 0
    for sadik in full_ordered_sadiks:
        summ += int(sadik[2])
    print(f'Количество учащихся на карантине {summ}')

    print(f'Полностью закрытых коллеждей - {len(full_ordered_college)}')
    print(f'Из них с ковидом - {len(full_ordered_college_covid)}')
    summ = 0
    for sadik in full_ordered_college:
        summ += int(sadik[2])
    print(f'Количество учащихся на карантине {summ}')

    print(f'Частично закрытых школ - {len(partially_ordered_schools)}')
    print(f'Из них с ковидом - {len(partially_ordered_schools_covid)}')
    summ_group = 0
    for sadik in partially_ordered_schools:
        summ_group += len(re.findall(',', sadik[1])) + 1
    print(f'Количество закрытых классов {summ_group}')






    print(f'Частично закрытых Детских садов - {len(partially_ordered_sadiks)}')
    print(f'Из них с ковидом - {len(partially_ordered_sadiks_covid)}')
    summ_group = 0
    for sadik in partially_ordered_sadiks:
        summ_group += len(re.findall(',', sadik[1])) + 1
    print(f'Количество закрытых групп {summ_group}')


    print(f'Частично закрытых коллеждей - {len(partially_ordered_college)}')
    print(f'Из них с ковидом - {len(partially_ordered_college_covid)}')
    summ_group = 0
    for sadik in partially_ordered_college:
        summ_group += len(re.findall(',', sadik[1])) + 1
    print(f'Количество закрытых групп {summ_group}')

    print(partially_ordered_sadiks)



    print('')