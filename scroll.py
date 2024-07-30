# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QScrollArea Test')
        # self.setGeometry(400, 400, 400, 800)

        formLayout = QFormLayout()
        groupBox = QGroupBox()

        for n in range(100):
            # label1 = QLabel('Slime_%2d' % n)
            # label2 = QLabel()
            # label2.setPixmap(QPixmap('./img/home.png'))
            button = QPushButton(str(n),self)
            button.setStyleSheet("background-color:#939597;font-size:20px;color:#000000;")
            button.setFixedHeight(100)
            button.setFixedWidth(370)
            formLayout.addRow(button)
            # formLayout.addRow(button)

        groupBox.setLayout(formLayout)

        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())