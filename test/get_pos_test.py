import os
import sys
import time
import random
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QPushButton

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
import sys, time, threading

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('oxxo.studio')
        self.resize(300, 200)
        # self.event = threading.Event()
        self.ui()
        self.run()
        self.pos = (0,0)

    def ui(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(10, 10, 100, 30)
        
        # self.label_b = QtWidgets.QLabel(self)
        # self.label_b.setGeometry(10, 50, 100, 30)

    def get_wifi_pos(self):
        while(1):
            time.sleep(5)
            self.pos = (100,100)
            self.label.setText("100,100")
            print("wifi:100,100")

    def get_imu_pos(self):
        while(1):
            time.sleep(1)
            self.pos=(self.pos[0]+1,self.pos[1]+1)
            print(self.pos)
            text = str(self.pos[0])+","+str(self.pos[1])
            self.label.setText(text)
            print("IMU")

    # def a(self):
    #     self.event.wait()             # 等待事件被觸發
    #     for i in range(0,5):
    #         self.label_a.setText(str(i))
    #         print('A:',i)
    #         time.sleep(0.5)

    # def b(self):
    #     for i in range(0,50,10):
    #         if i>20:
    #             self.event.set()      # 觸發事件
    #         self.label_b.setText(str(i))
    #         print('B:',i)
    #         time.sleep(0.5)

    def run(self):
        self.thread_wifi = QThread()
        self.thread_wifi.run = self.get_wifi_pos
        self.thread_wifi.start()
        self.thread_imu = QThread()
        self.thread_imu.run = self.get_imu_pos
        self.thread_imu.start()

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    # Form.thread_wifi = QThread()
    # Form.thread_wifi.run = Form.get_wifi_pos
    # Form.thread_wifi.start()
    # Form.thread_imu = QThread()
    # Form.thread_imu.run = Form.get_imu_pos
    # if not Form.thread_wifi.isFinished():
    #     Form.thread_imu.start()
    sys.exit(app.exec_())