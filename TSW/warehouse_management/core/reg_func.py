import datetime
import environ
import requests
import jwt
from .directory import *

env = environ.Env(
    DEBUG=(bool, False)
)

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # отключаем сообщения Warrings, что имеется HTTP-запрос без проверки SSL-сертификата

# на сервере создан туннель, через который идет работа с насэд, работать можно только через этот тоннель
# POST https://178.168.146.109:8077/authenticate - аутентификация к API
# GET https://178.168.146.109:8077/range?offset={}&limit={} - запрос записей по диапазону
# GET https://178.168.146.109:8077/regId/{id} - файл по id
# GET https://178.168.146.109:8077/id/{ln_id} - содержимое файла
# GET https://178.168.146.109:8077/guid?file_guid={}&limit={} - файл по GUID
# https://nces.by/wp-content/uploads/TU_EPI_1.3.pdf

url = 'https://178.168.146.109:8077/'
authentication = 'authenticate'
datalogin = {}
datalogin["username"] = env('NASED_USER')
datalogin["password"] = env('NASED_PASSWORD')

# headers = {'Authorization': 'Bearer ' + token}
# response = requests.get('https://178.168.146.109:8077/some_endpoint', headers=headers, verify=False)


# Алгоритм получения данных
#
# вначале получаем диапазон
# https://178.168.146.109:8077/range?offset=0&limit=10
#
# берем file_guid=6017E11F-8B0C-4268-A0E0-D485E56B089E
# делаем запрос
# https://178.168.146.109:8077/guid?file_guid=6017E11F-8B0C-4268-A0E0-D485E56B089E&limit=1
#
# затем в нем берем id, это будет RegID, получаем по нему данные и извлекаем
# https://178.168.146.109:8077/regId/15698483
#
# получем список с несколькими ln_id
# типа такого
# "files": [
#     {
#         "ln_id": 59121582,
#         "date_of": "2024-03-09T11:33:51",
#         "ln_type": 0
#     },
#     {
#         "ln_id": 59121611,
#         "date_of": "2024-03-09T11:34:28",
#         "ln_type": 3
#     }
# ]
#
# теперь делаем запрос по id = ln_id
# https://178.168.146.109:8077/id/59121582
# и получаем данные


"""авторизация в насед"""


def nased_login():  # авторизация, получение token, если авторизация не прошла, то token=None
    res = requests.post(url + authentication, json=datalogin, verify=False)
    if res.status_code == 200:
        # print("Успешная аутентификация!")
        token = res.json().get('token')  # предполагая, что токен возвращается в ответе
        return token
    else:
        return None


""""функция получения данных о насед при разных параметрах"""


def get_nased(param='range', param2=0, param3=0, token=nased_login()):
    r = {}
    if token is None:  # если токен пустой, то получаем токен
        token = nased_login()
    headers = {"Authorization": f"Bearer {token}"}
    if param == 'range':
        n_url = url + 'range?offset=' + str(param2) + '&limit=' + str(param3)
    elif param == 'regId':
        n_url = url + 'regId/' + str(param2)
    elif param == 'id':
        n_url = url + 'id/' + str(param2)
    elif param == 'guid':
        n_url = url + 'guid?file_guid=' + str(param2)
        if param3 != 0:
            n_url = n_url + '&limit=' + str(param3)
        else:
            n_url = n_url + '&limit=1'
    else:
        r = {'ERROR': 'неправильно задан первый параметр функции get_nased, варианты: range, regId, id, guid'}
        return r
    try:
        print('response send')
        print(n_url)

        response = requests.get(n_url, headers=headers, verify=False)

        print('headers')
        print(headers)

        print('response end')
        print(response)

        if response.status_code == 200:
            return response.text  # JSON
        else:  # если token стал недействительным, пробуем еще раз
            token = nased_login()  # получаем новый
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(n_url, headers=headers, verify=False)
            if response.status_code == 200:
                return response.text  # JSON
            else:
                description = HTTP_ANSWER.get(str(response.status_code), 'Неизвестный код состояния')
                r = {'ERROR': description}
                return r
    except Exception as e:
        r = {'ERROR': str(e)}
        return r
