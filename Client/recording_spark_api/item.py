9 - 5
import requests
from requests.exceptions import HTTPError
import os
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

# - - Лайв токен теперь безсмертный и многорназовый.
# + !!!Лайв токет смертный и одноразовый!!!

from werkzeug.exceptions import HTTPException
import json
from argparse import Namespace
import hashlib
import error_handling
#import recording_spark_api
from error_handling import *
import __init__

# error_handling.

def SAS(A):
    return A




def icon_download(item, route):
    print("SAS")
    print(str(item))
    try:
        #response = requests.get(f'{__init__.server[0]}item_icon/', timeout=(5, 3), headers={'short_token': __init__.short_token[0], 'SAS': "SSSSSSS"},)
        response = requests.get(f'{__init__.server[0]}ls_item_icon/', timeout=(5, 3), headers={'short_token': __init__.short_token[0], 'item_id': str(item)},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return icon_download(item, route)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)

    with open(route + "/" + str(item), 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s






def rm(item_id):
    try:
        response = requests.get(f'{__init__.server[0]}item_rm/', timeout=(5, 3), headers={'short_token': __init__.short_token[0]}, json = {'item_id': item_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return rm(item_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s


def add(item_name, status, user_id_1, user_id_2, comments, inventory_id):
    try:
        response = requests.get(f'{__init__.server[0]}item_add/', timeout=(5, 3), headers={'short_token': __init__.short_token[0]}, json = {'item_name': item_name, 'status': status, 'user_id_1': user_id_1, 'user_id_2': user_id_2, 'comments': comments, 'inventory_id': inventory_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return add(item_name, status, user_id_2, icon, comments, inventory_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    request_L = (response.text)
    Ap = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "item_id": Ap["item_id"]}}
    s = error_handling.obj_dic(A)
    return s


def edit(item_id, item_name, status, user_id_1, user_id_2, comments, inventory_id):
    try:
        response = requests.get(f'{__init__.server[0]}item_edit/', timeout=(5, 3), headers={'short_token': __init__.short_token[0]}, json = {'item_id': item_id, 'item_name': item_name, 'status': status, 'user_id_1': user_id_1, 'user_id_2': user_id_2, 'comments': comments, 'inventory_id': inventory_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return edit(item_id, item_name, status, user_id_1, user_id_2, png_id_name, comments, inventory_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s


def add_icon(item_id, icon):
    try:
        test_file = open(icon, "rb")
        files = {'file': ('item.png', test_file, {'Expires': '0'})}
        response = requests.get(f'{__init__.server[0]}add_item_icon/', headers={'short_token': __init__.short_token[0], 'item_id': str(item_id)}, files=files)
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return add_icon(item_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return exception_member(response)

        if response.status_code == 200:
            A = {"number": 200, "response": {"text": None}}
            s = error_handling.obj_dic(A)
            return s
    except Exception as e:
        return handle_exception(e)


def rm_icon(item_id):
    try:
        response = requests.get(f'{__init__.server[0]}rm_item_icon/', timeout=(5, 3), headers={'short_token': __init__.short_token[0], "item_id": str(item_id)}, )
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return rm_icon(item_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s



def ls_icon(item_id):
    try:
        if not os.path.isdir(f"{__init__.route[0]}/item/"):
            os.mkdir(f"{__init__.route[0]}/item/")
        response = requests.get(f'{__init__.server[0]}ls_item_icon/', headers={'short_token': __init__.short_token[0], 'item_id': str(item_id)},)
        if response.status_code == 426:
            P = exception_member(response)
            if P.number == 200:
                return ls_icon(item_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return exception_member(response)
        if response.status_code == 200:
            with open(f"{__init__.route[0]}/item/{item_id}", 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            A = {"number": 200, "response": {"text": None}}
            s = error_handling.obj_dic(A)
            return s
    except Exception as e:
        return handle_exception(e)




