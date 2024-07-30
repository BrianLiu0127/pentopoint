import sys, os, time, threading, random
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread, QPointF
# import resource_rc
# import WiFi_function as WiFi
# import GoogleAPI_function
# import Temp
# from astsp import TspSolver
# import keyboard

class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("Login.ui",self)
        self.HomeButton.clicked.connect(self.returnHome)
        self.loginBtn.clicked.connect(self.loginclick)

    def loginclick(self):
        print("login!")
        print("account:", self.account_input.text())
        print("password:", self.password_input.text())
    
    def returnHome(self):
        # self.pushButton.setStyleSheet("background-color: yellow;")
        print("back to home")

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
ll = Login()
ll.show()
QApplication.processEvents()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")