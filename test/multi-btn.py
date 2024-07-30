import sys, threading
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class DragButtonExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drag Button Example')
        self.setGeometry(200, 200, 400, 300)

        self.button = QPushButton('Drag Me', self)
        self.button.setGeometry(100, 100, 100, 50)
        self.button.setCheckable(True)
        self.button.setStyleSheet("background-color: lightblue;")
        self.button.clicked.connect(self.pressed)
        self.button.mousePressEvent = self.customMousePressEvent

        # 啟用滑鼠事件偵測
        self.button.setMouseTracking(True)

        self.drag_start_pos = None  # 拖曳開始時的位置

    def customMousePressEvent(self, event):
        print("mouse press")
        print(event.pos())
        print(self.button.geometry())
        # if event.buttons() == Qt.LeftButton and self.button.geometry().contains(event.pos()):
            # self.drag_start_pos = event.pos() - self.button.pos()
        self.drag_start_pos = event.pos()
        # 调用默认的mousePressEvent
        QPushButton.mousePressEvent(self.button, event)
        print("customMousePressEvent : ",self.drag_start_pos)

    def pressed(self):
        print("pressed!!!!")

    # def mousePressEvent(self, event):
    #     print("mouse press")
    #     print(event.pos())
    #     print(self.button.geometry())
    #     print(self.button.geometry().contains(event.pos()))
    #     if event.button() == Qt.LeftButton and self.button.geometry().contains(event.pos()):
    #         self.drag_start_pos = event.pos() - self.button.pos()
    #     print("mouse press")
    #     print(self.drag_start_pos)

    def mouseMoveEvent(self, event):
        print("start: ",self.drag_start_pos)
        print("end: ",event.globalPos())
        if event.buttons() == Qt.LeftButton and self.drag_start_pos is not None:
            # new_pos = event.globalPos() - self.drag_start_pos
            # new_pos.setX(max(0, new_pos.x()))  # 防止按鈕超出左邊界
            # self.button.move(self.mapFromGlobal(new_pos))
            new_pos_delta = event.pos() - self.drag_start_pos
            new_pos_delta.setY(0)
            print("delta: ",new_pos_delta)
            if (new_pos_delta.x() < 0):
                self.button.move(50, 100)
            if (new_pos_delta.x() > 0):
                self.button.move(100,100)
        print("mouse move")

    def mouseReleaseEvent(self, event):
        print(self.drag_start_pos)
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = None
        print("mouse release")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragButtonExample()
    window.show()
    sys.exit(app.exec_())
