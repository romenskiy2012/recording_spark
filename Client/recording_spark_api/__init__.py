server = ["http://127.0.0.1:5000/"]
short_token = []
live_token = []
user_id = []
Ln = []
route = []

import os, sys

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT))

import hashlib
import requests
import json
#from .item import *
#from .user import *
import item
import user
from error_handling import *
import error_handling

import socket

#from .mein import *
#import mein


#import json
#with open(f"{put}sonf.json", "r") as read_file:
#    X_Pars = json.load(read_file)


def SS(A):
    #global short_token
    #short_token = A
    Ln.append(A)
    print(Ln)
    return Ln


def login(email, password, remember):
    print(server[0])
    #global short_token, live_token
    a = f"{password}".encode('utf-8')
    hash_object = hashlib.sha512(a)
    hex_dig = hash_object.hexdigest()
    #print(hex_dig)
    try:
        response = requests.get(f'{server[0]}login/', timeout=(5, 3),  headers={'email': email, 'password': hex_dig, 'remember': str(remember), "ps_info_name": socket.gethostname()},)
        if response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    request_L = (response.text)
    SAS = json.loads(request_L)
    print(SAS)
    short_token.clear()
    short_token.append(SAS["short_token"])
    live_token.clear()
    live_token.append(SAS["live_token"])
    user_id.clear()
    user_id.append(SAS["user_id"])


    A = {"number": 200, "response": {"text": None, "short_token": short_token[0], "live_token": live_token[0], "user_id": user_id[0], "user_name": SAS["user_name"]}}
    #s = bunchify(A)
    s = error_handling.obj_dic(A)
    return s


def ls():
    print("SAS1")
    try:
        response = requests.get(f'{server[0]}ls/', timeout=(5, 3), headers={'short_token': short_token[0]},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.renew()
            if P.number == 200:
                return ls()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    request_L = (response.text)
    matrix = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "matrix": matrix["ls"]}}
    s = error_handling.obj_dic(A)
    return s

def permission(u_id):
    try:
        response = requests.get(f'{server[0]}permission/', timeout=(5, 3), headers={'short_token': short_token[0], "user_id": u_id},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.renew()
            if P.number == 200:
                return permission(u_id)
            else: return P
        if response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    request_L = (response.text)
    A = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "permission": A["permission"], "ownership_over_group": A["ownership_over_group"]}}
    s = error_handling.obj_dic(A)
    return s


def ls_group():
    print("SAS1")
    try:
        response = requests.get(f'{server[0]}ls_group/', timeout=(5, 3), headers={'short_token': short_token[0]},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.renew()
            if P.number == 200:
                return ls_group()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    request_L = (response.text)
    matrix = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "matrix": matrix["matrix"]}}
    s = error_handling.obj_dic(A)
    return s


def ls_sessions():
    print("SAS1")
    try:
        response = requests.get(f'{server[0]}ls_sessions/', timeout=(5, 3), headers={'short_token': short_token[0]},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.renew()
            if P.number == 200:
                return ls_sessions()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    request_L = (response.text)
    matrix = json.loads(request_L)
    A = {"number": 200, "response": {"text": None, "matrix": matrix["matrix"]}}
    s = error_handling.obj_dic(A)
    return s

def full_closure_session():
    print("full_closure_session")
    try:
        response = requests.get(f'{server[0]}full_closure_session/', timeout=(5, 3), headers={'short_token': short_token[0]},)
        print(f"SAS - {response.status_code}")
        if response.status_code == 426:
            P = error_handling.renew()
            if P.number == 200:
                return full_closure_session()
            else: return P
        if response.status_code != 200:
            print("Бля")
            return error_handling.exception_member(response)
    except Exception as e:
        return error_handling.handle_exception(e)
    A = {"number": 200, "response": {"text": None}}
    s = error_handling.obj_dic(A)
    return s

