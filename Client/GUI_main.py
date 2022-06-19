from PySide2.QtUiTools import QUiLoader #pip3 install PySide2
from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2.QtCore import QFile, QIODevice, QTimer, QRect, Qt
from PySide2.QtWidgets import QFileDialog, QTableWidget, QTableWidgetSelectionRange, QHeaderView, QMainWindow, QMessageBox, QLabel
import math
from PySide2.QtCore import QStringListModel
import sys
import os
from PySide2.QtGui import QIcon, QPixmap
import requests
import hashlib

from time import strftime, localtime, sleep #Для (Time)

from PySide2 import QtGui

import threading
event = threading.Event()

put = os.path.dirname(os.path.realpath(__file__)) + "/"#Путь- (part-1)
R = 0
matrix = []
matrix_u = []
target = 0
target_u = 0
column = [1,1,1,1,1,0,0]
column_u = [1,1,1,1,1,0,0]
changeling_status = 0
themes = ""
import recording_spark_api
import GUI_item, GUI_user, settings

A_ls_group = []
A_user_ls = []

columns = ['ID','Предмет','Статус','От кого','К кому','Коментарий','Нивентарный ID']
columns_u = ['ID','Имя','Почта','Аватарка','Работает ?','Група', 'Права']
columns_u_2 = []
columns_2 =[]


def INFO(A, B):
    #window.setGeometry(300, 300, 300, 220)
    #window.setWindowTitle('Icon')
    #window.setWindowIcon(QIcon('web.png'))
    # win.setFixedSize(200, 50)
    #window.show()

    msg = QMessageBox(window)
    msg.setWindowTitle(f"ERROE {A}")
    msg.setText(f" \n    {B}    \n ")
    #msg.setTextFormat(window.TextCharFormat.setFontWeight(20))

    #msg.setIcon(QMessageBox.Critical)
    #msg.label.move(180,40)
    #msg.setText.setFixedSize(50, 10)
    #msg.P.setGeometry(QtCore.QRect(70, 80, 100, 100))


    #my_label = QLabel()
    #my_label.setText('My Label')
    #my_label.setFixedSize(500, 100)

    #msg.CreatorL = QLabel("Created By:", msg)
    #msg.CreatorL.setGeometry(QRect(70, 80, 100, 100)) #(x, y, width, height)

    msg.exec_()

    #msg.setFixedSize(400, 5000)

def paint():
    if changeling_status == 0:
        columns_2.clear()
        a = 0
        for p in column:
            if p:
                columns_2.append(columns[a])
            a = a + 1
        ls_list = matrix
        window.tableWidget.setColumnCount(len(columns_2))
        window.tableWidget.setHorizontalHeaderLabels(columns_2)
        A_ls = A_user_ls
        column_T = column
    else:
        columns_u_2.clear()
        a = 0
        for p in column_u:
            if p:
                columns_u_2.append(columns_u[a])
            a = a + 1
        ls_list = matrix_u

        window.tableWidget.setColumnCount(len(columns_u_2))
        window.tableWidget.setHorizontalHeaderLabels(columns_u_2)
        A_ls = A_ls_group
        column_T = column_u
        print(f"A_ls_group - {A_ls_group}")
        print(f"column_T - {column_T}")

    if window.comboBox.currentIndex()-1 == -1:
        window.tableWidget.setRowCount(len(ls_list))
        filter_ls = ls_list
    else:
        saq = 0
        filter_ls = []
        for A in ls_list:
            if (changeling_status == 0 and (A_ls[window.comboBox.currentIndex()-1][0] == A[3] or A_ls[window.comboBox.currentIndex()-1][0] == A[5])) or (changeling_status == 1 and (A_ls[window.comboBox.currentIndex()-1][0] == A[5])):
                filter_ls.append(A)
                saq = saq + 1
        window.tableWidget.setRowCount(saq)
    #window.tableWidget.setColumnCount(len(ls_list[0])-3)


    a = 0
    b = 0
    q = 0
    q_2 = 0
    #print(f"{window.comboBox.currentIndex()-1} - {A_user_ls[window.comboBox.currentIndex()-1][0]}")
    for A in filter_ls:
        #print(f"{A[3]} - {A[5]}")
        for L in A:
            if (changeling_status == 0 and not (b == 5 or b == 3 or b == 7)) or (changeling_status == 1 and not (b == 5)):
                #print(b)
                if column_T[q_2]:
                    #print(f"{column_T[q]} - {L}")
                    window.tableWidget.setItem(a,q, QTableWidgetItem(str(L)))
                    q = q + 1
                q_2 = q_2 + 1
            b = b + 1
        a = a + 1
        b = 0
        q = 0
        q_2 = 0
def paint_u():
    paint()
"""
def paint_u(): # Рисуем с верху в низ с лево на право. !!! НЕТ !!!
    columns_u_2.clear()

    #print((window.tableWidget.rowCount()))

    #window.tableWidget.removeRow()
    #print(column_u)
    a = 0
    for p in column_u:
        if p:
            columns_u_2.append(columns_u[a])
        a = a + 1
    ls_list = matrix_u
    #print(ls_list)
    #print(len(ls_list))
    #print(len(ls_list[1]))
    window.tableWidget.setRowCount(len(ls_list))
    #window.tableWidget.setColumnCount(len(ls_list[0])-3)
    window.tableWidget.setColumnCount(len(columns_u_2))
    window.tableWidget.setHorizontalHeaderLabels(columns_u_2)
    a = 0
    b = 0
    q = 0
    q_2 = 0
    #print(f"{window.comboBox.currentIndex()} - 0")
    for A in ls_list:
        if (A_ls_group[window.comboBox.currentIndex()][0] == A[3] or A_ls_group[window.comboBox.currentIndex()][0] == A[5]) or window.comboBox.currentIndex() == 0:
            for L in A:
                if not (b == 5):
                    #print(b)
                    if column_u[q_2]:
                        #print(f"{column[q]} - {L}")
                        window.tableWidget.setItem(a,q, QTableWidgetItem(str(L)))
                        #window.tableWidget.setCellWidget(0,1,comBox)
                        q = q + 1
                    q_2 = q_2 + 1
                b = b + 1
            a = a + 1
            b = 0
            q = 0
            q_2 = 0


def paint(): # Рисуем с верху в низ с лево на право. !!! НЕТ !!!
    columns_2.clear()

    #print((window.tableWidget.rowCount()))

    #window.tableWidget.removeRow()
    a = 0
    for p in column:
        if p:
            columns_2.append(columns[a])
        a = a + 1
    ls_list = matrix
    #print(len(ls_list))
    #print(len(ls_list[1]))
    if window.comboBox.currentIndex()-1 == -1:
        window.tableWidget.setRowCount(len(ls_list))
    else:
        saq = 0
        for A in ls_list:
            if (A_user_ls[window.comboBox.currentIndex()-1][0] == A[3] or A_user_ls[window.comboBox.currentIndex()-1][0] == A[5]):
                saq = saq + 1
        window.tableWidget.setRowCount(saq)
    #window.tableWidget.setColumnCount(len(ls_list[0])-3)
    window.tableWidget.setColumnCount(len(columns_2))
    window.tableWidget.setHorizontalHeaderLabels(columns_2)
    a = 0
    b = 0
    q = 0
    q_2 = 0
    print(f"{window.comboBox.currentIndex()-1} - {A_user_ls[window.comboBox.currentIndex()-1][0]}")
    for A in ls_list:
        if (A_user_ls[window.comboBox.currentIndex()-1][0] == A[3] or A_user_ls[window.comboBox.currentIndex()-1][0] == A[5]) or window.comboBox.currentIndex()-1 == -1:
            print(f"{A[3]} - {A[5]}")
            for L in A:
                if not (b == 3 or b == 5 or b == 7):
                    #print(b)
                    if column[q_2]:
                        #print(f"{column[q]} - {L}")
                        window.tableWidget.setItem(a,q, QTableWidgetItem(str(L)))
                        q = q + 1
                    q_2 = q_2 + 1
                b = b + 1
            a = a + 1
            b = 0
            q = 0
            q_2 = 0
"""
def ls_u():
    global matrix_u
    L = recording_spark_api.user.ls()
    group = recording_spark_api.ls_group()
    print(recording_spark_api.server)
    print(L.number)
    if L.number == 403:
        print("БЛЯ")
        return  False
    elif L.number == 200:
        if group.number == 200:
            global A_ls_group
            print(group.response.matrix)
            A_ls_group = group.response.matrix
            window.comboBox.clear()
            window.comboBox.addItem("Все")
            for nbn in group.response.matrix:
                window.comboBox.addItem(nbn[1])
            window.comboBox.setCurrentIndex(0)
        print(L.response.matrix)
        matrix_u = L.response.matrix
        print(matrix_u)
        #print(SAS)
        paint_u()
        return True
    elif L.number == 1002:
        global R
        print(L.response.text)
        R = 1002
        window.close()

    else:
        print("БЛЯ")
        return False


def ls():
    global matrix
    L = recording_spark_api.ls()
    user = recording_spark_api.user.ls()
    print(recording_spark_api.server)
    print(L.number)
    if L.number == 403:
        print("БЛЯ")
        return  False
    elif L.number == 200:
        if user.number == 200:
            global A_user_ls
            print(user.response.matrix)
            A_user_ls = user.response.matrix
            window.comboBox.clear()
            window.comboBox.addItem("Все")
            for nbn in user.response.matrix:
                window.comboBox.addItem(nbn[1])
            window.comboBox.setCurrentIndex(0)
        print(L.response.matrix)
        matrix = L.response.matrix
        print(matrix)
        #print(SAS)
        paint()
        return True
    elif L.number == 1002:
        global R
        print(L.response.text)
        R = 1002
        window.close()

    else:
        print("БЛЯ")
        return False


def LLL(server):

    if changeling_status == 0:
        column.clear()
        column.append(window.checkBox.isChecked())
        column.append(window.checkBox_2.isChecked())
        column.append(window.checkBox_3.isChecked())
        column.append(window.checkBox_4.isChecked())
        column.append(window.checkBox_5.isChecked())
        column.append(window.checkBox_6.isChecked())
        column.append(window.checkBox_7.isChecked())
        #window.checkBox.isChecked()
        #print(f"SSSSS - {column}")

        if server == True:
            ls()
        else:
            paint()
    elif changeling_status == 1:
        column_u.clear()
        column_u.append(window.checkBox.isChecked())
        column_u.append(window.checkBox_2.isChecked())
        column_u.append(window.checkBox_3.isChecked())
        column_u.append(window.checkBox_4.isChecked())
        column_u.append(window.checkBox_5.isChecked())
        column_u.append(window.checkBox_6.isChecked())
        column_u.append(window.checkBox_7.isChecked())
        #window.checkBox.isChecked()
        #print(f"SSSSS - {column}")

        if server == True:
            ls_u()
        else:
            paint_u()


def start():
    LLL(server = True)
    ls()
    window.tableWidget.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
    #window.tableWidget.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
    #window.tableWidget.horizontalHeader().setSectionResizeMode(4,QHeaderView.ResizeToContents)

def SAS(A, B):
    window.tableWidget.setRangeSelected(QTableWidgetSelectionRange(A, 0, A, window.tableWidget.columnCount()-1), True)
    if changeling_status == 0:
        global target
        print(A, B)
        target = A
        #matrix["ls"]
        #png(matrix["ls"][7][A])
        print(matrix[A][7])
        window.label_2.setText("Описания:\n{}".format(str(matrix[A][8])))
        if matrix[A][7] != None:
            print(matrix[A][7])
            SAS = f"{recording_spark_api.route[0]}/item/{matrix[A][0]}"
            if os.path.exists(SAS):
                hash_L = hashlib.md5(open(SAS,'rb').read()).hexdigest()
                if matrix[A][7] == str(hash_L):
                    window.label_4.setPixmap(QtGui.QPixmap(SAS).scaledToWidth(200, mode = Qt.FastTransformation))
                else:
                    ss = recording_spark_api.item.ls_icon(matrix[A][0])
                    if ss.number == 200:
                        window.label_4.setPixmap(QtGui.QPixmap(SAS).scaledToWidth(200, mode = Qt.FastTransformation))

            else:
                ss = recording_spark_api.item.ls_icon(matrix[A][0])
                if ss.number == 200:
                    window.label_4.setPixmap(QtGui.QPixmap(SAS).scaledToWidth(200, mode = Qt.FastTransformation))
        else:
            window.label_4.setText("Инвентарный ID:\n{}".format(str(matrix[A][9])))



        #window.label_8.setText("В " + columns[B])
    elif changeling_status == 1:
        global target_u
        print(A, B)
        target_u = A
        matrix_u[A][7]
        #a_1 = str(matrix_u[A][7] & 1)
        a_1 = ""
        a_2 = ""
        b_1 = ""
        b_2 = ""
        a = 0
        f = False
        while a != 12:
            if f == False:
                if (matrix_u[A][7] >> a & 1) == 1:
                    a_1 = a_1 + "●"
                else:
                    a_1 = a_1 + "○"
                a = a + 1
                print(a, "A_1")
                if a == 5:
                    a_1 = a_1 + "|"
                    a_2 = a_1
                    a_1 = ""
                f = True
            else:

                if (matrix_u[A][7] >> a & 1) == 1:
                    b_1 = b_1 + "●"
                else:
                    b_1 = b_1 + "○"
                a = a + 1
                print(a, "A_2")
                if a == 6:
                    b_1 = b_1 + "|"
                    b_2 = b_1
                    b_1 = ""
                f = False
        #window.label_4.setText(f"Права:\nuser   |   item    \n--++**|--++**\n|{a_1}|\n|чзчзчз|чзчзчз|\n")
        window.label_4.setText(f"Права:\nuser|item\nз|{b_1}|{b_2}з\nч|{a_1}|{a_2}ч\n|▁▃▆|▁▃▆|\n")
        window.label_2.setText(f"Имя группы:\n{matrix_u[A][6]}\nID группы:\n{matrix_u[A][5]}\n")


def update_matrix_target():
    th = Thread(target=update_matrix)
    th.start()

def update_matrix():
    global changeling_status
    window.pushButton_7.setEnabled(False)
    window.pushButton_5.setEnabled(False)
    window.pushButton_2.setEnabled(False)
    window.pushButton_3.setEnabled(False)
    window.pushButton_4.setEnabled(False)
    window.pushButton_8.setEnabled(False)


    print("\nFalse\n")
    time.sleep(4)
    print(f"update_matrix - {changeling_status}")
    a = window.tableWidget.rowCount()
    for l in range(a):
        window.tableWidget.removeRow(0)
    if changeling_status == 0:
        ls()
    elif changeling_status == 1:
        ls_u()
    window.pushButton_7.setEnabled(True)
    window.pushButton_5.setEnabled(True)
    window.pushButton_2.setEnabled(True)
    window.pushButton_3.setEnabled(True)
    window.pushButton_4.setEnabled(True)
    window.pushButton_8.setEnabled(True)

def purgen():
    global R
    if changeling_status == 0:
        msg = QMessageBox.question(window, "   !!!ВНИМАНИЕ!!!   ",
        "Вы пытаетесь удолить предмет!\nИнформация о нём будет безвозвратно утерена.\nПроболжать ?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

        if msg == QMessageBox.Yes:
            print(f"AAA = {matrix[target][0]}")
            print(f"AAA = {matrix[target]}")
            print(f"AAA = {target}")
            l = recording_spark_api.item.rm(matrix[target][0])
            if l.number == 200:
                print("OK")
                if os.path.isfile(f"{recording_spark_api.route[0]}/item/{matrix[target][0]}"):
                    os.remove(f"{recording_spark_api.route[0]}/item/{matrix[target][0]}")
                update_matrix()
            elif l.number == 1002:

                print(l.response.text)
                R = 1002
                window.close()
            else:
                INFO(l.number, l.response.text)
            print(l.number)
    elif changeling_status == 1:
        msg = QMessageBox.question(window, "   !!!ВНИМАНИЕ!!!   ",
        "Вы пытаетесь удолить уч. запесь!\nИнформация о нём будет безвозвратно утерена.\nПроболжать ?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

        if msg == QMessageBox.Yes:
            #print(f"AAA = {matrix[target][0]}")
            #print(f"AAA = {matrix[target]}")
            #print(f"AAA = {target}")
            l = recording_spark_api.user.rm(matrix[target][0])
            if l.number == 200:
                print("OK")
                update_matrix()
            elif l.number == 1002:
                print(l.response.text)
                R = 1002
                window.close()
            else:
                INFO(l.number, l.response.text)
            print(l.number)


def item(P):
    if P == 1:
        A = GUI_item.open_l (matrix[target], P, themes)
    elif P == 0:
        A = GUI_item.open_l ([], P, themes)
    elif P == 2:
        A = GUI_item.open_l (matrix[target], P, themes)
    print(f"AAAAA{A}")
    if A != -1:
        ls()

def user(P):
    if P == 1:
        A = GUI_user.open_l (matrix_u[target_u], P, themes)
    elif P == 0:
        A = GUI_user.open_l ([], P, themes)
    if P == 2:
        A = GUI_user.open_l (matrix_u[target_u], P, themes)
    print(f"AAAAA{A}")
    #if A != -1:
        #ls()

def log_out():
    print("AAAA")
    global R
    R = 1
    window.close()

import asyncio
from threading import Thread
def changeling_target():
    th = Thread(target=changeling)
    th.start()

def AAA():
    while True:
        event_set = event.wait()
        if event_set:
            changeling()
            print("Event received, releasing thread...")
        else:
            print("Time out, moving ahead without event...")
        event.clear()
    """
    print("AAA_AAA")
    if A:
        print("SSS")
        #btn_apply = window.buttonBox.button(QtGui.pushButton_5.Apply)
        #btn_apply.setVisible(True)
        window.pushButton_5.setEnabled(True)
    else:
        #btn_apply = window.buttonBox.button(QtGui.pushButton_5.Apply)
        #btn_apply.setVisible(False)
        window.pushButton_5.setEnabled(False)
    """
def changeling():
    global changeling_status
    #await AAA(False)
    #th = Thread(target=AAA, args=(False,))
    #th.start()
    window.pushButton_7.setEnabled(False)
    window.pushButton_5.setEnabled(False)
    window.pushButton_2.setEnabled(False)
    window.pushButton_3.setEnabled(False)
    window.pushButton_4.setEnabled(False)
    window.pushButton_8.setEnabled(False)

    if changeling_status == 0:
        changeling_status = 1
        column_u_clon = tuple(column_u)
        print(column_u_clon, "column_u_clon")
        print(column, "column")
        column_u[1] = 1
        print(column_u_clon, "column_u_clon")
        window.pushButton_5.setIcon(QIcon(f"{put}content/icon/item.png"))
        ls_u()
        window.label.setText("Фильтровать по группам")
        window.checkBox.setText(columns_u[0])
        window.checkBox_2.setText(columns_u[1])
        window.checkBox_3.setText(columns_u[2])
        window.checkBox_4.setText(columns_u[3])
        window.checkBox_5.setText(columns_u[4])
        window.checkBox_6.setText(columns_u[5])
        window.checkBox_7.setText(columns_u[6])
        window.checkBox.setChecked(column_u_clon[0])
        window.checkBox_2.setChecked(column_u_clon[1])
        window.checkBox_3.setChecked(column_u_clon[2])
        window.checkBox_4.setChecked(column_u_clon[3])
        window.checkBox_5.setChecked(column_u_clon[4])
        window.checkBox_6.setChecked(column_u_clon[5])
        window.checkBox_7.setChecked(column_u_clon[6])

        print(column, "column")
    elif changeling_status == 1:
        changeling_status = 0
        column_clon = tuple(column)
        print(column_clon, "column_clon")
        column[1] = 1
        print(column_clon, "column_clon")
        window.pushButton_5.setIcon(QIcon(f"{put}content/icon/user.png"))
        ls()
        window.checkBox.setText(columns[0])
        window.checkBox_2.setText(columns[1])
        window.checkBox_3.setText(columns[2])
        window.checkBox_4.setText(columns[3])
        window.checkBox_5.setText(columns[4])
        window.checkBox_6.setText(columns[5])
        window.checkBox_7.setText(columns[6])
        window.label.setText("Фильтровать по пользователем")
        window.checkBox.setChecked(column_clon[0])
        window.checkBox_2.setChecked(column_clon[1])
        window.checkBox_3.setChecked(column_clon[2])
        window.checkBox_4.setChecked(column_clon[3])
        window.checkBox_5.setChecked(column_clon[4])
        window.checkBox_6.setChecked(column_clon[5])
        window.checkBox_7.setChecked(column_clon[6])
    print()
    #await AAA(True)
    window.pushButton_7.setEnabled(True)
    window.pushButton_5.setEnabled(True)
    window.pushButton_2.setEnabled(True)
    window.pushButton_3.setEnabled(True)
    window.pushButton_4.setEnabled(True)
    window.pushButton_8.setEnabled(True)

#th = Thread(target=AAA)
#th.start()

def ppp(A):
    if changeling_status == 0:
        R = item(A)
    elif changeling_status == 1:
        user(A)

def open_l(app, user_name, themes_l):
    global window, R, changeling_status, themes
    themes = themes_l
    R = 0
    changeling_status = 0



    #if not QApplication.instance():
    #    app = QApplication(sys.argv)
    #else:
    #    app = QApplication.instance()
    #app = QApplication(sys.argv)

    ui_file_name = put + "content/ui/mainwindow.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    window.show()
    pal = window.palette()

    #pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QColor("#24587A"))
    #pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QColor("#03426A"))
    #window.setPalette(pal)

    #window.tableWidget.setStyleSheet("background-color:'#000000';")
    window.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

    #window.playlist_table.setSelectionMode(QAbstractItemView.NoSelection)
    window.setStyleSheet(open(f"{put}content/themes/{themes}/main_all").read())



    #window.mainWindow.objectName("SSSSSSSSSSS")
    window.setWindowTitle('Recording Spark')

    #window.label_5.setText(user_name)


    """
    if X_Pars["short_token"] != "":
        if ls():
            print("OK")
        else:
            if renew():
                print("OK")
                ls()
    """
    #user_png_download()
            #else:
                #if X_Pars["server"] != "":
                    #window.lineEdit_3.setText(X_Pars["server"])
                #if X_Pars["email"] != "":
                    #window.lineEdit.setText(X_Pars["email"])




    window.label_5.setText(user_name)
    window.tableWidget.cellClicked.connect(SAS)
    #window.pushButton_4.clicked.connect(GUI_item.open_l)
    window.pushButton_4.clicked.connect(lambda:ppp (0))
    window.pushButton_2.clicked.connect(lambda:ppp (1))
    window.pushButton_8.clicked.connect(lambda:ppp (2))

    window.pushButton_7.clicked.connect(update_matrix_target)
    window.pushButton_3.clicked.connect(purgen)
    #window.pushButton_5.clicked.connect(changeling)
    #window.pushButton_5.clicked.connect(lambda:event.set())
    window.pushButton_5.clicked.connect(changeling_target)

    #ls()
    window.setWindowIcon(QIcon(f"{put}content/icon/2icon.png"))
    window.pushButton_5.setIcon(QIcon(f"{put}content/icon/user.png"))
    window.pushButton_8.setIcon(QIcon(f"{put}content/icon/copy.png"))
    window.pushButton_4.setIcon(QIcon(f"{put}content/icon/add.png"))
    window.pushButton_3.setIcon(QIcon(f"{put}content/icon/rm.png"))
    window.pushButton_7.setIcon(QIcon(f"{put}content/icon/update.png"))
    window.pushButton_6.setIcon(QIcon(f"{put}content/icon/cog-306433_1280.png"))
    window.pushButton_2.setIcon(QIcon(f"{put}content/icon/82-825182_this-free-icons-png-design-of-gray-pencil-icon-gray-pencil.png"))
    window.pushButton.setIcon(QIcon(f"{put}content/icon/uploads_exit_exit_PNG5.png"))

    window.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    QTimer.singleShot(0, start)




    window.checkBox.toggled.connect(lambda:LLL (server = False))
    window.checkBox_2.toggled.connect(lambda:LLL (server = False))
    window.checkBox_3.toggled.connect(lambda:LLL (server = False))
    window.checkBox_4.toggled.connect(lambda:LLL (server = False))
    window.checkBox_5.toggled.connect(lambda:LLL (server = False))
    window.checkBox_6.toggled.connect(lambda:LLL (server = False))
    window.checkBox_7.toggled.connect(lambda:LLL (server = False))
    window.pushButton.clicked.connect(log_out)

    window.pushButton_6.clicked.connect(lambda:settings.open_l ())


    window.comboBox.activated.connect(paint)







    #window.tableWidget.setColumnWidth(0, 40)
    #window.statTable.setSizeAdjustPolicy(window.QAbstractScrollArea.AdjustToContents)
    #window.tableWidget.resizeColumnsToContents()

    #window.tableWidget.ResizeSection(0, 10)


    #png("2021-11-19_11-52.png")


    #window.pushButton_4.clicked.connect(login)
    #window.QtWidgets.QCheckBox.setCheckState(sss)

    #sys.exit(app.exec_())
    app.exec_()
    return R




#open_l()



