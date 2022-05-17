from PySide2.QtUiTools import QUiLoader #pip3 install PySide2
from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2.QtCore import QFile, QIODevice, QTimer, QSize, Qt
from PySide2.QtWidgets import QFileDialog, QMessageBox
import math
from PySide2.QtCore import QStringListModel

import sys
import os
from PySide2.QtGui import QIcon, QPixmap, QPainter, QPalette, QBrush, QImage

import requests
put = os.path.dirname(os.path.realpath(__file__)) + "/"#Путь- (part-1)
R = 0
u_n = ""
remember = 1

backround = []
import recording_spark_api
import bd_module

server_user_and_list = []

themes = ""

server_id = 0


def SSS(A):
    """
    print(f"{put}content/themes/{themes}/{A}")
    con =  open(f"{put}content/themes/{themes}/{A}", "r")
    s = con.readlines()
    con.close()
    print(s)
    return s
    """
def rm_server(window_L):
    global server_user_and_list
    A = True
    if window_L.comboBox.count() != 0:
        msg = QMessageBox.question(window_L, "   !!!ВНИМАНИЕ!!!   ",
        "На этот сервепр уже завязоны пользователи. Если вы удолите сервер, то также удолятся пользователи.\nВы уверены ?\n", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)
        if msg == QMessageBox.Yes:
            server_id = window_L.comboBox_2.currentIndex()
            for user in server_user_and_list[server_id][1]:
                HG = user
                OG = server_user_and_list[server_id][0]
                if OG[4]:
                    server_url = f"https://{OG[2]}:{OG[3]}/"
                else:
                    server_url = f"http://{OG[2]}:{OG[3]}/"
                M = recording_spark_api.user.kill_session(HG[0], HG[4], server_url)
                if M.number == 200 or M.number == 404:
                    bd_module.rm(HG[0], OG[0])
                    window_L.comboBox.clear()
                    start(window_L)
                elif M.number != 404:
                    msg = QMessageBox.question(window_L, "   !!!ВНИМАНИЕ!!!   ",
                        "Не удолось закрыть сесию\nСервер всё ещё думает что вы не выходили из акаунта.\nВсё равно удолить сесию ?", QMessageBox.Yes |
                        QMessageBox.No, QMessageBox.No)
                    if msg == QMessageBox.Yes:
                        bd_module.rm(HG[0], OG[0])
                    else:
                        A = False
            if A == True:
                bd_module.rm_server(server_user_and_list[server_id][0][0])
            start(window_L)

    else:
        msg = QMessageBox.question(window_L, "   !!!ВНИМАНИЕ!!!   ",
            "Вы уверены ?\n", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if msg == QMessageBox.Yes:
            server_id = window_L.comboBox_2.currentIndex()
            bd_module.rm_server(server_user_and_list[server_id][0][0])
            start(window_L)

def rm_user(window_L):
    global server_user_and_list
    msg = QMessageBox.question(window_L, "   !!!ВНИМАНИЕ!!!   ",
        "Вы уверены ?\n", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)
    if msg == QMessageBox.Yes:

        server_id = window_L.comboBox_2.currentIndex()
        user_id = window_L.comboBox.currentIndex()
        #server_user_and_list[server_id][1][user_id][1]
        #user_id = bd_module.ls_user()
        #HG = bd_module.user_id_check(user_id[id][0], server_id)
        HG = server_user_and_list[server_id][1][user_id]
        OG = server_user_and_list[server_id][0]
        if OG[4]:
            server_url = f"https://{OG[2]}:{OG[3]}/"
        else:
            server_url = f"http://{OG[2]}:{OG[3]}/"
        M = recording_spark_api.user.kill_session(HG[0], HG[4], server_url)
        if M.number == 200 or M.number == 404:
            bd_module.rm(HG[0], OG[0])
            window_L.comboBox.clear()
            start(window_L)
        elif M.number != 404:
            msg = QMessageBox.question(window_L, "   !!!ВНИМАНИЕ!!!   ",
                "Не удолось закрыть сесию\nСервер всё ещё думает что вы не выходили из акаунта.\nВсё равно удолить сесию ?", QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No)
            if msg == QMessageBox.Yes:
                bd_module.rm(HG[0], OG[0])
                window_L.comboBox.clear()
                start(window_L)



def login(window_L):
    global R, u_n, remember, server_id
    server_list_target = server_user_and_list[window_L.comboBox_3.currentIndex()][0]
    if server_list_target[4]:
        ssl = "https://"
    else:
        ssl = "http://"
    server = f"{ssl}{server_list_target[2]}:{server_list_target[3]}/"




    print("SASAS")
    login_l = window_L.lineEdit.text()
    password = window_L.lineEdit_2.text()


    I = window_L.checkBox.isChecked()
    #print(int(I))

    recording_spark_api.server.clear()
    recording_spark_api.server.append(server)
    P = recording_spark_api.login(login_l, password, int(I))
    oloss = "background: rgb(0, 0, 0, 50%); color:  rgb(250, 250, 250, 100%);"
    if P.number == 412:
        window_L.label.setStyleSheet(oloss)
        #window_L.widget.show()
        window_L.label.setText("Не верный лигин или пароль!")

    elif P.number == 200:


        server_id = server_list_target[0]
        #window_L.label.setText("Успех!")

        #recording_spark_api.server.clear()
        #recording_spark_api.short_token.append(P.response.short_token)
        #recording_spark_api.live_token.clear()
        #recording_spark_api.short_token.append(P.response.live_token)
        #recording_spark_api.user_id.clear()
        #recording_spark_api.user_id.append(P.response.user_id)
        u_n = P.response.user_name
        recording_spark_api.route.clear()
        recording_spark_api.route.append(f"{put}/png/{server_id}/")
        if os.path.isfile(f"{put}/png/{server_id}/"):
            os.mkdir(f"{put}/png/{server_id}/")
        if I == 1:
            HG = bd_module.user_id_check(P.response.user_id, server_list_target[0])
            if (HG) != None:
                msg = QMessageBox.question(window_L, "   !!!ВНИМАНИЕ!!!   ",
                "Произошло совподение по логину из автовхода!\nЗаменить сушествуюшею сению на новую ?", QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No)

                if msg == QMessageBox.Yes:
                    bd_module.rm(P.response.user_id, server_list_target[0])
                    OG = bd_module.ls_server_id(HG[2])
                    if OG[4]:
                        ADA = f"https://{OG[2]}:{OG[3]}/"
                    else:
                        ADA = f"http://{OG[2]}:{OG[3]}/"
                    M = recording_spark_api.user.kill_session(HG[0], HG[1], ADA)
                    bd_module.add(P.response.user_id, P.response.user_name, server_list_target[0], login_l, P.response.live_token, P.response.short_token)
                    if M.number != 200:
                        msg = QMessageBox(window_L)
                        msg.setWindowTitle(f"ERROE # {M.number}")
                        msg.setText(f" \n    {M.response.text}    \n ")
                        msg.exec_()
                    R = 1
                    u_n = P.response.user_name
                    remember = I
                    if I == 1:
                        bd_module.target(P.response.user_id, server_list_target[0])
                    window_L.close()
                else:
                    #bd_module.add(P.response.user_id, f"{P.response.user_name} - D", f"http://{server}/", login_l, P.response.live_token, P.response.short_token)
                    R = 1
                    u_n = P.response.user_name
                    remember = 0
                    window_L.close()

                #msg.exec_()
            else:
                if I == 1:
                    bd_module.add(P.response.user_id, P.response.user_name, server_list_target[0], login_l, P.response.live_token, P.response.short_token)
                    bd_module.target(P.response.user_id, server_list_target[0])
                R = 1
                remember = I
                window_L.close()


            #msg = QMessageBox(window_L)
            #msg.setWindowTitle("   !!!ВНИМАНИЕ!!!   ")
            #msg.setText(" \n    Произошло совподение по логину из автовхода!\nЗакройте окно если НЕ хотите перезаписать данные!")





        #add(id, name, server, email, live_token, short_token, target)

        #X_Pars["short_token"] = P.response.short_token
        #X_Pars["live_token"] = P.response.live_token
        #X_Pars["user_id"] = P.response.user_id


        #with open(f"{put}sonf.json", "w") as write_file:
        #    json.dump(X_Pars,write_file)

        else:
            R = 1
            u_n = P.response.user_name
            remember = 0
            window_L.close()
    else:
        #window_L.widget.show()
        window_L.label.setStyleSheet(oloss)
        window_L.label.setText(f"Ошибка #{P.number}\n{P.response.text}")
def registration(window_L):
    palette = QPalette()
    img = QImage(backround[2])
    scaled = img.scaled(window_L.size(), Qt.KeepAspectRatioByExpanding, transformMode = Qt.SmoothTransformation)
    palette.setBrush(QPalette.Window, QBrush(scaled))
    window_L.setPalette(palette)

    window_L.stackedWidget.setCurrentIndex(2)
    window_L.label_14.setText("  ○ ○ ●  ")
    #A = put + "content/icon/SSS4.jpg"
    #window_L.setStyleSheet('.QWidget {border-image: url(' + A + ') 0 0 0 0 stretch stretch;} .QLabel{border-image: None;}')
def authorization(window_L):
    palette = QPalette()
    img = QImage(backround[0])
    scaled = img.scaled(window_L.size(), Qt.KeepAspectRatioByExpanding, transformMode = Qt.SmoothTransformation)
    palette.setBrush(QPalette.Window, QBrush(scaled))
    window_L.setPalette(palette)

    window_L.stackedWidget.setCurrentIndex(0)
    window_L.label_14.setText("  ● ○ ○  ")
    #A = put + "content/icon/SSS3.jpg"
    #window_L.setStyleSheet('.QWidget {border-image: url(' + A + ') 0 0 0 0 stretch stretch;} .QLabel{border-image: None;}')

def choice(window_L):
    palette = QPalette()
    img = QImage(backround[1])
    scaled = img.scaled(window_L.size(), Qt.KeepAspectRatioByExpanding, transformMode = Qt.SmoothTransformation)
    palette.setBrush(QPalette.Window, QBrush(scaled))
    window_L.setPalette(palette)

    window_L.stackedWidget.setCurrentIndex(1)
    window_L.label_14.setText("  ○ ● ○  ")
    #A = put + "content/icon/sky-lights-siyanie-kosmos.jpg"
    #window_L.setStyleSheet('.QWidget {border-image: url(' + A + ') 0 0 0 0 stretch stretch;} .QLabel{border-image: None;}' + LUPP)



def start(window_L):
    global server_user_and_list
    window_L.comboBox.clear()
    window_L.comboBox_2.clear()
    window_L.comboBox_3.clear()
    A = False
    server_user_and_list = []
    server_list = bd_module.ls_server()
    user_list = bd_module.ls()
    user_list_lon = []
    for server in server_list:
        for user in user_list:
            if user[2] == server[0]:
                user_list_lon.append(user)
        server_user_and_list.append([server,user_list_lon])
        user_list_lon = []
    print(server_user_and_list, "AAAAAAA")

    P = 0
    for server in server_user_and_list:
        window_L.comboBox_3.addItem(server[0][1])
        window_L.comboBox_2.addItem(server[0][1])
        print(server[0][2])
        for user in server[1]:
            print(user[6], 1)
            if user[6] == 1:
                print("AAAAAAAAAAAAAAAAAAA")
                window_L.comboBox_2.setCurrentIndex(P)
                window_L.comboBox_3.setCurrentIndex(P)
                Q = 0
                for user in server[1]:
                    window_L.comboBox.addItem(user[1])
                    if user[6] == 1:
                        window_L.comboBox.setCurrentIndex(Q)
                    Q = Q + 1
                choice(window_L)
                A = True
                break
        P = P + 1
    if A == False:
        if window_L.comboBox_2.count() == 0:
            window_L.pushButton_5.setEnabled(False)
            window_L.pushButton_4.setEnabled(False)
            window_L.pushButton_3.setEnabled(False)
            window_L.pushButton_15.setEnabled(False)
        else:
            for user in server_user_and_list[0][1]:
                window_L.comboBox.addItem(user[1])
            if window_L.comboBox.count() == 0:
                window_L.pushButton_5.setEnabled(False)
                window_L.pushButton_4.setEnabled(False)
            choice(window_L)
    window_L.pushButton.setEnabled(False)
    # [server[][][]]
    """
    global user_list, server_list, server_user_list
    server_user_list = []
    server_list = bd_module.ls_server()
    user_list = bd_module.ls()
    user_list_lon = []
    for server in server_list:
        for user in user_list:
            if user[2] == server[0]:
                user_list_lon.append(user)
        server_user_list.append(user_list_lon)
        user_list_lon = []
    #print(server_list)
    #print(user_list)
    for K in server_list:
        print(K[1])
        window_L.comboBox_3.addItem(K[1])
        window_L.comboBox_2.addItem(K[1])

    for K in user_list:
        if K[6] == 1:
            server_target = K[2]
    P = 0
    for K in server_list:
        if K[0] == server_target:
            window_L.comboBox_2.setCurrentIndex(P)
            window_L.comboBox_3.setCurrentIndex(P)
        P = P + 1

    if len(user_list) == 0:
        window_L.pushButton_5.setEnabled(False)
        window_L.pushButton_3.setEnabled(False)
        window_L.pushButton_4.setEnabled(False)
    else:
        window_L.pushButton_5.setEnabled(True)
        window_L.pushButton_3.setEnabled(True)
        window_L.pushButton_4.setEnabled(True)
        choice(window_L)
        #for ppp in server_user_list:
        #    if ppp
        #    server_target
        #server_user_list
        for K in user_list:
            window_L.comboBox.addItem(K[1])
        P = 0
        for K in user_list:
            if K[6] == 1:
                window_L.comboBox.setCurrentIndex(P)
            P = P + 1




    #window_L.comboBox_2.setCurrentIndex(K)
    #window_L.comboBox_3.setCurrentIndex(K)
    """

def login_lineEdit_triger(window_L):
    if (window_L.lineEdit_2.text() == None or window_L.lineEdit_2.text() == "") or (window_L.lineEdit.text() == None or window_L.lineEdit.text() == "") or window_L.comboBox_3.count() == 0:
        window_L.pushButton.setEnabled(False)
    else:
        window_L.pushButton.setEnabled(True)

def server_add(window_L):
    window_L.pushButton_13.setEnabled(False)
    window_L.stackedWidget.setCurrentIndex(3)
    window_L.label_14.setStyleSheet("background: rgb(0, 0, 0, 0%); color:  rgb(0, 0, 0, 0%);")

def lineEdit_triger(window_L):
    if window_L.lineEdit_3.text() == None or window_L.lineEdit_3.text() == "":
        window_L.pushButton_13.setEnabled(False)
        window_L.lineEdit_7.setPlaceholderText("")
    else:
        if window_L.checkBox_3.isChecked():
            window_L.lineEdit_7.setPlaceholderText(window_L.lineEdit_3.text() + " - SSL = ON")
        else:
            window_L.lineEdit_7.setPlaceholderText(window_L.lineEdit_3.text() + " - SSL = OFF")
        window_L.pushButton_13.setEnabled(True)



def server_add_a(window_L):
    global server_user_and_list
    ssl = window_L.checkBox_3.isChecked()
    if window_L.lineEdit_7.text() == "" or window_L.lineEdit_7.text() == None:
        if ssl:
            name = window_L.lineEdit_3.text() + " - SSL = ON"
        else:
            name = window_L.lineEdit_3.text() + " - SSL = OFF"
    else:
        name = window_L.lineEdit_7.text()
    adres = ""
    PO = True
    port = ""
    for NM in list(window_L.lineEdit_3.text()):
        if PO and NM != ":":
            adres = adres + NM
        elif NM != ":":
            port = port + NM
        else:
            PO = False


    server_id = bd_module.add_server(name, adres, port, ssl)
    authorization(window_L)
    server = bd_module.ls_server_id(server_id)
    print(server_id, "server_id")
    print(server, "server")

    server_user_and_list.append([server,[]])
    print(server_user_and_list)
    window_L.comboBox_3.addItem(server[1])
    window_L.comboBox_2.addItem(server[1])
    window_L.comboBox_3.setCurrentIndex(window_L.comboBox_3.count() - 1)
    window_L.pushButton_15.setEnabled(True)
    window_L.pushButton_3.setEnabled(True)




    #server_list.clear()
    #server_list = bd_module.ls_server()

def login_choice(window_L):
    server_index = window_L.comboBox_2.currentIndex()
    print(server_index)
    print(server_user_and_list[server_index], "SAS")

    user_id = window_L.comboBox.currentIndex()
    user = server_user_and_list[server_index][1][user_id]
    print(user[5])
    print(user[1])
    #user_id = bd_module.ls_user()
    print("SASAS")
    #token_l = bd_module.ls_user_target(id)
    recording_spark_api.short_token.clear()
    recording_spark_api.short_token.append(user[5])
    recording_spark_api.live_token.clear()
    recording_spark_api.live_token.append(user[4])
    recording_spark_api.user_id.clear()
    recording_spark_api.user_id.append(user[0])
    recording_spark_api.server.clear()
    OG = bd_module.ls_server_id(user[2])
    print(user[2])
    print(OG)
    if OG[4]:
        ADA = f"https://{OG[2]}:{OG[3]}/"
    else:
        ADA = f"http://{OG[2]}:{OG[3]}/"
    recording_spark_api.server.append(ADA)
    print(recording_spark_api.user_id)
    P = recording_spark_api.ls()
    oloss = "background: rgb(0, 0, 0, 50%); color:  rgb(250, 250, 250, 100%);"
    if P.number == 200:
        global R, u_n, server_id
        recording_spark_api.route.clear()
        recording_spark_api.route.append(f"{put}/png/{server_user_and_list[server_index][0][0]}/")
        if not os.path.isdir(f"{put}/png/{server_user_and_list[server_index][0][0]}/"):
            os.mkdir(f"{put}/png/{server_user_and_list[server_index][0][0]}/")
        bd_module.token_update(recording_spark_api.user_id[0], recording_spark_api.live_token[0], recording_spark_api.short_token[0], user[2])
        server_id = OG[0]
        R = 1
        u_n = user[1]
        bd_module.target(user[0], user[2])
        window_L.close()
    elif P.number == 1002:
        window_L.label_6.setStyleSheet(oloss)
        window_L.label_6.setText("Сесия устарела!")
    else:
        window_L.label_6.setStyleSheet(oloss)
        window_L.label_6.setText(f"Ошибка #{P.number}")

def server_choice (index, window_L):
    window_L.comboBox.clear()
    for user in server_user_and_list[index][1]:
        window_L.comboBox.addItem(user[1])
    print(window_L.comboBox.count())
    if window_L.comboBox.count() == 0:
        window_L.pushButton_5.setEnabled(False)
        window_L.pushButton_4.setEnabled(False)
    else:
        window_L.pushButton_5.setEnabled(True)
        window_L.pushButton_4.setEnabled(True)

def GUI(app):
    if os.path.exists(f"{put}content/themes/{themes}/background/login.jpg"):
        A = f"{put}content/themes/{themes}/background/login.jpg"
        backround.append(A)
    else:
        backround.append(None)
    if os.path.exists(f"{put}content/themes/{themes}/background/entrance.jpg"):
        B = f"{put}content/themes/{themes}/background/entrance.jpg"
        backround.append(B)
    else:
        backround.append(None)
    if os.path.exists(f"{put}content/themes/{themes}/background/registration.jpg"):
        C = f"{put}content/themes/{themes}/background/registration.jpg"
        backround.append(C)
    else:
        backround.append(None)




    #app = QApplication(sys.argv)

    ui_file_name = put + "content/ui/" + "login.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
        sys.exit(-1)
    loader = QUiLoader()
    window_L = loader.load(ui_file)
    ui_file.close()
    if not window_L:
        print(loader.errorString())
        sys.exit(-1)
    window_L.show()


    #window_L.widget.hide()

    #painter = QPainter(window_L)
    #pixmap = QPixmap(A)
    #painter.drawPixmap(window_L.rect(), pixmap)

    #palette = QPalette()
    #palette.setBrush(QPalette.Background, QBrush(QPixmap(A)))
    #window_L.setPalette(painter)
    #loll = "#MainWindow{border-image:url("+A+")}"
    #print(A)
    #window_L.setObjectName("MainWindow")
    #window_L.setStyleSheet(loll)


    window_L.setWindowTitle("R/K")
    #pal = window_L.palette()
    #pal.setBrush(QPalette.Normal, QPalette.Window, QBrush(QPixmap(B)))
    #window_L.setPalette(pal)


    palette = QPalette()
    img = QImage(backround[0])
    scaled = img.scaled(window_L.size(), Qt.KeepAspectRatioByExpanding, transformMode = Qt.SmoothTransformation)
    palette.setBrush(QPalette.Window, QBrush(scaled))
    window_L.setPalette(palette)



    oloss = "background: rgb(0, 0, 0, 0%); color:  rgb(0, 0, 0, 0%);"
    window_L.setWindowIcon(QIcon(f"{put}content/icon/2icon.png"))
    window_L.setStyleSheet(open(f"{put}content/themes/{themes}/login_all").read())
    window_L.comboBox.setStyleSheet(open(f"{put}content/themes/{themes}/QComboBox_all").read())
    window_L.comboBox_3.setStyleSheet(open(f"{put}content/themes/{themes}/QComboBox_all").read())
    window_L.label.setStyleSheet(oloss)
    window_L.label_6.setStyleSheet(oloss)
    window_L.label_10.setStyleSheet(oloss)
    #window_L.page.setStyleSheet(".QWidget{border-image:url(" + f"{A}" + ")}")
    #window_L.page_2.setStyleSheet(".QWidget{border-image:url(" + f"{B}" + ")}")
    #window_L.page_3.setStyleSheet(".QWidget{border-image:url(" + f"{C}" + ")}")
    #window_L.setStyleSheet(".QWidget{border-image:url(" + A + ")}")
    #window_L.setStyleSheet(".QWidget {border-image: url(" + A + ") 0 0 0 0 stretch stretch;} .QLabel{border-image: None;}")

    window_L.lineEdit_3.textChanged.connect(lambda:lineEdit_triger (window_L))
    window_L.checkBox_3.toggled.connect(lambda:lineEdit_triger (window_L))


    window_L.comboBox_2.activated.connect(lambda:server_choice (window_L.comboBox_2.currentIndex(),window_L))



    window_L.pushButton.clicked.connect(lambda:login (window_L))
    window_L.pushButton_2.clicked.connect(lambda:choice (window_L))
    window_L.pushButton_7.clicked.connect(lambda:registration (window_L))
    window_L.pushButton_8.clicked.connect(lambda:registration (window_L))
    window_L.pushButton_9.clicked.connect(lambda:authorization (window_L))
    window_L.pushButton_10.clicked.connect(lambda:authorization (window_L))
    window_L.pushButton_11.clicked.connect(lambda:choice (window_L))

    window_L.pushButton_4.clicked.connect(lambda:rm_user (window_L))
    window_L.pushButton_13.clicked.connect(lambda:server_add_a (window_L))

    window_L.pushButton_3.clicked.connect(lambda:rm_server(window_L))
    window_L.pushButton_15.clicked.connect(lambda:rm_server(window_L))

    #window_L..clicked.connect(lambda:registration (window_L))
    #window_L..clicked.connect(lambda:registration (window_L))
    window_L.pushButton_3.setIcon(QIcon(f"{put}content/icon/rm.png"))
    window_L.pushButton_15.setIcon(QIcon(f"{put}content/icon/rm.png"))
    window_L.pushButton_4.setIcon(QIcon(f"{put}content/icon/rm.png"))
    window_L.pushButton_12.setIcon(QIcon(f"{put}content/icon/add.png"))
    window_L.pushButton_12.setStyleSheet(open(f"{put}content/themes/{themes}/login_QPushButton_rm").read())
    window_L.pushButton_15.setStyleSheet(open(f"{put}content/themes/{themes}/login_QPushButton_rm").read())
    QTimer.singleShot(100, lambda:start(window_L))


    window_L.pushButton_5.clicked.connect(lambda:login_choice (window_L))
    window_L.pushButton_12.clicked.connect(lambda:server_add (window_L))



    window_L.pushButton_14.clicked.connect(lambda:authorization (window_L))


    window_L.lineEdit.textChanged.connect(lambda:login_lineEdit_triger (window_L))
    window_L.lineEdit_2.textChanged.connect(lambda:login_lineEdit_triger (window_L))

    #window_L.pushButton_7.setIcon(QIcon(f"{put}content/icon/registration.png"))
    #window_L.pushButton_7.setIcon(QIcon.pixmap(64,64))
    #if X_Pars["server"] != "":
        #window_L.lineEdit_3.setText(X_Pars["server"])
    #if X_Pars["email"] != "":
        #window_L.lineEdit.setText(X_Pars["email"])
    #sys.exit(app.exec_())
    app.exec_()

def open_l(app, themes_A):
    global R, u_n, remember, themes, server_id
    themes = themes_A
    remember = 1
    R = 0
    GUI(app)
    print(u_n, "u_nu_nu_nu_nu_nu_nu_nu_nu_n")
    return R, u_n, remember, server_id

