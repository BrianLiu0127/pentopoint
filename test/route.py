import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QPointF, QLineF
import math

class ArrowLabel(QLabel):
    def __init__(self, start, end, parent=None):
        super().__init__(parent)
        self.start = start
        self.end = end
        self.setFixedSize(20, 20)  # Adjust the size as needed
        self.setStyleSheet("background-color: transparent;")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.red, 2)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)

        # Calculate arrow angle
        angle = self.calculate_angle(self.start, self.end)

        # Draw arrow
        self.draw_arrow(painter, self.rect().center(), angle)

    def calculate_angle(self, start, end):
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        return -math.degrees(math.atan2(dy, dx))

    def draw_arrow(self, painter, point, angle):
        painter.translate(point)
        painter.rotate(angle)
        painter.translate(-point)

        arrow_size = 10
        painter.drawLine(point, QPointF(point.x() + arrow_size, point.y()))
        painter.drawLine(QPointF(point.x() + arrow_size, point.y()), QPointF(point.x() + arrow_size - 5, point.y() - 5))
        painter.drawLine(QPointF(point.x() + arrow_size, point.y()), QPointF(point.x() + arrow_size - 5, point.y() + 5))

class MapWidget(QWidget):
    def __init__(self, map_image_path):
        super().__init__()
        self.map_label = QLabel(self)
        self.map_pixmap = QPixmap(map_image_path)
        self.map_label.setPixmap(self.map_pixmap)
        self.map_label.setScaledContents(True)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.map_label)
        self.setLayout(self.layout)

        self.arrow_labels = []
        self.scale_x = 1
        self.scale_y = 1

    def set_path(self, points):
        self.clear_arrows()
        for i in range(len(points) - 1):
            self.add_arrow_label(points[i], points[i + 1])
        self.update()

    def add_arrow_label(self, start, end):
        scaled_start = QPointF(start.x() * self.scale_x, start.y() * self.scale_y)
        scaled_end = QPointF(end.x() * self.scale_x, end.y() * self.scale_y)
        arrow_label = ArrowLabel(scaled_start, scaled_end, self.map_label)
        
        # Move the label to the midpoint between the start and end points
        midpoint = QPointF((scaled_start.x() + scaled_end.x()) / 2, (scaled_start.y() + scaled_end.y()) / 2)
        arrow_label.move(round(midpoint.x() - arrow_label.width() / 2), round(midpoint.y() - arrow_label.height() / 2))
        
        arrow_label.show()
        self.arrow_labels.append(arrow_label)

    def clear_arrows(self):
        for label in self.arrow_labels:
            label.deleteLater()
        self.arrow_labels = []

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_scale()

    def update_scale(self):
        widget_width = self.width()
        widget_height = self.height()
        image_width = self.map_pixmap.width()
        image_height = self.map_pixmap.height()

        self.scale_x = widget_width / image_width
        self.scale_y = widget_height / image_height

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.map_widget = MapWidget('./img/4F平面圖_4aps.png')
        layout.addWidget(self.map_widget)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        self.points = [
            [QPointF(50.5, 50.5), QPointF(150.5, 50.5), QPointF(150.5, 150.5), QPointF(50.5, 150.5)],
            [QPointF(60.2, 60.2), QPointF(160.2, 60.2), QPointF(160.2, 160.2), QPointF(60.2, 160.2)],
            [QPointF(70.1, 70.1), QPointF(170.1, 70.1), QPointF(170.1, 170.1), QPointF(70.1, 170.1)],
        ]
        self.current_index = 0

        add_path_button = QPushButton("Add Path")
        add_path_button.clicked.connect(self.add_path)
        button_layout.addWidget(add_path_button)

    def add_path(self):
        if self.current_index < len(self.points):
            self.map_widget.set_path(self.points[self.current_index])
            self.current_index += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
