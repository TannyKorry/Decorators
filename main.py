import datetime
import os
import re
######################### ПРОСТОЙ ДЕКОРАТОР ##############################

def logger_(old_function):
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        with open('main.log', 'a') as f:
            f.write(f'Data: {datetime.datetime.now()}\n'
                    f'name function: {old_function.__name__}\n'
                    f'parameters: {args}, {kwargs}\n')
            result = old_function(*args, **kwargs)
            f.write(f'result: {result}\n\n')
        return result
    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger_
    def hello_world():
        return 'Hello World'

    @logger_
    def summator(a, b=0):
        return a + b

    @logger_
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


######################### ПАРАМЕТРИЗОВАННЫЙ ДЕКОРАТОР #############################


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            # result = old_function(*args, **kwargs)
            with open(path, 'a') as f:
                f.write(f'Data: {datetime.datetime.now()}\n'
                        f'name function: {old_function.__name__}\n'
                        f'parameters: {args}, {kwargs}\n')
                result = old_function(*args, **kwargs)
                f.write(f'result: {result}\n\n')
            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

######################### СВОЙ ПРИМЕР #########################

cont = [
    ['Мартиняхин Виталий Геннадьевич', '', '', 'ФНС', '', '+74959130037', ''],
    ['Наркаев', 'Вячеслав Рифхатович', '', 'ФНС', '', '8 495-913-0168', '']
]


@logger(path='log_2.log')
def arrange(contacts):
    for c in contacts:
        item = ' '.join(c[:3]).split(' ')
        c[:3] = item[:3]
    return contacts


@logger_
def format_num(contacts):
    contact_list = []
    for contact in arrange(contacts):
        pattern = r'(\+7|8)\s*\(?(\d{3})\)?[\s|-]?(\d{3})[\s|-]?(\d{2})[\s|-]?(\d{2})\s*\(?([д][о]?[б]?[.]?\s*\d+)?\)?'
        substitution = r'+7(\2)\3-\4-\5 \6'
        res = re.sub(pattern, substitution, contact[5])
        contact[5] = res
        contact_list.append(contact)
    return contact_list


if __name__ == '__main__':
    # Задание 1
    test_1()
    # Задание 2
    test_2()
    # Задание 3
    format_num(cont)