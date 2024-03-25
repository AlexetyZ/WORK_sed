def exp():
    import re

    js_code = "alert('Hello, World!')"

    # Заменяем eval на функцию, которая принимает строку кода и выполняет ее
    exec_js_code = re.sub(r"eval\(", r"eval(function* (\)\ { return (\(\); }) ", js_code)

    # Выполняем полученный код
    eval(exec_js_code)


def exp1(arg1='arg1', arg2='arg2'):
    print(arg1, arg2)


def exp2():
    args = {'arg1': 'arg1cus', 'arg2': 'arg2cus'}
    exp1(**args)



if __name__ == "__main__":
    exp2()