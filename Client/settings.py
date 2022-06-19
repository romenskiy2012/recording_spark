from PySide2.QtUiTools import QUiLoader #pip3 install PySide2
from PySide2.QtWidgets import QApplication, QTableWidgetItem, QLabel
from PySide2.QtCore import QFile, QIODevice, QTimer
from PySide2.QtWidgets import QFileDialog, QMessageBox
import math
from PySide2.QtCore import QStringListModel
import sys
import os
from PySide2.QtGui import QIcon, QPixmap
import requests
import recording_spark_api
put = os.path.dirname(os.path.realpath(__file__)) + "/"#Путь- (part-1)
R = 0

def start(window):
    P = recording_spark_api.ls_sessions()
    print(P.number)
    if P.number:
        LKL = ["Имя компа", "IP", "Дата входа", "№"]
        HG = ""
        m = 0
        print(P.response.matrix)
        for A in P.response.matrix:
            for G in A:
                HG = HG + f"{LKL[m]}: {G}\n"
                m = m + 1
            m = 0
            HG = HG + "\n\n"

        object = QLabel(f'{HG}')
        window.scrollArea.setWidget(object)

def SAS_r (window):
    print("QW")

def sessions(window):
    msg = QMessageBox.question(window, "   !!!ВНИМАНИЕ!!!   ",
            "Вы пытаетесь закрыть все сесии!\nВсе открытые сесии будут закрыты\nПроболжать ?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

    if msg == QMessageBox.Yes:
        M = recording_spark_api.full_closure_session()
        if M.number != 200:
            msg = QMessageBox(window)
            msg.setWindowTitle(f"ERROE {M.number}")
            msg.setText(f" \n    {M.response.text}    \n ")
            msg.exec_()

def GUI():
    #app = QApplication(sys.argv)

    ui_file_name = put + "/content/ui/settings.ui"
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

    window.setStyleSheet("""
        .QMainWindow{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 '#56A0BB', stop:1 '#759BBD');}
        QLabel{color: rgb(255, 255, 255);
        background-color: rgb(54, 54, 54, 150);
        border-radius: 15px;
        }

        QLineEdit{
        	border-radius: 15px;
            background: rgb(54, 54, 54, 150);
            color:  rgb(255, 255, 255);
            }

        QComboBox:on {
            padding-top: 3px;
            padding-left: 4px;
        }


        QComboBox{
        color: '#ffffff';
        background-color: rgb(54, 54, 54, 150);
        border-radius: 15px;
        selection-color: '#539b6a';
        selection-background-color: rgb(119, 119, 119, 150);
        selection-border-radius: 15px;


        }
        QComboBox.QAbstractItemView{
        border: 1px solid grey;
        background-color: rgb(54, 54, 54, 250);
        color: rgb(54, 54, 54, 0);
        selection-color: '#539b6a';
        selection-background-color: rgb(54, 54, 54, 150);
        }



        QComboBox::down-arrow {
            background-color: rgb(54, 54, 54, 0);}

        QComboBox::drop-down{
            background-color: rgb(54, 54, 54, 0);
            border-left-color: "#000000";
        }



        .QPushButton {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #c9d6ff, stop:1 #e2e2e2);
        color: #1b1b1b;
        border: none;
        border-radius: 10px;
        text-align: center;
        }
        .QPushButton:hover {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #97A9E3, stop:1 #D2D2D2);
        }
        .QPushButton:pressed {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #7186CB, stop:1 #C0C0C0);
        }


        """)
    oloss = "background: rgb(0, 0, 0, 0%); color:  rgb(0, 0, 0, 0%);"
    window.label_4.setStyleSheet(oloss)

    QTimer.singleShot(100, lambda:start(window))

    window.pushButton_2.clicked.connect(lambda:SAS_r (window))
    window.pushButton.clicked.connect(lambda:sessions(window))


    print("A")

def open_l():
    #print("Кородний коне: {}, а также наш ооочень длинный и живучий токен {}"
    #      .format(recording_spark_api.short_token[0],recording_spark_api.live_token[0],))
    global R
    R = 0
    GUI()
    print(f"AAAAA{R}")
    return R








