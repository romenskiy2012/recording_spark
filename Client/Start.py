#!/usr/bin/python3
from PySide2.QtUiTools import QUiLoader #pip3 install PySide2
from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2.QtCore import QFile, QIODevice
from PySide2.QtWidgets import QFileDialog
import math
from PySide2.QtCore import QStringListModel
import sys
import os
from PySide2.QtGui import QIcon, QPixmap
import requests
put = os.path.dirname(os.path.realpath(__file__)) + "/"#Путь- (part-1)
import recording_spark_api
import login
import GUI_main

import json




from PySide2.QtUiTools import QUiLoader #pip3 install PySide2
from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2.QtCore import QFile, QIODevice
from PySide2.QtWidgets import QFileDialog
import math
from PySide2.QtCore import QStringListModel
import sys
import os
from PySide2.QtGui import QIcon, QPixmap
import requests
app = QApplication(sys.argv)



import bd_module
themes = "heavenly_bliss"

#with open(f"{put}content/json/user.json", "r") as read_file:
    #X_Pars = json.load(read_file)

#bd_module.token_update(1, "sAS", "sos", 14)

#print(X_Pars)

if not os.path.isdir(put + "png"):
    os.mkdir(put + "png")

user_name = ""
remember = 1
server_id = 0
A = True
while A == True:
    R, user_name, remember, server_id = login.open_l(app, themes)
    print(R, user_name, remember, server_id, "server_id")
    if R == 1:
        R = GUI_main.open_l(app, user_name, themes)
        if remember == 0:
            KMK = recording_spark_api.user.kill_session(recording_spark_api.user_id[0] ,recording_spark_api.live_token[0], recording_spark_api.server[0])
            print(KMK.number)
        else:
            bd_module.token_update(recording_spark_api.user_id[0], recording_spark_api.live_token[0], recording_spark_api.short_token[0], server_id)
            print("ОК")
        if R == 0:
            A = False

    else:
        A = False


#R = 0
#A = True
#while A == True:


    """
    if X_Pars["short_token"] != None and X_Pars["short_token"] != "" and X_Pars["server"] != None and X_Pars["server"] != "":
        print("XXXXXX")
        recording_spark_api.short_token.clear()
        recording_spark_api.short_token.append(X_Pars["short_token"])
        recording_spark_api.live_token.clear()
        recording_spark_api.live_token.append(X_Pars["live_token"])
        recording_spark_api.server.clear()
        recording_spark_api.server.append(f'http://{X_Pars["server"]}/')
        recording_spark_api.user_id.clear()
        recording_spark_api.user_id.append(X_Pars["user_id"])

        R = GUI_main.open_l(app)
        print(R)
        print("LOL")
        if R == 1002:
            X_Pars["short_token"] = None
            X_Pars["live_token"] = None
            with open(f"{put}sonf.json", "w") as write_file:
                json.dump(X_Pars,write_file)
            R = login.open_l(app)
            if R == 0:
                print("SASSS")
                A = False
        if R == 0:
            print("exit")
            A = False



    else:
        R = login.open_l(app)
        if R == 0:
            print("SASSS")
            A = False
        #print(f"AAASAS = {login.open_l()}")
    """

#    R = login.open_l(app)
#    if R == 0:
#        print("SASSS")
#        A = False
#    elif R == 1:
#        print("SASSS")


#X_Pars["short_token"] = recording_spark_api.short_token[0]
#X_Pars["live_token"] = recording_spark_api.live_token[0]
#with open(f"{put}content/json/user.json", "w") as write_file:
#        json.dump(X_Pars,write_file)

if len(recording_spark_api.user_id) == 0 or len(recording_spark_api.live_token) == 0 or len(recording_spark_api.short_token) == 0 or remember == 0:
    print("NOT token_update")
else:
    print("token_update")
    bd_module.token_update(recording_spark_api.user_id[0], recording_spark_api.live_token[0], recording_spark_api.short_token[0], server_id)



