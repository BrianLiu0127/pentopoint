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
from PyQt5.QtCore import QThread
import resource_rc
import WiFi_function as WiFi
import GoogleAPI_function
import Temp

SCALE_MAP = 13 #19.49

class Item(QPushButton):
    def __init__(self):
        super(Item,self).__init__()
        self.right = 1
        self.pos = (0,0)
        self.isnotclass = 0
        self.shelf = ""
        self.clicked.connect(lambda:MapList.showitem(self))
        # self.clicked.connect(lambda:MapList.delList(self))
        # self.mousePressEvent = self.customMousePressEvent


def generate_List(file_name):
    #generate shopping list
    # text = GoogleAPI_function.detect_text("./List.jpg", GoogleAPI_function.api_key)
    # print(text)
    # text = "咖啡\n威士忌\n麵粉\n油\n維他命\n紙巾\n豆腐\n餅乾\n米\n牛奶\n大象\n"
    text = "茶\n啤酒\n米\n衛生紙\n堅果\n洋芋片"
    targets = text.split("\n")
    # targets.remove('')
    list = []
    for product in targets:
        [shelf, keyword] = Temp.find_shelf_with_keywords(product_name=product)
        [x, y, label] = Temp.find_shelf_position(shelf, keyword)
        list.append((product,x,y,label,shelf))
        print(shelf)
        print(keyword)
        print(x,y,label)
    # for i in range(15):
    #     name = "item"+str(i)
    #     x = random.randrange(31)
    #     y = random.randrange(30)
    #     list.append((name,x,y))
    return list
    # return [("banana",1,12),("apple",2,24),("banana1",1,12),("apple1",2,24),("banana2",1,12),("apple2",2,24),("banana3",1,12),("apple3",2,24),("banana4",1,12),("apple4",2,24),("banana5",1,12),("apple5",2,24),("banana6",1,12),("apple6",2,24),("banana7",1,12),("apple7",2,24),("banana",1,12),("apple",2,24),("banana1",1,12),("apple1",2,24),("banana2",1,12),("apple2",2,24),("banana3",1,12),("apple3",2,24),("banana4",1,12),("apple4",2,24),("banana5",1,12),("apple5",2,24),("banana6",1,12),("apple6",2,24),("banana7",1,12),("apple7",2,24)]
    # return [("banana",1,12),("apple",2,24)]

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("MainWindow.ui",self)
        self.pushButton.clicked.connect(self.changescreen)

    def changescreen(self):
        # self.pushButton.setStyleSheet("background-color: yellow;")
        print("Clicked")
        widget.setCurrentIndex(widget.currentIndex()+1)

class CameraScreen(QMainWindow):
    def __init__(self):
        super(CameraScreen, self).__init__()
        loadUi("CameraScreen.ui",self)
        self.HomeButton.clicked.connect(self.returnHome)
        self.Capture.pressed.connect(self.click_photo)
        self.Capture.released.connect(self.released_photo)
        

        self.available_cameras = QCameraInfo.availableCameras() 

		# if no camera found 
        if not self.available_cameras: 
			# exit the code 
            sys.exit()
        
        self.save_path = os.getcwd() 

		# creating a QCameraViewfinder object 
        self.viewfinder = QCameraViewfinder() 

		# showing this viewfinder 
        self.viewfinder.show()

		# making it central widget of main window 
        self.verticalLayout.addWidget(self.viewfinder)
		# Set the default camera. 
        self.select_camera(0) 

		# creating a tool bar 
        # toolbar = QToolBar("Camera Tool Bar") 

		# adding tool bar to main window 
        # self.addToolBar(toolbar) 

		# creating a photo action to take photo 
        # click_action = QAction("Click photo", self) 

		# adding action to it 
		# calling take_photo method 
        # click_action.triggered.connect(self.click_photo) 
    def select_camera(self, i): 

		# getting the selected camera 
        self.camera = QCamera(self.available_cameras[i]) 

		# setting view finder to the camera 
        self.camera.setViewfinder(self.viewfinder) 

		# setting capture mode to the camera 
        # self.camera.setCaptureMode(QCamera.CaptureStillImage) 
        self.camera.setCaptureMode(QCamera.CaptureViewfinder) 

		# if any error occur show the alert 
        self.camera.error.connect(lambda: self.alert(self.camera.errorString())) 

		# start the camera 
        self.camera.start() 

		# creating a QCameraImageCapture object 
        self.capture = QCameraImageCapture(self.camera) 

		# showing alert if error occur 
        self.capture.error.connect(lambda error_msg, error, 
								msg: self.alert(msg)) 

		# when image captured showing message 
		# self.capture.imageCaptured.connect(lambda d, 
		# 								i: self.status.showMessage("Image captured : "
		# 															+ str(self.save_seq))) 

		# getting current camera name 
        self.current_camera_name = self.available_cameras[i].description() 
        print(self.current_camera_name)
		# initial save sequence 
        # self.save_seq = 0

	# method to take photo  
    def click_photo(self): 

		# time stamp 
        # timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
		# capture the image and save it on the save path 
        
        
        # self.capture.capture(os.path.join(self.save_path, 'List.jpg'))
        
        
        # print(self.save_path)
        # image = self.viewfinder.grab()
        # image.save('List.jpg')
		# increment the sequence 
        # self.save_seq += 1
        # widget.setCurrentIndex(2)
        print("captured")
        # saveImg_event.set()
        # widget.widget(2).setImage()

        # QtWidgets.QApplication.processEvents()
    
    def released_photo(self):
        print("released")
        widget.widget(2).setImage()

	# method for alerts 
    def alert(self, msg): 

		# error message 
        error = QErrorMessage(self) 

		# setting text to the error message 
        error.showMessage(msg) 

    def returnHome(self):
        # self.pushButton.setStyleSheet("background-color: yellow;")
        print("back to home")
        widget.setCurrentIndex(0)

class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi("ShowImage.ui",self)
        self.HomeButton.clicked.connect(self.returnHome)
        self.Capture.clicked.connect(self.backtoCamera)
        self.Checked.clicked.connect(self.gotomap)

    def setImage(self):
        # saveImg_event.wait()
        print("image set")
        pixmap = QPixmap('List.jpg')
        pix_map = pixmap.scaled(400, 222, QtCore.Qt.KeepAspectRatio)
        self.Img.setPixmap(pix_map)
        widget.setCurrentIndex(2)
        self.repaint()
        # QtWidgets.QApplication.processEvents()

    def returnHome(self):
        print("back to home")
        widget.setCurrentIndex(0)

    def backtoCamera(self):
        print("back to camera")
        widget.setCurrentIndex(1)
    
    def gotomap(self):
        print("go to map list")
        del widget.widget(1).camera
        widget.widget(3).setList()
        widget.widget(3).update_label.start()
        widget.widget(3).thread_wifi.start()
        widget.setCurrentIndex(3)

class MapList(QWidget):
    def __init__(self):
        super().__init__()
        # super(MapList, self).__init__()
        loadUi("MapList.ui",self)
        # self.setGeometry(0,0,1024,600)
        self.pos = (0,0)
        self.realpos = (0,0)
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()
        self.scrollarea = QScrollArea()
        self.ShoppingCartButton = []
        self.ShoppingCartLabel = []
        self.ShoppingCartPoint = []

        self.pop_up_screen = QDialog(self)
        self.pop_up_screen.setWindowTitle('Something Wrong')
        self.pop_up_screen_layout = QVBoxLayout(self.pop_up_screen)
        # 添加标签、文本框和按钮到小窗口
        self.wrong_name = ""
        self.wrong_product_label = QLabel('辨識錯誤', self.pop_up_screen)
        self.wrong_product_inputbox = QLineEdit(self.pop_up_screen)
        self.wrong_product_button_check = QPushButton('輸入完成', self.pop_up_screen)
        self.wrong_product_button_abandon = QPushButton('放棄此項', self.pop_up_screen)
        self.wrong_product_button_abandon.clicked.connect(lambda:self.delItem(self.wrong_name))
        self.wrong_product_button_check.clicked.connect(self.changeItem)

        # 将标签、文本框和按钮添加到小窗口布局中
        self.pop_up_screen_layout.addWidget(self.wrong_product_label)
        self.pop_up_screen_layout.addWidget(self.wrong_product_inputbox)
        self.pop_up_screen_layout.addWidget(self.wrong_product_button_check)
        self.pop_up_screen_layout.addWidget(self.wrong_product_button_abandon)

        # 设置小窗口位置为窗口中心
        # self.pop_up_screen.move(round(512 - self.pop_up_screen.width() / 2), round(300 - self.pop_up_screen.height() / 2))
        self.pop_up_screen.move(self.geometry().center())# - self.pop_up_screen.rect().center())
        self.pop_up_screen.hide()


        hlay = QHBoxLayout(self)
        hlay.setContentsMargins(0,0,0,0)
        hlay.setSpacing(0)
        self.scrollarea.setContentsMargins(0,0,0,0)
        
        mapimg = QLabel()
        mapimg.setScaledContents(True)
        # pixmap = QPixmap('./img/4F平面圖_4aps.png')
        pixmap = QPixmap('./img/路徑地圖.jpg')
        pixmap_s = pixmap.scaled(433, 400, aspectRatioMode=Qt.KeepAspectRatio)
        mapimg.setPixmap(pixmap_s)
        hlay.addWidget(mapimg)
        hlay.addWidget(self.scrollarea)

        self.PosButton = QPushButton(self)
        self.PosButton.setStyleSheet("background-color:red;border-radius: 6px;")
        self.PosButton.setFixedSize(12,12)
        self.PosButton.move(156,550)
        self.PosButton.show()
        self.PosButton.clicked.connect(self.delList)

        self.RealPos = QPushButton(self)
        self.RealPos.setStyleSheet("background-color:blue;border-radius: 5px;")
        self.RealPos.setFixedSize(10,10)
        self.RealPos.move(156,550)
        self.RealPos.show()
        # self.Target = QLabel(self)
        # self.Target.setStyleSheet("background-color:rgba(245, 223, 77,0.7);font-size:20px;border:1px solid #000;border-radius: 15px;")
        # self.Target.setFixedSize(100,60)
        # self.Target.hide()
        # self.Target_point = QLabel(self)
        # self.Target_point.setStyleSheet("background-color:rgba(0,255,0,1);border-radius: 5px;")
        # self.Target_point.setFixedSize(10,10)
        # self.Target_point.hide()

        self.wait_pos = threading.Event()

        self.update_label = QThread()
        self.update_label.run = self.set_PosButton_pos
        self.update_label.wait
        # self.update_label.start()
        
        # self.update_pos = QThread()
        # self.update_pos.run = self.get_pos
        # self.update_pos.start()

        self.thread_wifi = QThread()
        self.thread_wifi.run = self.get_wifi_pos
        # self.thread_wifi.start()

    def get_wifi_pos(self):
        index = 103
        orientation = 1
        while(1):
            time.sleep(0.05)
            # self.pos = (15,15)
            # self.label.setText(",100")
            # print("wifi:15,15")
            POS = WiFi.scan_wifi_position(index)
            # POS = [[10,10],[10,10]]
            # print("POS:", POS)
            self.pos = POS[0]
            self.realpos = POS[0]
            index = index + orientation
            if (index > 654 or index < 1):
                orientation = -orientation
            self.wait_pos.set()

    def get_pos(self):
        while(1):
            time.sleep(0.1)
            self.pos = (self.pos[0]+1,self.pos[1])
            if (self.pos[0] > 31):
                self.pos = (0,self.pos[1] + 1)
                # self.pos[1] = self.pos[1] + 1
            if (self.pos[1] > 30):
                self.pos = (0,0)
            self.wait_pos.set()

    def set_PosButton_pos(self):
        while(1):
            self.wait_pos.wait()
            x = round(self.pos[0] * SCALE_MAP)
            y = 400-round(self.pos[1] * SCALE_MAP)
            self.PosButton.move(x,y-10)
            self.PosButton.hide()

            x2 = round(self.realpos[0] * SCALE_MAP)
            y2 = 400-round(self.realpos[1] * SCALE_MAP)
            self.RealPos.move(x2,y2-10)
            self.RealPos.show()

    def delItem(self,name:str):
        for item in maplist.ShoppingCartButton:
            if item.text() == name:
                self.delList(item)
                self.pop_up_screen.hide()
                self.wrong_name = ""

    def delList(self,item):
        maplist.formLayout.removeRow(item)
        maplist.ShoppingCartButton.remove(item)
        # print(maplist.ShoppingCartButton)
        print("delList fin")

    def changeItem(self):
        new_name = self.wrong_product_inputbox.text()
        [shelf, keyword] = Temp.find_shelf_with_keywords(product_name=new_name)
        [x, y, label] = Temp.find_shelf_position(shelf, keyword)
        if label != -1:
            for item in maplist.ShoppingCartButton:
                if item.text() == self.wrong_name:
                    item.setText(new_name)
                    item.pos = (x,y)
                    item.isnotclass = label
                    item.shelf = shelf
                    item.setStyleSheet("background-color:#939597;font-size:14px;color:#000000;")
            self.pop_up_screen.hide()
        else:
            self.wrong_product_label.setText("辨識商品:"+new_name+"可能有誤，請輸入正確內容或是放棄此項")
        self.wrong_product_inputbox.clear()

    def setList(self):
        ShopingList = generate_List("List.png")
        self.ShoppingCartButton = []
        self.ShoppingCartLabel = []
        self.ShoppingCartPoint = []

        # self.verticalSpacer = QSpacerItem(0,0,QSizePolicy.Minimum, QSizePolicy.Expanding)
        for items in ShopingList:
            button = Item()
            button.setText(items[0])
            button.pos = (items[1],items[2])
            button.isnotclass = items[3]
            button.shelf = items[4]
            print("button pos:", button.pos)
            button.setStyleSheet("background-color:#939597;font-size:14px;color:#000000;")
            button.setFixedHeight(40)
            button.setFixedWidth(249)
            if (button.isnotclass == -1):
                button.setStyleSheet("background-color:rgba(230, 119, 98,1);font-size:14px;color:#000000;")
                button.setText("\""+items[0]+"\" 可能有誤")
            # button.clicked.connect(self.showitem)
            self.ShoppingCartButton.append(button)
            self.formLayout.addRow(button)
            # self.addBtn(button)

            target_point = QLabel(self)
            target_point.setStyleSheet("font-size:10px;background-color:rgba(0,255,0,1);border-radius: 5px;")
            target_point.setFixedSize(10,10)
            target_point.hide()
            self.ShoppingCartPoint.append(target_point)
            target = QLabel(self)
            target.setStyleSheet("font-size:10px;background-color:rgba(245, 223, 77,1);font-size:12px;border:1px solid #000;border-radius: 15px;")
            target.setFixedSize(68,40)
            target.setAlignment(Qt.AlignCenter)
            target.hide()
            self.ShoppingCartLabel.append(target)

        print(ShopingList)

        self.formLayout.setAlignment(Qt.AlignCenter)
        self.groupBox.setLayout(self.formLayout)
        self.scrollarea.setWidget(self.groupBox)


    def showitem(self:Item):
        # print(type(self))
        # print(self.pos)
        x = round(self.pos[0] * SCALE_MAP)#19.49
        y = 400-round(self.pos[1] * SCALE_MAP)#19.49
        isnotclass = self.isnotclass
        idx = maplist.ShoppingCartButton.index(self)
        if (maplist.ShoppingCartLabel[idx].isHidden()):
            maplist.ShoppingCartPoint[idx].move(x+2,y-2)
            maplist.ShoppingCartPoint[idx].show()
            maplist.ShoppingCartLabel[idx].move(x,y-maplist.ShoppingCartLabel[idx].height())
            maplist.ShoppingCartLabel[idx].setText(self.text())
            maplist.ShoppingCartLabel[idx].show()
            if (isnotclass == 0):
                maplist.ShoppingCartLabel[idx].setText(self.text()+"\n可能在"+self.shelf)
                maplist.ShoppingCartPoint[idx].setStyleSheet("background-color:rgba(0,255,0,0.3);border-radius: 10px;border:1px solid #000")
                if (self.shelf == "飲料"):
                    maplist.ShoppingCartPoint[idx].setFixedSize(round(123*4/6),round(182*4/6))
                elif (self.shelf == "酒類"):
                    maplist.ShoppingCartPoint[idx].setFixedSize(round(123*4/6),round(182*4/6))
                elif (self.shelf == "南北貨"):
                    maplist.ShoppingCartPoint[idx].setFixedSize(round(306*4/6),round(173*4/6))
                elif (self.shelf == "調味料"):
                    maplist.ShoppingCartPoint[idx].setFixedSize(round(123*4/6),round(182*4/6))
                elif (self.shelf == "營養品"):
                    maplist.ShoppingCartPoint[idx].setFixedSize(round(306*4/6),round(186*4/6))
                elif (self.shelf == "清潔用品"): 
                    maplist.ShoppingCartPoint[idx].setFixedSize(round(306*4/6),round(186*4/6))
                elif (self.shelf == "冷藏/凍食品"):
                    maplist.ShoppingCartPoint[idx].setFixedSize(round(107*4/6),round(271*4/6))
                elif (self.shelf == "休閒食品"): 
                    maplist.ShoppingCartPoint[idx].setFixedSize(round(107*4/6),round(239*4/6))
                else:
                    maplist.ShoppingCartPoint[idx].setFixedSize(0,0)
                new_x = round(x-maplist.ShoppingCartPoint[idx].width()/2)
                new_y = round(y-maplist.ShoppingCartPoint[idx].height()/2)
                maplist.ShoppingCartPoint[idx].move(new_x,new_y)
                maplist.ShoppingCartLabel[idx].move(round(x-maplist.ShoppingCartLabel[idx].width()/2),round(y-maplist.ShoppingCartLabel[idx].height()/2))
            if (isnotclass == -1): #找不到貨架 or 商品
                maplist.ShoppingCartLabel[idx].hide()
                maplist.ShoppingCartPoint[idx].hide()
                maplist.wrong_product_label.setText("辨識商品:"+self.text()+"可能有誤，請輸入正確內容或是放棄此項")
                maplist.wrong_name = self.text()
                maplist.pop_up_screen.show()
        else:
            maplist.ShoppingCartLabel[idx].hide()
            maplist.ShoppingCartPoint[idx].hide()

        # maplist.Target.move(x,y-maplist.Target.height())
        # maplist.Target.setText(self.text())
        # maplist.Target.show()
        # maplist.Target_point.move(x+2,y-2)
        # maplist.Target_point.show()

    def returnHome(self):
        print("back to home")
        widget.setCurrentIndex(0)

    # def backtoCamera(self):
    #     print("back to camera")
    #     widget.setCurrentIndex(1)




os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
mainwindow = MainWindow()
camerascreen = CameraScreen()
showimage = ShowImage()
maplist = MapList()
widget.addWidget(mainwindow)
widget.addWidget(camerascreen)
widget.addWidget(showimage)
widget.addWidget(maplist)
widget.setFixedHeight(400)
widget.setFixedWidth(682)
widget.show()
QApplication.processEvents()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")