9 - 5
import requests
from requests.exceptions import HTTPError
# + Регистрация                         add_user(user_name, password)
# + Редоктирование пользователей        user_edit(user_id, user_name, email, password, avatar, active)
# + Информация о пользователях          user_info(user_id)
# + Логин                               login(email, password)
# + Обновления долгоживушего токина     renew
# + Просмотор всей базы                 ls
# # Сортировка
# + Создание строки                     item_add(item_name, status, user_id_1, user_id_2, png_id_name, comments, inventory_id)
# + Удоление строки                     item_delete(item_id)
# + Удоление пользователя               user_delete(user_id)
# + Редоктирование строки               item_edit(item_name, status, user_id_1, user_id_2, png_id_name, comments, inventory_id)
# + Получение иконки                    item_icon_download(item, route)
# + Получение авотарки                  user_icon_download(route)
# Изменение авотарки

server = "http://127.0.0.1:5000/"
icon = "/tmp/"
short_token = ""
live_token = ""


from werkzeug.exceptions import HTTPException
import json
from argparse import Namespace
import hashlib



def obj_dic(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, obj_dic(j))
        elif isinstance(j, seqs):
            setattr(top, i,
                type(j)(obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top





def input(short_token_A, live_token_A):
    global short_token, live_token
    short_token = short_token_A
    live_token = live_token_A



# BEGIN Обработка ошибок.
def handle_exception(e):
    if isinstance(e, requests.exceptions.ConnectTimeout):
        A = '{"number": 524, "response": {"text": "Время ожидания ситекло."}}'
        return json.loads(A, object_hook=lambda d: Namespace(**d))
    elif isinstance(e, requests.exceptions.ReadTimeout):
        A = '{"number": 524, "response": {"text": "Время ожидания ситекло."}}'
        return json.loads(A, object_hook=lambda d: Namespace(**d))
    elif isinstance(e, HTTPError):
        P = f"Произошла другая ошибка: {e}"
        A = '{"number": 520, "response": {"text": "' + P + '"}}'
        return json.loads(A, object_hook=lambda d: Namespace(**d))
    elif isinstance(e, Exception):
        P = f"Произошла другая ошибка: {e}"
        A = '{"number": 520, "response": {"text": "' + P + '"}}'
        return json.loads(A, object_hook=lambda d: Namespace(**d))
    else:
        print('Success!')

def exception_member(response):
    if response.status_code == 412:
        A = {"number": 412, "response": {"text": response.text}}
        print(response.text)
        return json.loads(A, object_hook=lambda d: Namespace(**d))
    if response.status_code == 500:
        A = '{"number": 500, "response": {"text": "Ошибка на стороне сервера."}}'
        print("Ошибка на стороне сервера.")
        return json.loads(A, object_hook=lambda d: Namespace(**d))
    if response.status_code == 401:
        A = '{"number": `, "response": {"text": "Необходима ваторизация."}}'
        print("Необходима ваторизация.")
        return json.loads(A, object_hook=lambda d: Namespace(**d))
    if response.status_code == 426:
        return renew()

# END





def renew():
    global short_token, live_token
    try:
        print("SSS")
        response = requests.get(f'{server}renew/', timeout=(5, 3), headers={'live_token': live_token},)
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    request_L = (response.text)
    SAS = json.loads(request_L)
    short_token = SAS["short_token"]
    live_token  = SAS["live_token"]
    A = {"number": 200, "response": {"text": None}}
    s = obj_dic(A)
    return s



def login(email, password):
    global short_token, live_token
    a = f"{password}".encode('utf-8')
    hash_object = hashlib.sha512(a)
    hex_dig = hash_object.hexdigest()
    print(hex_dig)
    try:
        response = requests.get(f'{server}login/', timeout=(5, 3),  headers={'email': email, 'password': hex_dig},)
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    request_L = (response.text)
    SAS = json.loads(request_L)
    short_token = SAS["short_token"]
    live_token = SAS["live_token"]
    A = {"number": 200, "response": {"text": None, "short_token": short_token, "live_token": live_token}}
    #s = bunchify(A)
    s = obj_dic(A)
    return s


def ls():
    print("SAS")
    try:
        response = requests.get(f'{server}ls/', timeout=(5, 3), headers={'short_token': short_token},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    request_L = (response.text)
    matrix = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "matrix": matrix["ls"]}}
    s = obj_dic(A)
    return s



def item_icon_download(item, route):
    print("SAS")
    try:
        response = requests.get(f'{server}item_icon/{item}', timeout=(5, 3), headers={'short_token': short_token},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)

    with open(route + item, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    A = {"number": 200, "response": {"text": None}}
    s = obj_dic(A)
    return s


def user_icon_download(route):
    print("SAS")
    try:
        response = requests.get(f'{server}avatar_icon/', timeout=(5, 3), headers={'short_token': short_token},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)

    with open(route + "avatar.png", 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    A = {"number": 200, "response": {"text": None}}
    s = obj_dic(A)
    return s

def user_delete(user_id):
    try:
        response = requests.get(f'{server}user_delete/', timeout=(5, 3), headers={'user_id': user_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = obj_dic(A)
    return s

def registration(email, password):
    a = f"{password}".encode('utf-8')
    hash_object = hashlib.sha512(a)
    hex_dig = hash_object.hexdigest()
    try:
        response = requests.get(f'{server}registration/', timeout=(5, 3),  headers={'email': email, 'password': hex_dig},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = obj_dic(A)
    return s

def user_info(user_id):
    try:
        response = requests.get(f'{server}user_info/', timeout=(5, 3), headers={'user_id': user_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    request_L = (response.text)
    user_info_list = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "user_name": user_info_list["user_name"], "email":user_info_list["email"], "avatar":user_info_list["avatar"], "active":user_info_list["active"], "group_id":user_info_list["group_id"], "permission":user_info_list["permission"]}}
    s = obj_dic(A)
    return s


def item_delete(item_id):
    try:
        response = requests.get(f'{server}item_delete/', timeout=(5, 3), headers={'item_id': item_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = obj_dic(A)
    return s


def item_add(item_name, status, user_id_1, user_id_2, png_id_name, comments, inventory_id):
    try:
        response = requests.get(f'{server}item_add/', timeout=(5, 3), headers={'item_name': item_name, 'status': status, 'user_id_1': user_id_1, 'user_id_2': user_id_2, 'png_id_name': png_id_name, 'comments': comments, 'inventory_id': inventory_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    request_L = (response.text)
    Ap = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "item_id": Ap["item_id"]}}
    s = obj_dic(A)
    return s





def user_edit(user_id, user_name, email, password, avatar, active):
    a = f"{password}".encode('utf-8')
    hash_object = hashlib.sha512(a)
    hex_dig = hash_object.hexdigest()
    try:
        response = requests.get(f'{server}user_edit/', timeout=(5, 3), headers={'user_id': user_id, 'user_name': user_name, 'email': email, 'password': hex_dig, 'avatar': avatar, 'active': active},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = obj_dic(A)
    return s



def item_edit(item_name, status, user_id_1, user_id_2, png_id_name, comments, inventory_id):
    try:
        response = requests.get(f'{server}item_edit/', timeout=(5, 3), headers={'item_name': item_name, 'status': status, 'user_id_1': user_id_1, 'user_id_2': user_id_2, 'png_id_name': png_id_name, 'comments': comments, 'inventory_id': inventory_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = obj_dic(A)
    return s



