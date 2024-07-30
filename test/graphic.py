import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QFont, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create a QGraphicsScene
        self.scene = QGraphicsScene()

        # Load the full image
        self.fullImage = QPixmap('./img/4F平面圖_4aps.png')
        # self.fullImageItem = QGraphicsPixmapItem(self.fullImage)
        self.fullImageItem = QLabel()
        self.fullImageItem.setPixmap(self.fullImage)
        self.scene.addWidget(self.fullImageItem)

        # Add a second label on top of the image
        self.textItem = QGraphicsTextItem("Overlay Text")
        self.textItem.setDefaultTextColor(Qt.red)
        self.textItem.setFont(QFont("Arial", 30))
        self.textItem.setPos(50, 50)  # Set the position of the text
        self.scene.addItem(self.textItem)

        # Create a QGraphicsView
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Button to toggle zoom
        self.btn = QPushButton('Zoom In/Out', self)
        self.btn.clicked.connect(self.toggleZoom)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

        self.setWindowTitle('Image Viewer')
        self.show()

        self.zoomed = False

    def toggleZoom(self):
        if self.zoomed:
            self.view.resetTransform()
        else:
            self.view.scale(1.5, 1.5)  # Adjust the scaling factor as needed
        
        self.zoomed = not self.zoomed

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageWindow()
    sys.exit(app.exec_())
