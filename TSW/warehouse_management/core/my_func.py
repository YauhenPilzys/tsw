import re
import datetime
from num2words import num2words

""" функция проверяет все ли символы в строке латинские большие и плюс цифры """


def check_truck_number(n):
    if re.search(r'[^A-Z0-9-]', n):  # регулярное выражение, проверка на большие латинские буквы, цифры и дефис
        return False
    else:
        return True


""" функция возвращает последнюю цифру года """


def get_YearN():
    return str(datetime.datetime.now().year)[3]


# now = timezone.now()  - точнее , с учетом часового пояса . from django.utils import timezone

""" функция приводит число к 6 знакам """


def str_6digits(s):
    r = s
    if len(s) < 6:
        r = s.zfill(6)
    return r


"""функция преобразует число в строковое представление с учетом валюты и склонения"""


def number_to_words(number, cur='BYN', l='ru'):
    """функция склоняет выбранную валюту целую часть относительно последней цифры в сумме"""

    def currency_declination(n, c='BYN'):
        if n < 0:
            return ""
        r = ""
        # ('RUB', 'российский рубль'),
        # ('BYN', 'белорусский рубль'),
        # ('EUR', 'евро'),
        # ('USD', 'доллар сша'),
        # ('LTL', 'литовский лит'),
        # ('LVL', 'латвийский лат'),
        # ('KZT', 'казахстанский тенге'),
        # ('UAH', 'украинская гривна'),
        if (c == 'BYN'):
            if (n == 1) or (n > 20 and (n % 10) == 1):
                r = 'белорусский рубль'
            elif (n == 2) or (n == 3) or (n == 4) or (n > 20 and (n % 10) == 2) or (n > 20 and (n % 10) == 3) or (n > 20 and (n % 10) == 4):
                r = 'белорусских рубля'
            else:  # остальные случаи
                r = 'белорусских рублей'
        elif (c == 'RUB'):
            if (n == 1) or (n > 20 and (n % 10) == 1):
                r = 'российский рубль'
            elif (n == 2) or (n == 3) or (n == 4) or (n > 20 and (n % 10) == 2) or (n > 20 and (n % 10) == 3) or (n > 20 and (n % 10) == 4):
                r = 'российских рубля'
            else:  # остальные случаи
                r = 'российских рублей'
        elif (c == 'EUR'):
            r = 'евро'
        elif (c == 'USD'):
            if (n == 1) or (n > 20 and (n % 10) == 1):
                r = 'доллар сша'
            elif (n == 2) or (n == 3) or (n == 4) or (n > 20 and (n % 10) == 2) or (n > 20 and (n % 10) == 3) or (n > 20 and (n % 10) == 4):
                r = 'доллара сша'
            else:  # остальные случаи
                r = 'долларов сша'
        elif (c == 'LTL'):
            if (n == 1) or (n > 20 and (n % 10) == 1):
                r = 'литовский лит'
            else:  # остальные случаи
                r = 'литовских лита'
        elif (c == 'LVL'):
            if (n == 1) or (n > 20 and (n % 10) == 1):
                r = 'латвийский лат'
            else:  # остальные случаи
                r = 'латвийских лата'
        elif (c == 'KZT'):
            if (n == 1) or (n > 20 and (n % 10) == 1):
                r = 'казахстанский тенге'
            else:  # остальные случаи
                r = 'казахстанских тенге'
        elif (c == 'UAH'):
            if (n == 1) or (n > 20 and (n % 10) == 1):
                r = 'украинская гривна'
            elif (n == 2) or (n == 3) or (n == 4) or (n > 20 and (n % 10) == 2) or (n > 20 and (n % 10) == 3) or (n > 20 and (n % 10) == 4):
                r = 'украинские гривны'
            else:  # остальные случаи
                r = 'украинских гривен'
        else:  # остальные валюты просто возвращаем короткое значение самой валюты
            return с
        return r

    # делаю Беорусские рубли, Российские рубли, Доллар США, Евро
    # склонения 1- рубль, 2,3,4 - рубля, 5,6,7,8,9,0 - рублей
    # склонения 1 - копейка, 2,3,4 - копейки, 5,6,7,8,9,0 - копеек
    # склонения 1- доллар, 2,3,4 - доллара, 5,6,7,8,9,0 - долларов
    # склонения 1 - цент, 2,3,4 - цента, 5,6,7,8,9,0 - центов
    """функция склоняет выбранную валюту дробную часть относительно последней цифры в сумме"""

    def fraction_declination(k, c='BYN'):

        r = ''
        if (c == 'BYN') or (c == 'RUB') or (c == 'UAH'):
            if (k == 1) or (k > 20 and (k % 10) == 1):
                r = 'копейка'
            elif (k == 2) or (k == 3) or (k == 4) or (k > 20 and (k % 10) == 2) or (k > 20 and (k % 10) == 3) or (k > 20 and (k % 10) == 4):
                r = 'копейки'
            else:  # остальные случаи
                r = 'копеек'
        elif (c == 'EUR') or (c == 'USD') or (c == 'LTL'):
            if (k == 1) or (k > 20 and (k % 10) == 1):
                r = 'цент'
            else:  # остальные случаи
                r = 'цента'
        elif (c == 'LVL'):
            if (k == 1) or (k > 20 and (k % 10) == 1):
                r = 'сантим'
            else:  # остальные случаи
                r = 'сантима'
        elif (c == 'KZT'):
            if (k == 1) or (k > 20 and (k % 10) == 1):
                r = 'тыин'
            elif (k == 2) or (k == 3) or (k == 4) or (k > 20 and (k % 10) == 2) or (k > 20 and (k % 10) == 3) or (k > 20 and (k % 10) == 4):
                r = 'тыина'
            else:  # остальные случаи
                r = 'тыинов'
        else:  # остальные валюты просто возвращаем короткое значение самой валюты
            return с
        return r

    rubl = int(number)
    # last_c=  # последняя цифра рублей
    kop = int(round((number - rubl) * 100))
    words = num2words(rubl, lang=l).capitalize()
    if kop > 0:
        words += ' ' + currency_declination(rubl, cur) + ' '
        if ((cur == 'BYN') or (cur == 'RUB') or (cur == 'UAH')) and (kop % 10 != 0):  # копейки, когда нет окончания на 0
            s = num2words(kop, lang=l)  # делаем прописью, ошибка будет в последнем слове
            w = s.split()  # делим на слова
            r = ' '.join(w[:-1])  # Объединить все слова, кроме последнего
            if (kop == 1) or (kop % 10 == 1):
                r += ' одна'
            elif (kop == 2) or (kop % 10 == 2):
                r += ' две'
            elif (kop == 3) or (kop % 10 == 3):
                r += ' три'
            elif (kop == 4) or (kop % 10 == 4):
                r += ' четыре'
            elif (kop == 5) or (kop % 10 == 5):
                r += ' пять'
            elif (kop == 6) or (kop % 10 == 6):
                r += ' шесть'
            elif (kop == 7) or (kop % 10 == 7):
                r += ' семь'
            elif (kop == 8) or (kop % 10 == 8):
                r += ' восемь'
            elif (kop == 9) or (kop % 10 == 9):
                r += ' девять'
            words += r
        else:
            words += num2words(kop, lang=l)
        words += ' ' + fraction_declination(kop, cur)
    else:
        words += ' ' + currency_declination(rubl, cur)
    return words
