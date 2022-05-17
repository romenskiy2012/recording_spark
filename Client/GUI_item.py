from PySide2.QtUiTools import QUiLoader #pip3 install PySide2
from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2.QtCore import QFile, QIODevice, QTimer
from PySide2.QtWidgets import QFileDialog, QMessageBox
import math
from PySide2.QtCore import QStringListModel
import sys
import os
from PySide2.QtGui import QIcon, QPixmap
import requests
put = os.path.dirname(os.path.realpath(__file__)) + "/"#Путь- (part-1)
R = -1
U_1 = 0
U_2 = 0

import recording_spark_api


import json
with open(f"{put}content/json/user.json", "r") as read_file:
    X_Pars = json.load(read_file)

def sex(SSS, window, l):
    ###window.pushButton_2.setEnabled(False)
    print(SSS)
    if l == 0:
        if SSS != U_1:
            window.pushButton_4.setEnabled(True)
        else:
            window.pushButton_4.setEnabled(False)
    elif l == 1:
        if SSS != U_2:
            window.pushButton_5.setEnabled(True)
        else:
            window.pushButton_5.setEnabled(False)


def SAS(window):
    m = window.radioButton.isChecked()
    print(m)
    m = window.radioButton_2.isChecked()
    print(m)

    window.radioButton_2.setChecked(1)

def test(window, L,target, IM):
    global R
    STOP = False
    if IM == 0 or IM == 2:
        icon = window.lineEdit_5.text()
        if icon == None or icon == "":
            print("ТУТ НИЧЕГО НЕТ!!!")
            icon = None
        elif not os.path.exists(icon):
            STOP = True
            msg = QMessageBox(window)
            msg.setWindowTitle(f"ERROE")
            msg.setText(f" \n    Нет такого файла!    \n ")
            msg.exec_()

        print(window.comboBox.currentIndex())
        print(window.comboBox.currentText())

        print(window.comboBox_2.currentIndex())
        print(window.comboBox_2.currentText())

        user_id_1 = L[window.comboBox.currentIndex()][0]
        user_id_2 = L[window.comboBox_2.currentIndex()][0]
        if window.lineEdit_4.text() == "":
            cdcd = None
        else:
            cdcd = int(window.lineEdit_4.text())

        if not (window.lineEdit.text() == "" and window.lineEdit_2.text() == ""):
            M = recording_spark_api.item.add(window.lineEdit.text(), window.lineEdit_2.text(), user_id_1, user_id_2, window.lineEdit_3.text(), cdcd)
            print(M.number)
            if M.number == 200:
                R = M.response.item_id
                print(R, "M.response.item_id")
                if icon != None:
                    M_2 = recording_spark_api.item.add_icon(R, icon)
                    if M_2.number != 200:
                        msg = QMessageBox(window)
                        msg.setWindowTitle(f"ERROE {M_2.number}")
                        msg.setText(f" \n    {M_2.response.text}    \n ")
                        msg.exec_()
                window.close()
                #return R
            else:
                msg = QMessageBox(window)
                msg.setWindowTitle(f"ERROE {M.number}")
                msg.setText(f" \n    {M.response.text}    \n ")
                msg.exec_()
    elif IM == 1:
        if window.lineEdit.text() == target[1]:
            item_name = None
        else:
            item_name = window.lineEdit.text()
        if window.lineEdit_2.text() == target[2]:
            status = None
        else:
            status = window.lineEdit_2.text()
        if window.lineEdit_3.text() == target[8] or (window.lineEdit_3.text() == "" and target[8] == None):
            comments = None
        else:
            comments = window.lineEdit_3.text()
        if window.lineEdit_4.text() == target[9]:
            inventory_id = None
        else:
            if window.lineEdit_4.text() == "" or window.lineEdit_4.text() == None:
                inventory_id = -1
            else:
                inventory_id = int(window.lineEdit_4.text())


        if L[window.comboBox.currentIndex()][0] == target[3]:
            user_id_1 = None
        else:
            user_id_1 = L[window.comboBox.currentIndex()][0]
        if L[window.comboBox.currentIndex()][0] == target[5]:
            user_id_2 = None
        else:
            user_id_2 = L[window.comboBox_2.currentIndex()][0]
        #user_id_1 = L[window.comboBox.currentIndex()][0]
        #user_id_2 = L[window.comboBox_2.currentIndex()][0]



        if window.lineEdit.text() != "" and window.lineEdit_2.text() != "":
            print(item_name, "__", status, "__", user_id_1, "__", user_id_2, "__", comments, "__", inventory_id, "___________________________-")
            print(target[8])
            if item_name == None and status == None and user_id_1 == None and user_id_2 == None and comments == None and inventory_id == -1:
                print("OK")
                if window.lineEdit_5.text() != "не_изменять":
                    if target[7] == None and (window.lineEdit_5.text() == None or window.lineEdit_5.text() == ""):
                        print("Ничё не изменилось!")
                    elif window.lineEdit_5.text() == None or window.lineEdit_5.text() == "":
                        ASSSA = recording_spark_api.item.rm_icon(target[0])
                        if ASSSA.number == 200:
                            if os.path.isfile(f"{recording_spark_api.route[0]}/item/{target[0]}"):
                                os.remove(f"{recording_spark_api.route[0]}/item/{target[0]}")
                            R = 0
                            window.close()
                            #return R
                        else:
                            msg = QMessageBox(window)
                            msg.setWindowTitle(f"ERROE {ASSSA.number}")
                            msg.setText(f" \n    {ASSSA.response.text}    \n ")
                            msg.exec_()
                    else:
                        MK = recording_spark_api.item.add_icon(target[0], window.lineEdit_5.text())
                        if MK.number == 200:
                            R = 0
                            window.close()
                        else:
                            msg = QMessageBox(window)
                            msg.setWindowTitle(f"ERROE {MK.number}")
                            msg.setText(f" \n    {MK.response.text}    \n ")
                            msg.exec_()

            else:
                M = recording_spark_api.item.edit(target[0], item_name, status, user_id_1, user_id_2, comments, inventory_id)
                print(M.number)
                if M.number == 200:
                    if window.lineEdit_5.text() != "не_изменять":
                        if (window.lineEdit_5.text() == None or window.lineEdit_5.text() == ""):
                            MK = recording_spark_api.item.rm_icon(target[0])
                            if MK.number != 200:
                                if os.path.isfile(f"{recording_spark_api.route[0]}/item/{target[0]}"):
                                    os.remove(f"{recording_spark_api.route[0]}/item/{target[0]}")
                            else:
                                msg = QMessageBox(window)
                                msg.setWindowTitle(f"ERROE {MK.number}")
                                msg.setText(f" \n    {MK.response.text}    \n ")
                                msg.exec_()
                        else:
                            MK = recording_spark_api.item.add_icon(target[0], window.lineEdit_5.text())
                            if MK.number != 200:
                                msg = QMessageBox(window)
                                msg.setWindowTitle(f"ERROE {MK.number}")
                                msg.setText(f" \n    {MK.response.text}    \n ")
                                msg.exec_()
                    R = 0
                    window.close()
                    #return R
                else:
                    msg = QMessageBox(window)
                    msg.setWindowTitle(f"ERROE {M.number}")
                    msg.setText(f" \n    {M.response.text}    \n ")
                    msg.exec_()



def SAS_r(window, L, target,N):
    if N == 0:
        window.lineEdit.setText(target[1])
    elif N == 1:
        window.lineEdit_2.setText(target[2])
    elif N == 2:
        window.lineEdit_3.setText(target[8])
    elif N == 3:
        if target[9] == None:
            window.lineEdit_4.setText(None)
        else:
            window.lineEdit_4.setText(str(target[9]))

    elif N == 4:
        window.comboBox.setCurrentIndex(U_1)
        window.pushButton_4.setEnabled(False)
    elif N == 5:
        window.comboBox_2.setCurrentIndex(U_2)
        window.pushButton_5.setEnabled(False)
    elif N == 6:
        window.lineEdit_5.setText("не_изменять")

    print(U_1)
    print(N)



def icon(window):
    Way_2 = QFileDialog.getOpenFileName(window, "Выберете изображение.", "/home/",  "Файлы изображений (*.png *.jpg *.jpeg)")
    Way_3 = Way_2[0]
    window.lineEdit_5.setText(Way_3)


def start(window, L, target, IM):
    for l in L:
        window.comboBox.addItem(l[1])
        window.comboBox_2.addItem(l[1])
    window.lineEdit.setPlaceholderText("Имя")
    window.lineEdit_2.setPlaceholderText("Статус")
    window.lineEdit_3.setPlaceholderText("Коментарий")
    window.lineEdit_4.setPlaceholderText("Инвентарный ID")


    if len(target) != 0:
        global U_1, U_2

        window.lineEdit_5.setPlaceholderText("Удолить")
        window.lineEdit_5.setText("не_изменять")

        print(target)
        window.lineEdit.setText(target[1])
        window.lineEdit_2.setText(target[2])
        window.lineEdit_3.setText(target[8])
        if target[9] == None:
            window.lineEdit_4.setText(None)
        else:
            window.lineEdit_4.setText(str(target[9]))

        K = 0
        m = True
        for p in L:
            if target[3] == p[0]:
                window.comboBox.setCurrentIndex(K)
                U_1 = K
                m = False
                break
            K = K + 1
        if m:
            L.append([target[3],target[4],None,None,None,None])
            window.comboBox.addItem(target[4])
            window.comboBox.setCurrentIndex(K)
            U_1 = K
        K = 0
        m = True
        for p in L:
            if target[5] == p[0]:
                window.comboBox_2.setCurrentIndex(K)
                U_2 = K
                m = False
                break
            K = K + 1
        if m:
            L.append([target[5],target[6],None,None,None,None])
            window.comboBox_2.addItem(target[6])
            window.comboBox_2.setCurrentIndex(K)
            U_2 = K

        print("L")
        window.pushButton_2.setEnabled(False)
        window.pushButton_3.setEnabled(False)
        window.pushButton_4.setEnabled(False)
        window.pushButton_5.setEnabled(False)
        window.pushButton_6.setEnabled(False)
        window.pushButton_7.setEnabled(False)
        window.pushButton_9.setEnabled(False)

        window.setWindowTitle("ID: {} - {}".format(target[0],target[1]))

    if IM == 0 or IM == 2:
        window.lineEdit_5.setPlaceholderText("Выберете изображенмия")
        window.pushButton_2.deleteLater()
        window.pushButton_3.deleteLater()
        window.pushButton_4.deleteLater()
        window.pushButton_5.deleteLater()
        window.pushButton_6.deleteLater()
        window.pushButton_7.deleteLater()
        window.pushButton_9.deleteLater()
        window.label_7.deleteLater()

        window.setWindowTitle("Создания")

def M(window,target,p):
    if p == 4:
        if "не_изменять" != window.lineEdit_5.text():
            window.pushButton_9.setEnabled(True)
        else:
            window.pushButton_9.setEnabled(False)
    if p == 0:
        if target[1] != window.lineEdit.text():
            window.pushButton_2.setEnabled(True)
        else:
            window.pushButton_2.setEnabled(False)
    elif p == 1:
        if target[2] != window.lineEdit_2.text():
            window.pushButton_3.setEnabled(True)
        else:
            window.pushButton_3.setEnabled(False)
    elif p == 2:
        if target[8] != window.lineEdit_3.text():
            window.pushButton_6.setEnabled(True)
        else:
            window.pushButton_6.setEnabled(False)
    elif p == 3:
        #####  !!!СДЕЛАТЬ ПРОВЕРКУ ЧТО ЭТО INT!!!
        print("##################")
        print(window.lineEdit_4.text())
        print("##################")
        if window.lineEdit_4.text() != "":
            try:
                namber = int(window.lineEdit_4.text())
            except ValueError:
                window.pushButton.setEnabled(False)
            else:
                if not window.pushButton.isEnabled():
                    window.pushButton.setEnabled(True)
            if str(target[9]) != window.lineEdit_4.text():
                window.pushButton_7.setEnabled(True)
            else:
                window.pushButton_7.setEnabled(False)
        else:
            print(target[9])
            print(window.lineEdit_4.text())
            if target[9] == None or target[9] == "":
                window.pushButton_7.setEnabled(False)
            else:
                window.pushButton_7.setEnabled(True)

def M_2(window):
    if window.lineEdit_4.text() != "":
        try:
            namber = int(window.lineEdit_4.text())
        except ValueError:
            window.pushButton.setEnabled(False)
            return 0
            #if window.pushButton.isEnabled():
    if "" == window.lineEdit.text() or window.lineEdit_2.text() == "":
        window.pushButton.setEnabled(False)
    else:
        window.pushButton.setEnabled(True)








        #window.lineEdit_2.text()

def GUI(L, target, IM, themes):

    #app = QApplication(sys.argv)

    ui_file_name = put + "/content/ui/item.ui"
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

    window.setWindowIcon(QIcon(f"{put}/content/icon/2icon.png"))

    window.setStyleSheet(open(f"{put}content/themes/{themes}/item_all").read())

    QTimer.singleShot(100, lambda:start(window, L, target, IM))
    # 71A7BB

    #window.pushButton.clicked.connect(lambda:test (window,L))
    window.pushButton.clicked.connect(lambda:test(window, L,target, IM))
    window.pushButton_8.clicked.connect(lambda:icon(window))

    if IM == 1:
        window.pushButton_2.clicked.connect(lambda:SAS_r (window, L, target,0))
        window.pushButton_3.clicked.connect(lambda:SAS_r (window, L, target,1))
        window.pushButton_6.clicked.connect(lambda:SAS_r (window, L, target,2))
        window.pushButton_7.clicked.connect(lambda:SAS_r (window, L, target,3))

        window.pushButton_4.clicked.connect(lambda:SAS_r (window, L, target,4))
        window.pushButton_5.clicked.connect(lambda:SAS_r (window, L, target,5))
        window.pushButton_9.clicked.connect(lambda:SAS_r (window, L, target,6))

        #window.lineEdit.initStyleOption()

        #window.lineEdit.textChanged[str].connect(M)
        window.lineEdit.textChanged.connect(lambda:M (window,target,0))
        window.lineEdit_2.textChanged.connect(lambda:M (window,target,1))
        window.lineEdit_3.textChanged.connect(lambda:M (window,target,2))
        window.lineEdit_4.textChanged.connect(lambda:M (window,target,3))
        window.lineEdit_5.textChanged.connect(lambda:M (window,target,4))


        window.comboBox.activated.connect(lambda:sex (window.comboBox.currentIndex(),window,0))
        window.comboBox_2.activated.connect(lambda:sex (window.comboBox_2.currentIndex(),window,1))



    elif IM == 0 or IM == 2:
        window.lineEdit.textChanged.connect(lambda:M_2 (window))
        window.lineEdit_2.textChanged.connect(lambda:M_2 (window))
        window.lineEdit_4.textChanged.connect(lambda:M_2 (window))


    #window_L.widget.hide()
    #window_L.setStyleSheet('.QWidget {border-image: url(' + A + ') 0 0 0 0 stretch stretch;} .QLabel{border-image: None;}')
    #window_L.pushButton.clicked.connect(lambda:login (window_L))
    #sys.exit(app.exec_())
    #app.exec_()

def open_l(target, IM, themes):
    #print("Кородний коне: {}, а также наш ооочень длинный и живучий токен {}"
    #      .format(recording_spark_api.short_token[0],recording_spark_api.live_token[0],))
    global U_1, U_2, R
    R = 0
    U_1 = 0
    U_2 = 0
    NNN = recording_spark_api.user.ls()
    if NNN.number == 200:
        print(target)
        print(NNN.response.matrix)
        GUI(NNN.response.matrix, target, IM, themes)
    print(f"AAAAA{R}")
    return R

#GUI(0)
