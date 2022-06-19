import requests
from requests.exceptions import HTTPError
#from werkzeug.exceptions import HTTPException
from argparse import Namespace
from recording_spark_api import *
import __init__


# BEGIN Токенное.
def renew():
    print("SAS2")
    global short_token, live_token
    #print(short_token)
    if len(__init__.live_token) == 0 or __init__.live_token[0] == None or __init__.live_token[0] == "": ### ????????
        A = {"number": 1002, "response": {"text": "Токен не продлить!"}}
        s = obj_dic(A)
        return s
    #print(short_token)
    try:
        print("SSS")
        response = requests.get(f'{server[0]}renew/', timeout=(5, 3), headers={'live_token': __init__.live_token[0], "user_id": str(__init__.user_id[0])},)
        if response.status_code != 200:
            if response.status_code == 426:
                print(response.text)
                A = {"number": 1002, "response": {"text": response.text}}
                s = obj_dic(A)
                return s
            print("Бля")
            return exception_member(response)
    except Exception as e:
        return handle_exception(e)
    request_L = (response.text)
    SAS = json.loads(request_L)
    __init__.short_token.clear()
    __init__.short_token.append(SAS["short_token"])
    __init__.live_token.clear()
    __init__.live_token.append(SAS["live_token"])
    #short_token = SAS["short_token"]


    A = {"number": 200, "response": {"text": None}}
    s = obj_dic(A)
    return s
# END

# BEGIN Побочное.
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
# END



# BEGIN Обработка ошибок.
def handle_exception(e):
    if isinstance(e, requests.exceptions.ConnectTimeout):
        A = {"number": 524, "response": {"text": "Время ожидания ситекло."}}
        print( "Время ожидания ситекло.")
        return obj_dic(A)
    elif isinstance(e, requests.exceptions.ReadTimeout):
        A = {"number": 524, "response": {"text": "Время ожидания ситекло."}}
        print( "Время ожидания ситекло.")
        return obj_dic(A)
    elif isinstance(e, HTTPError):
        A = {"number": 520, "response": {"text": f"Произошла другая ошибка: {e}"}}
        print(f"Произошла другая ошибка: {e}")
        return obj_dic(A)
    elif isinstance(e, Exception):
        print(f"Произошла другая ошибка: {e}")
        A = {"number": 520, "response": {"text": f"Произошла другая ошибка: {e}"}}
        return obj_dic(A)
    else:
        print('Success!')

def exception_member(response):
    if response.status_code == 412:
        A = {"number": 412, "response": {"text": response.text}}
        print(response.text)
        return obj_dic(A)
    elif response.status_code == 500:
        A = {"number": 500, "response": {"text": "Ошибка на стороне сервера."}}
        print("Ошибка на стороне сервера.")
        return obj_dic(A)
    elif response.status_code == 401:
        A = {"number": 401, "response": {"text": "Необходима ваторизация."}}
        print("Необходима ваторизация.")
        return obj_dic(A)
    elif response.status_code == 426:
        return renew()
        #print("SAS")
    elif response.status_code == 404:
        A = {"number": 404, "response": {"text": "Сайт не найден."}}
        return obj_dic(A)
    else:
        A = {"number": response.status_code, "response": {"text": response.text}}
        return obj_dic(A)
# END
