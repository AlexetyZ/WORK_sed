import schedule
from Backend_controller import ChekNew
import datetime
def run_check():
    print('')
    print(datetime.datetime.now())
    try:
        ChekNew()
        ChekNew()
    except Exception as ex:
        print('')
        print('Возникла ошибка!!!!')
        print('')
        print(ex)

def main():
    et = input('Введите периодичность запуска(минуты)   ')
    print(f'start backend... каждые(ую) {et} минут(у)')
    run_check()
    schedule.every(int(et)).minutes.do(run_check)
    while True:

        schedule.run_pending()


if __name__=='__main__':
    main()

