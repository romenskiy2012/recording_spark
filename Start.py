#!/usr/bin/python3

import os

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename

from time import strftime, localtime, sleep #Для (Time)
import json
import hashlib
import logging

import bd_module
from datetime import date

put = os.path.dirname(os.path.realpath(__file__)) + "/"#Путь- (part-1)
with open(f"{put}settings.json", "r") as read_file:
    settings = json.load(read_file)
import logging
if settings["log_type"] == "INFO":
    level=logging.INFO
elif settings["log_type"] == "DEBUG":
    level=logging.DEBUG
elif settings["log_type"] == "ERROR":
    level=logging.ERROR
else:
    print('Тип лога указан не верно, авто "INFO"\nВареанты: "INFO", "DEBUG", ERROR')
    level=logging.INFO


logging.basicConfig(filename=settings["log_file"], level=level)




def authentication(token):
    uid = bd_module.check_user_short_token(token)
    #return uid, gid
    return uid

def mi_ip(request):
    try:
        return request.headers['x-forwarded-for']
    except:
        return request.remote_addr



UPLOAD_FOLDER = put + 'png/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
print(UPLOAD_FOLDER)
print("SAS")

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)



@app.route('/login/', methods=['GET', 'POST'])
def login():
    email = request.headers['email']
    password = request.headers['password']
    remember = request.headers['remember']
    ps_info_name = request.headers['ps_info_name']
    uid ,user_name, active = bd_module.check_user(email, password)
    if uid == None:
        logging.info(f"Авторизаии под пользователям {email} !!!ОТКАЗ!!!")
        return "login not found", 412
    elif active == 0:
        logging.info(f"Авторизаии под пользователям {email} !!!ОТКЛЮЧИНА!!!")
        return "Учётная запесь отключина!", 423
    else:
        if remember == "1":

            short_token, live_token = bd_module.add_live_token(uid, ps_info_name, mi_ip(request), date.today(),30*24*60*60)
            #short_token = bd_module.add_short_token(uid)
            #live_token = bd_module.add_live_token(uid)
        else:
            short_token, live_token = bd_module.add_live_token(uid, ps_info_name, mi_ip(request), date.today(),12*60*60)
            #short_token = bd_module.add_short_token(uid)
            #live_token = None
        print(short_token, " - " ,live_token)
        logging.info(f"Авторизаии под пользователям {email} !УСПЕХ!")
        return json.dumps({"short_token": short_token, "live_token": live_token, "user_id": uid, "user_name": user_name}, separators=(',', ':'))


@app.route('/ls/', methods=['GET', 'POST'])
def ls():
    print("ls")
    print(request.headers['short_token'])
    uid = authentication(request.headers['short_token'])
    print(uid)
    if uid == None:
        print("/ls/' - 403")
        return "403", 426
    return json.dumps({"ls": bd_module.ls_item(uid)}, separators=(',', ':'))


@app.route('/item_add/', methods=['GET', 'POST'])
def item_add():
    print("item_add")
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"ls - Отказ по токену! IP - {mi_ip(request)}")
        print("/ls/' - 403")
        return "403", 426
    print(request)
    content = request.json
    print(content)
    item_name = content['item_name']
    status = content['status']
    user_id_1 = content['user_id_1']
    user_id_2 = content['user_id_2']
    comments = content['comments']
    inventory_id = content['inventory_id']
    id = bd_module.add_item(uid, user_id_1, user_id_2, item_name, status, None, comments, inventory_id)
    if id != 0:
        logging.info(f"Пользователь {uid} создал предмет {id}")
        return json.dumps({"item_id": id}, separators=(',', ':'))
    else:
        logging.info(f"Пользователю {uid} отказано в создании предмета")
        return "Отказ", 403

@app.route('/item_edit/', methods=['GET', 'POST'])
def item_edit():
    print("item_edit")
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"item_edit - Отказ по токену! IP - {mi_ip(request)}")
        print("/item_edit/' - 403")
        return "403", 426
    content = request.json
    item_id = content['item_id']
    item_name = content['item_name']
    status = content['status']
    user_id_1 = content['user_id_1']
    user_id_2 = content['user_id_2']
    comments = content['comments']
    inventory_id = content['inventory_id']
    id = bd_module.item_edit(uid, item_id, user_id_1, user_id_2, item_name, status, None, comments, inventory_id)
    if id == 1:
        logging.info(f"Пользователь {uid} изменил предмета {item_id}")
        return "OK", 200
    else:
        logging.info(f"Пользователю {uid} отказано в редактировании предмета {item_id}")
        return "Отказ", 403

@app.route('/item_rm/', methods=['GET', 'POST'])
def item_rm():
    print("item_rm")
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"item_rm - Отказ по токену! IP - {mi_ip(request)}")
        print("/item_rm/' - 403")
        return "403", 426
    content = request.json
    item_id = content['item_id']
    id = bd_module.item_rm(uid, item_id)
    if id == 1:
        if os.path.isfile(f"{put}png/item/{item_id}"):
            os.remove(f"{put}png/item/{item_id}")
            logging.info(f"Иконка предмета {item_id} удалена")
        logging.info(f"Пользователь {uid} удолил предмета {item_id}")
        return "OK", 200
    else:
        logging.info(f"Пользователю {uid} отказанно в удоление предмета {item_id}")
        return "Отказ", 403





@app.route('/user_ls/', methods=['GET', 'POST'])
def user_ls():
    print("user_ls")
    print(request.headers['short_token'])
    uid = authentication(request.headers['short_token'])
    print(uid)
    if uid == None:
        logging.debug(f"user_ls - Отказ по токену! IP - {mi_ip(request)}")
        print("/user_ls/' - 403")
        return "403", 426
    return json.dumps({"ls": bd_module.ls_user(uid)}, separators=(',', ':'))

@app.route('/user_info/', methods=['GET', 'POST'])
def user_info():
    uid = authentication(request.headers['short_token'])
    user_id = (request.headers['user_id'])
    #uid = 455435
    if uid == None:
        logging.debug(f"user_info - Отказ по токену! IP - {mi_ip(request)}")
        print("/user_info/' - 403")
        return "403", 426
    user_info = bd_module.user_info(uid, user_id)
    print(user_info)
    if user_info != None:
    #########################
        directory = app.config['UPLOAD_FOLDER']
        # user_info
        print(user_info) ################################################################################################################
        student  = {
            "user_name" : user_info[0],
            "email" : user_info[1],
            "avatar" : user_info[2],
            "active": user_info[3],
            "group_id": user_info[4],
            "permission": user_info[5],
        }
        b = json.dumps(student)

        return b
    else:
        return "Отказ в доступе!", 403



@app.route('/renew/', methods=['GET', 'POST'])
def renew():
    print("renew")
    short_token, live_token = bd_module.update_short_token(request.headers['user_id'], request.headers['live_token'])
    #short_token = bd_module.check_user_live_token(request.headers['live_token'])
    if short_token == None:
        logging.debug(f"renew - Отказ по токену! IP - {mi_ip(request)}")
        print("/renew/' - 403")
        return "Токен не верен", 426
    return json.dumps({"short_token": short_token, "live_token": live_token}, separators=(',', ':'))


"""
@app.route('/exit/', methods=['GET', 'POST']) # ??? Что это ???
def exit():
    print("exit")
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"exit - Отказ по токену!")
        print("/exit/' - 403")
        return "403", 426
    return json.dumps({"short_token": short_token}, separators=(',', ':'))
"""



@app.route('/kill_session/', methods=['GET', 'POST'])
def kill_session():
    print("kill_session")
    user_id = request.headers['user_id']
    live_token = request.headers['live_token']
    print(live_token)
    A = bd_module.rm_live_token(user_id, live_token)
    if A:
        return "OK"
    else:
        return "404", 404

@app.route('/ls_sessions/', methods=['GET', 'POST'])
def ls_sessions(): # !!! МОГУТ БЫТЬ ПРОБЛЕМЫ !!!
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"ls_sessions - Отказ по токену! IP - {mi_ip(request)}")
        print("/ls_sessions/' - 426")
        return "426", 426
    A = bd_module.ls_sessions(uid)
    return json.dumps({"matrix": A}, separators=(',', ':'))

@app.route('/exiting_session/', methods=['GET', 'POST'])
def exiting_session(): # !!! МОГУТ БЫТЬ ПРОБЛЕМЫ !!!
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"exiting_session - Отказ по токену! IP - {mi_ip(request)}")
        print("/exiting_session/' - 426")
        return "426", 426
    position = request.headers['position']
    A = bd_module.rm_live_token_position(uid, position)
    return "OK"

@app.route('/full_closure_session/', methods=['GET', 'POST'])
def full_closure_session(): # !!! МОГУТ БЫТЬ ПРОБЛЕМЫ !!!
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"full_closure_session - Отказ по токену! IP - {mi_ip(request)}")
        print("/full_closure_session/' - 426")
        return "426", 426
    A = bd_module.full_sessions_kill(uid)
    return "OK"

@app.route('/user_add/', methods=['GET', 'POST'])
def user_add():
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"user_add - Отказ по токену! IP - {mi_ip(request)}")
        print("/user_add/' - 426")
        return "426", 426
    content = request.json
    user_name = content['user_name']
    email = content['email']
    password = content['password']
    avatar = content['avatar']
    active = content['active']
    group_id = content['group_id']
    A = bd_module.user_add(uid, user_name, email, password, avatar, active, group_id)
    if A == None:
        return "Отказ в доступе!", 403
    return json.dumps({"user_id": A}, separators=(',', ':'))



@app.route('/user_edit/', methods=['GET', 'POST'])
def user_edit():
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"user_edit - Отказ по токену! IP - {mi_ip(request)}")
        print("/user_edit/' - 426")
        return "426", 426
    content = request.json
    user_id = content['user_id']
    user_name = content['user_name']
    email = content['email']
    password = content['password']
    avatar = content['avatar']
    active = content['active']
    group_id = content['group_id']

    A = bd_module.user_edit(uid, user_id, user_name, email, password, avatar, active, group_id)

    if A == 0:
        return "Отказ в доступе!", 403
    return "OK"

@app.route('/ls_group/', methods=['GET', 'POST'])
def ls_group():
    uid = authentication(request.headers['short_token'])
    if uid == None:
        logging.debug(f"ls_group - Отказ по токену! IP - {mi_ip(request)}")
        print("/ls_group/' - 426")
        return "426", 426
    A = bd_module.ls_group(uid)
    return json.dumps({"matrix": A}, separators=(',', ':'))

"""
@app.route('/permission/', methods=['GET', 'POST'])
def permission():
    print("permission")
    print(request.headers['short_token'])
    uid = authentication(request.headers['short_token'])
    print(uid)
    if uid == None:
        print("/permission/' - 426")
        return "426", 426
    user_id = request.headers["user_id"]
    A = permission(uid,user_id)
    return json.dumps({"ls": bd_module.ls_user(uid)}, separators=(',', ':'))
"""

@app.route('/', methods=['GET', 'POST'])
def lol():
    #return request.remote_addr
    #return request.headers['x-forwarded-for']
    return mi_ip(request)

@app.route('/SAS/', methods=['GET', 'POST'])
def ASA():
    content = request.json
    print(content)

    return "SAS"




@app.route('/rm_item_icon/', methods=['GET', 'POST'])
def rm_item_icon():
    uid = authentication(request.headers['short_token'])
    #uid = 1
    item_id = request.headers['item_id']
    if uid == None:
        logging.debug(f"rm_item_icon - Отказ по токену! IP - {mi_ip(request)}")
        print("/rm_item_icon/' - 403")
        return "403", 426
    a = bd_module.item_edit(uid, item_id, None, None, None, None, '-1', None, None)
    if a == 1:
        if os.path.isfile(f"{put}png/item/{item_id}"):
            os.remove(f"{put}png/item/{item_id}")

        return "OK"
    return "Отказ в доступе!", 403


@app.route('/add_item_icon/', methods=['GET', 'POST'])
def add_item_icon():
    uid = authentication(request.headers['short_token'])
    #uid = 1
    item_id = request.headers['item_id']
    if uid == None:
        logging.debug(f"add_item_icon - Отказ по токену! IP - {mi_ip(request)}")
        print("/add_item_icon/' - 403")
        return "403", 426
    if 'file' in request.files:
        if bd_module.item_w_test(uid,item_id) == 1:
            file = request.files['file']
            print(file)
            # безопасно извлекаем оригинальное имя файла
            filename = secure_filename(file.filename)
            directory = app.config['UPLOAD_FOLDER'] + "item"
            file.save(os.path.join(directory, item_id))
            hash = hashlib.md5(open(f"{UPLOAD_FOLDER}item/{item_id}",'rb').read()).hexdigest()
            bd_module.item_edit(uid, item_id, None, None, None, None, hash, None, None)


            return f"{hash}"
        return "Отказ в доступе!", 403
    return "Файла нет"
    """
    if request.method == 'POST':
        file = request.files['file']
        #if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))
    return "OF"
    """

@app.route('/ls_item_icon/', methods=['GET', 'POST'])
def ls_item_icon():
    print("item_icon")
    item_id = request.headers['item_id']

    uid = authentication(request.headers['short_token'])
    #uid = 1
    print(uid)
    if uid == None:
        logging.debug(f"ls_item_icon - Отказ по токену! IP - {mi_ip(request)}")
        print("/ls_item_icon/' - 403")
        return "403", 426
    item_info = bd_module.item_info(uid,item_id)
    if item_info != None:
        if item_info[5] != None:
            directory = app.config['UPLOAD_FOLDER']
            return send_from_directory(directory=directory+"item", path=str(item_id))
        return "Нет изображения", 404
    return "Нет такого предмета", 404


@app.route('/ls_avatar_icon/', methods=['GET', 'POST'])
def ls_avatar_icon():
    uid = authentication(request.headers['short_token'])
    url = request.headers['uid']
    #uid = 455435
    if uid == None:
        logging.debug(f"avatar - Отказ по токену! IP - {mi_ip(request)}")
        print("/avatar/' - 403")
        return "403", 426
    url = bd_module.avatar_png(uid)
    if url != None:
        if int(url) == uid:
            directory = app.config['UPLOAD_FOLDER']
            return send_from_directory(directory=directory+"user", path=uid)
        ### SAS
        directory = app.config['UPLOAD_FOLDER']
        return send_from_directory(directory=directory+"user", path=url)
    return None


if __name__ == "__main__":
    app.run(host=settings["host"], port=settings["port"])
