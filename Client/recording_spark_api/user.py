import requests
from requests.exceptions import HTTPError
#from .error_handling import *
from error_handling import *
import error_handling
import __init__
#from .recording_spark_api import *
import mein
#from .mein import *

#from werkzeug.exceptions import HTTPException
import json
from argparse import Namespace
import hashlib

def SAS(A):
    __init__.Ln.append(A)
    #print(A)
    #print(__init__.short_token)
    print(__init__.Ln)
    return __init__.Ln

def registration(email, password): # +
    print(__init__.server)
    a = f"{password}".encode('utf-8')
    hash_object = hashlib.sha512(a)
    hex_dig = hash_object.hexdigest()
    try:
        response = requests.get(f'{__init__.server[0]}registration/', timeout=(5, 3),  headers={'email': email, 'password': hex_dig},)
        print(f"SAS - {response.status_code}")
        if response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    request_L = (response.text)
    id = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "id": id["id"],}}
    s = error_handling.obj_dic(A)
    return s

def edit(user_id, user_name, email, password, avatar, active): # -
    global short_token, server
    a = f"{password}".encode('utf-8')
    hash_object = hashlib.sha512(a)
    hex_dig = hash_object.hexdigest()
    try:
        response = requests.get(f'{__init__.server[0]}user_edit/', timeout=(5, 3), headers={'short_token': __init__.short_token[0], 'user_id': user_id, 'user_name': user_name, 'email': email, 'password': hex_dig, 'avatar': avatar, 'active': active},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.exception_member(response)
            if P.number == 200:
                return edit(user_id, user_name, email, password, avatar, active)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s

def info(user_id): # +
    try:
        response = requests.get(f'{__init__.server[0]}user_info/', timeout=(5, 3), headers={'short_token': __init__.short_token[0], 'user_id': str(user_id)},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.exception_member(response)
            if P.number == 200:
                return info(user_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    request_L = (response.text)
    user_info_list = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "user_name": user_info_list["user_name"], "email":user_info_list["email"], "avatar":user_info_list["avatar"], "active":user_info_list["active"], "group_id":user_info_list["group_id"], "permission":user_info_list["permission"]}}
    s = error_handling.obj_dic(A)
    return s


def icon_download(route): # +
    print("SAS")
    try:
        response = requests.get(f'{__init__.server[0]}ls_avatar_icon/', timeout=(5, 3), headers={'short_token': __init__.short_token[0], 'uid': route},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.exception_member(response)
            if P.number == 200:
                return icon_download(route)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)

    with open(route + "/avatar.png", 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s





def delete(user_id): # -
    try:
        response = requests.get(f'{__init__.server[0]}user_delete/', timeout=(5, 3), headers={'short_token': __init__.short_token[0], 'user_id': user_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.exception_member(response)
            if P.number == 200:
                return delete(user_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s


def ls():
    try:
        response = requests.get(f'{server[0]}user_ls/', timeout=(5, 3), headers={'short_token': __init__.short_token[0]},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.exception_member(response)
            if P.number == 200:
                return ls()
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    request_L = (response.text)
    matrix = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "matrix": matrix["ls"]}}
    s = error_handling.obj_dic(A)
    return s

def exiting_session():
    0

def kill_session(user_id, live_token, server):
    try:
        response = requests.get(f"{server}kill_session/", timeout=(5, 3), headers={"live_token":live_token, "user_id": str(user_id)})
        if response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s


def add(user_name, email, password, avatar, active, group_id):
    try:
        a = f"{password}".encode('utf-8')
        hash_object = hashlib.sha512(a)
        hex_dig = hash_object.hexdigest()

        response = requests.get(f'{__init__.server[0]}user_add/', timeout=(5, 3), headers={'short_token': __init__.short_token[0]}, json = {"user_name": user_name, "email": email, "password": hex_dig, "avatar": avatar, "active": active, "group_id": group_id})
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.exception_member(response)
            if P.number == 200:
                return add(user_name, email, password, avatar, active, group_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    request_L = (response.text)
    A = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "user_id": A["user_id"]}}
    s = error_handling.obj_dic(A)
    return s

def edit(user_id, user_name, email, password, avatar, active, group_id):
    try:
        if password == None:
            hex_dig = None
        else:
            a = f"{password}".encode('utf-8')
            hash_object = hashlib.sha512(a)
            hex_dig = hash_object.hexdigest()

        response = requests.get(f'{__init__.server[0]}user_edit/', timeout=(5, 3), headers={'short_token': __init__.short_token[0]}, json = {"user_id": user_id, "user_name": user_name, "email": email, "password": hex_dig, "avatar": avatar, "active": active, "group_id": group_id})
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.exception_member(response)
            if P.number == 200:
                return add(user_name, email, password, avatar, active, group_id)
            else: return P
        elif response.status_code == 403:
            A = {"number": 403, "response": {"text": response.text}}
            return error_handling.obj_dic(A)
        elif response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s

