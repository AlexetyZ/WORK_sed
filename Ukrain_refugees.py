import os
import datetime
import shutil
import locale


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class File_operation:

    def __init__(self):
        pass
    def create_file_for_today(self):
        basic_file_name = self.find_fresh_basic_file()
        print(basic_file_name)
        period_dates = [datetime.datetime.now()]
        self.copy_from_basic_files(period_dates, basic_file_name)
        return 'Successful creating file for today!'

    def create_files_for_a_period(self):
        period_dates = self.get_dates_interval()
        basic_file_name = self.get_input_base_file_name()
        self.copy_from_basic_files(period_dates, basic_file_name)

    def copy_from_basic_files(self, period_dates, basic_file_name):
        for date in period_dates:
            additional_dir = f"Z:\\ПВР таблицы\\{date.strftime('%B').lower()}\\ПВР {date.strftime('%d.%m.%Y')}"
            if os.path.exists(additional_dir):
                print('такая папка есть')
                print(os.path.dirname(additional_dir))
                pass
            else:
                print('такой папки нет')
                os.mkdir(additional_dir)
            shutil.copyfile(basic_file_name, f"{additional_dir}\\Таблица ПВР {date.strftime('%d.%m.%Y')}.xls")
        return 'Success to copy'

    def find_fresh_basic_file(self):
        day_ago = 0
        date = datetime.datetime.now()-datetime.timedelta(days=day_ago)
        while True:
            date = datetime.datetime.now() - datetime.timedelta(days=day_ago)
            filename = f"Z:\\ПВР таблицы\\{date.strftime('%B').lower()}\ПВР {date.strftime('%d.%m.%Y')}\\Таблица ПВР {date.strftime('%d.%m.%Y')}.xls"
            # print(f'try {filename}')
            if os.path.exists(filename):

                return filename
            else:
                day_ago += 1
                if day_ago > 50:
                    break
                continue





    def get_dates_interval(self):
        dates = []
        date_start = datetime.datetime.strptime(input('введите дату начала в формате дд.мм.гггг'), '%d.%m.%Y')
        date_end = datetime.datetime.strptime(input('введите дату окончания в формате дд.мм.гггг'), '%d.%m.%Y')
        # print(f'{type(date_start)=} \n {type(date_end)=}')
        day_count = (date_end - date_start).days + 1
        for day in range((date_end - date_start).days+1):
            date = (date_start + datetime.timedelta(days=day))
            week_days = [1, 2, 3, 4, 5]
            # print(date.strftime('%w'))
            if int(date.strftime('%w')) in week_days:
                dates.append(date)
        return dates

    def get_input_base_file_name(self):
        file_name = input('абсолютное имя базового файла')
        file_name = file_name.replace(file_name[:1], '').replace(file_name[:-1], '')
        if os.path.exists(file_name):
            return file_name

    def main(self):
        self.get_input_base_file_name()
        # create_dirs_for_datas()


if __name__ == "__main__":

    # try:
    result = File_operation().create_file_for_today()

    print(result)
    # except Exception as ex:
    #     print(ex)
    input('Press Enter for exit')