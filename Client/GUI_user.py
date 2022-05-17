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
group_list = []
import recording_spark_api


import json
with open(f"{put}content/json/user.json", "r") as read_file:
    X_Pars = json.load(read_file)

def sex(SSS, window,target):
    ###window.pushButton_2.setEnabled(False)
    print(SSS)
    a = 0
    for m in group_list:
        if m[0] == target[5]:
            break
        a = a + 1
    if SSS != a:
        window.pushButton_7.setEnabled(True)
    else:
        window.pushButton_7.setEnabled(False)


def SAS(window):
    m = window.radioButton.isChecked()
    print(m)
    m = window.radioButton_2.isChecked()
    print(m)

    window.radioButton_2.setChecked(1)

def test(window, target, IM):
    global R
    if IM == 0 or IM == 2:
        #print(window.comboBox.currentIndex())
        #print(window.comboBox.currentText())

        #print(window.comboBox_2.currentIndex())
        #print(window.comboBox_2.currentText())
        group_id = group_list[window.comboBox.currentIndex()][0]
        E_1 = window.checkBox.isChecked()
        E_2 = window.checkBox_2.isChecked()

        # add(user_name, email, password, avatar, active, group_id)
        M = recording_spark_api.user.add(window.lineEdit.text(), window.lineEdit_2.text(), window.lineEdit_3.text(), E_1, E_2, group_id)
        print(M.number)
        if M.number == 200:
            R = M.response.user_id
            window.close()
            #return R
        else:
            msg = QMessageBox(window)
            msg.setWindowTitle(f"ERROE {M.number}")
            msg.setText(f" \n    {M.response.text}    \n ")
            msg.exec_()
    elif IM == 1:
        #group_id = target   email, password, avatar, active, group_id
        group_id = group_list[window.comboBox.currentIndex()][0]
        E_1 = window.checkBox.isChecked()
        E_2 = window.checkBox_2.isChecked()
        if window.lineEdit_3.text() == "" or window.lineEdit_3.text() == None:
            password = None
        else:
            password = window.lineEdit_3.text()
        if window.lineEdit.text() == target[1]:
            user_name = None
        else:
            user_name = window.lineEdit.text()
        if window.lineEdit_2.text() == target[2]:
            email = None
        else:
            email = window.lineEdit_2.text()
        if window.checkBox.isChecked() == target[3]:
            avatar = None
        else:
            avatar = window.checkBox.isChecked()
        print(window.checkBox_2.isChecked(), target[4])
        if window.checkBox_2.isChecked() == target[4]:
            active = None
        else:
            active = window.checkBox_2.isChecked()


        if group_list[window.comboBox.currentIndex()][0] == target[5]:
            group_id = None
        else:
            group_id = group_list[window.comboBox.currentIndex()][0]

        if (target[4] == 1 and window.checkBox_2.isChecked() == False) or (password != None):
            msg = QMessageBox.question(window, "   !!!ВНИМАНИЕ!!!   ",
            "Вы пытаетесь отключить/сменить пароль у этой учётной запеси!\nВсе открытые сесии будут закрыты\nПроболжать ?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

            if msg == QMessageBox.Yes:
                M = recording_spark_api.user.edit(target[0],user_name, email, password, avatar, active, group_id)
                print(M.number)
                if M.number == 200:
                    R = 0
                    window.close()
                    #return R
                else:
                    msg = QMessageBox(window)
                    msg.setWindowTitle(f"ERROE {M.number}")
                    msg.setText(f" \n    {M.response.text}    \n ")
                    msg.exec_()
        else:
            M = recording_spark_api.user.edit(target[0],user_name, email, password, avatar, active, group_id)
            print(M.number)
            if M.number == 200:
                R = 0
                window.close()
                #return R
            else:
                msg = QMessageBox(window)
                msg.setWindowTitle(f"ERROE {M.number}")
                msg.setText(f" \n    {M.response.text}    \n ")
                msg.exec_()



def SAS_r(window, target,N):
    if N == 0:
        window.lineEdit.setText(target[1])
    elif N == 1:
        window.lineEdit_2.setText(target[2])
    elif N == 2:
        window.checkBox_2.setChecked(target[4])
        window.pushButton_6.setEnabled(False)
        #window.lineEdit_3.setText(target[8])
    elif N == 3:
        a = 0
        for m in group_list:
            if m[0] == target[5]:
                break
            a = a + 1
        window.comboBox.setCurrentIndex(a)
        window.pushButton_7.setEnabled(False)

    elif N == 4:
        #window.comboBox.setCurrentIndex(U_1)
        window.lineEdit_3.setText("")
        window.pushButton_4.setEnabled(False)
    elif N == 5:
        window.checkBox.setChecked(target[3])
        window.pushButton_5.setEnabled(False)

    print(U_1)
    print(N)



def start(window, target, IM):
    print(f"target - {target}")
    global group_list
    Alo = recording_spark_api.ls_group()
    if Alo.number == 200:
        group_list = Alo.response.matrix
        #for l in L:
        #    window.comboBox.addItem(l[1])
        #    window.comboBox_2.addItem(l[1])
        window.lineEdit.setPlaceholderText("Имя")
        window.lineEdit_2.setPlaceholderText("")
        window.lineEdit_3.setPlaceholderText("")
        for mlo in group_list:
            window.comboBox.addItem(mlo[1])


        if len(target) != 0:


            print(target)
            window.lineEdit.setText(target[1])
            window.lineEdit_2.setText(target[2])
            #window.lineEdit_3.setText(target[8])


            K = 0
            m = True
            print(f"group_list - {group_list}, {target}")
            for p in group_list:
                if target[5] == p[0]:
                    window.comboBox.setCurrentIndex(K)
                    U_1 = K
                    m = False
                    break
                K = K + 1
            if m:
                group_list.append([target[5],target[6],target[7]])
                window.comboBox.addItem(target[6])
                window.comboBox.setCurrentIndex(K)
            #if m:
            #    L.append([target[3],target[4],None,None,None,None])
            #    window.comboBox.addItem(target[4])
            #    window.comboBox.setCurrentIndex(K)
            #    U_1 = K
            if target[4] == 1:
                window.checkBox_2.setChecked(True)
            if target[3] == 1:
                window.checkBox.setChecked(True)


            print("L")
            window.pushButton_2.setEnabled(False)
            window.pushButton_3.setEnabled(False)
            window.pushButton_4.setEnabled(False)
            window.pushButton_5.setEnabled(False)
            window.pushButton_6.setEnabled(False)
            window.pushButton_7.setEnabled(False)

            window.setWindowTitle("ID: {} - {}".format(target[0],target[1]))

        if IM == 0 or IM == 2:
            window.pushButton_2.deleteLater()
            window.pushButton_3.deleteLater()
            window.pushButton_4.deleteLater()
            window.pushButton_5.deleteLater()
            window.pushButton_6.deleteLater()
            window.pushButton_7.deleteLater()
            window.label_7.deleteLater()

            window.setWindowTitle("Создания")

def M(window,target,p):
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
        if not ("" == window.lineEdit_3.text() or window.lineEdit_3.text() == None): # Проблема
            window.pushButton_4.setEnabled(True)
        else:
            window.pushButton_4.setEnabled(False)
    elif p == 3:
        if window.checkBox.isChecked() != bool(target[3]):
            window.pushButton_5.setEnabled(True)
        else:
            window.pushButton_5.setEnabled(False)
    elif p == 4:
        print(window.checkBox_2.isChecked())
        if window.checkBox_2.isChecked() != bool(target[4]):
            window.pushButton_6.setEnabled(True)
        else:
            window.pushButton_6.setEnabled(False)

        #####  !!!СДЕЛАТЬ ПРОВЕРКУ ЧТО ЭТО INT!!!

            #if target[9] == None or target[9] == "":
            #    window.pushButton_7.setEnabled(False)
            #else:
            #    window.pushButton_7.setEnabled(True)

def M_2(window):
    print()
    """
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
    """







        #window.lineEdit_2.text()

def GUI(target, IM, themes):
    #app = QApplication(sys.argv)

    ui_file_name = put + "/content/ui/user.ui"
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

    window.setStyleSheet(open(f"{put}content/themes/{themes}/user_all").read())

    QTimer.singleShot(0, lambda:start(window, target, IM))
    # 71A7BB

    #window.pushButton.clicked.connect(lambda:test (window,L))
    window.pushButton.clicked.connect(lambda:test(window, target, IM))

    if IM == 1:
        window.pushButton_2.clicked.connect(lambda:SAS_r (window, target,0))
        window.pushButton_3.clicked.connect(lambda:SAS_r (window, target,1))
        window.pushButton_6.clicked.connect(lambda:SAS_r (window, target,2))
        window.pushButton_7.clicked.connect(lambda:SAS_r (window, target,3))

        window.pushButton_4.clicked.connect(lambda:SAS_r (window, target,4))
        window.pushButton_5.clicked.connect(lambda:SAS_r (window, target,5))

        #window.lineEdit.initStyleOption()

        #window.lineEdit.textChanged[str].connect(M)
        window.lineEdit.textChanged.connect(lambda:M (window,target,0))
        window.lineEdit_2.textChanged.connect(lambda:M (window,target,1))
        window.lineEdit_3.textChanged.connect(lambda:M (window,target,2))


        window.comboBox.activated.connect(lambda:sex (window.comboBox.currentIndex(),window, target))


        window.checkBox.stateChanged.connect(lambda:M (window, target, 3))
        window.checkBox_2.stateChanged.connect(lambda:M (window, target, 4))



    elif IM == 0 or IM == 2:
        window.lineEdit.textChanged.connect(lambda:M_2 (window))
        window.lineEdit_2.textChanged.connect(lambda:M_2 (window))


    #window_L.widget.hide()
    #window_L.setStyleSheet('.QWidget {border-image: url(' + A + ') 0 0 0 0 stretch stretch;} .QLabel{border-image: None;}')
    #window_L.pushButton.clicked.connect(lambda:login (window_L))
    #sys.exit(app.exec_())
    #app.exec_()
    print("SEX")

def open_l(target, IM, themes):
    #print("Кородний коне: {}, а также наш ооочень длинный и живучий токен {}"
    #      .format(recording_spark_api.short_token[0],recording_spark_api.live_token[0],))
    global R
    R = 0
    print(target)
    GUI(target, IM, themes)
    print(f"AAAAA{R}")
    return R

#GUI(0)

