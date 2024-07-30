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
import resource_rc
import WiFi_function as WiFi
import GoogleAPI_function
import Temp
from astsp import TspSolver
import keyboard
import pandas as pd

Scale_map = 13 #19.49

tsp_solver = TspSolver()

class Item(QPushButton):
    signal_show = QtCore.pyqtSignal()
    def __init__(self):
        super(Item,self).__init__()
        self.checkBtn = QPushButton(self)
        self.checkBtn.setStyleSheet("border-radius: 0px;background-color:rgba(245, 200, 77,1);")
        self.checkBtn.setGeometry(10,10,12,12)
        self.checkBtn.setIcon(QIcon("img/checked"))
        self.checkBtn.setIconSize(QtCore.QSize(12,12))
        self.right = 1
        self.pos = (0,0)
        self.isnotclass = 0
        self.shelf = ""
        self.clicked.connect(lambda:MapList.clickItem(self))
        self.signal_show.connect(lambda:MapList.showitem(self))

def get_sorted_list(self, cur_pos: tuple[int, int], name_list :tuple[str]) -> list[str]:
    # print(cur_pos)
    # print(name_list)
    # newlist = name_list
    newlist = []
    for idx in range(1,len(name_list)):
        newlist.append(name_list[idx])
    newlist.append(name_list[0])
    return newlist

def generate_List(file_name):
    #generate shopping list
    # text = GoogleAPI_function.detect_text("./List.jpg", GoogleAPI_function.api_key)
    # print(text)
    # text = "咖啡\n威士忌\n麵粉\n油\n維他命\n紙巾\n豆腐\n餅乾\n米\n牛奶\n大象\n"
    text = "茶\n啤酒\n米\n衛生紙\n堅果"#\n洋芋片"
    # text = "茶\n米\n衛生紙\n堅果"#\n洋芋片"
    # targets = [
    #     "茶",
    #     "啤酒",
    #     "米",
    #     "醬",
    #     "雞精",
    #     "衛生紙",
    #     "牛奶",
    #     "巧克力",
    #     "堅果",
    #     "飲料",
    #     "酒類",
    #     "南北貨",
    #     "調味料",
    #     "營養品",
    #     "清潔用品",
    #     "冷藏/凍食品",
    #     "休閒食品"
    # ]
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

def check_login(account:str,password:str) -> int:
    # 0 => wrong account or password, 1 => success, 2 => The account doesn't exist
    data = pd.read_csv('Account.csv',dtype=str)
    # print(data['Account'][0:len(data['Account'])])
    account_row = data[data['Account'] == account]
    if account_row.empty:
        return 2 #'查無此帳號'
    print(account_row.iloc[0]['Password'])
    # 檢查密碼
    if account_row.iloc[0]['Password'] == password:
        return 1 #'登入成功'
    else:
        return 0 #'密碼錯誤'

def check_register(account:str, password:str, email:str) -> bool:
    # 0 => account already exists, 1 => success 
        # 讀取CSV文件，確保所有數據都是字符串型別
    try:
        df = pd.read_csv('Account.csv', dtype=str)
    except FileNotFoundError:
        # 如果文件不存在，創建一個空的DataFrame
        df = pd.DataFrame(columns=['Account', 'Password'])

    # 查找帳號
    if account in df['Account'].values:
        return 0 #'已註冊'

    # 如果帳號不存在，添加新的帳號和密碼
    new_entry = pd.DataFrame({'Account': [account], 'Password': [password]})
    df = pd.concat([df, new_entry], ignore_index=True)

    # 將更新後的DataFrame寫回到CSV文件
    df.to_csv('Account.csv', index=False)

    return 1 #'註冊成功'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("MainWindow.ui",self)
        self.pushButton.clicked.connect(self.changescreen)
        self.LoginBtn.clicked.connect(self.loginscreen)

    def changescreen(self):
        # self.pushButton.setStyleSheet("background-color: yellow;")
        print("Clicked")
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def loginscreen(self):
        # self.pushButton.setStyleSheet("background-color: yellow;")
        widget.setCurrentIndex(widget.currentIndex()+4)

class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("Login.ui",self)
        self.HomeButton.clicked.connect(self.returnHome)
        self.loginBtn.clicked.connect(self.loginclick)
        self.go2registerBtn.clicked.connect(self.change2register)
        self.registerBtn.clicked.connect(self.registerclick)
        self.go2login.clicked.connect(self.change2login)
        self.back2loginBtn.clicked.connect(self.change2login)
        self.name = "guest"

    def loginclick(self):
        if (self.account_input.text() != "" and self.password_input.text() != ""):
            check_login_result = check_login(self.account_input.text(),self.password_input.text())
            if (check_login_result == 1):
                print("account:", self.account_input.text())
                print("password:", self.password_input.text())
                print("login!")
                self.name = self.account_input.text()
                self.message.setText("")
                widget.setCurrentIndex(1) #拍照
            elif (check_login_result == 2):
                print("The account doesn't exist.")
                self.message.setText("帳號不存在")
            else:
                print("wrong account or wrong password")
                self.message.setText("帳號或密碼錯誤")

    def registerclick(self):
        if (self.account_input_2.text != " " and self.password_input_2.text() != " " and self.email_input.text() != ""):
            if (check_register(self.account_input_2.text(),self.password_input_2.text(),self.email_input.text())):
                print("registration is complete!")
                print("account:", self.account_input_2.text())
                print("password:", self.password_input_2.text())
                print("email: ", self.email_input.text())
                self.stackedWidget.setCurrentIndex(2) # registraction success
            else:
                print("This account already exists.")
                self.message_2.setText("此帳號已註冊")
    
    def change2register(self):
        self.stackedWidget.setCurrentIndex(1)

    def change2login(self):
        self.stackedWidget.setCurrentIndex(0)

    def returnHome(self):
        # self.pushButton.setStyleSheet("background-color: yellow;")
        print("back to home")
        widget.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)
        self.account_input.clear()
        self.password_input.clear()
        self.account_input_2.clear()
        self.password_input_2.clear()
        self.email_input.clear()
        self.message.clear()
        self.message_2.clear()

    def isLogin(self):
        return self.name != "guest"

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
        # widget.widget(3).update_label.start()
        widget.widget(3).thread_wifi.start()
        # widget.widget(3).set_path()
        # widget.widget(3).thread_update_list.start()
        widget.setCurrentIndex(3)

class MapList(QWidget):
    signal_set_path = QtCore.pyqtSignal()
    update_label = QtCore.pyqtSignal()
    update_map = QtCore.pyqtSignal()

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
        self.rightLayout = QVBoxLayout()
        self.leftLayout = QVBoxLayout()
        # self.nearproductwidget = NearProduct()
        self.ShoppingCartButton = []
        self.ShoppingCartBuyed = []
        self.ShoppingCartLabel = []
        self.ShoppingCartPoint = []
        self.path_label = []
        self.path_point = []

        self.nearproductwidget = QWidget()
        self.NPvlay = QVBoxLayout()
        self.NPvlay.setContentsMargins(10,10,10,10)
        self.NPvlay.setSpacing(0)
        self.NPbutton = QPushButton("買到了！")
        self.NPbutton.setFixedHeight(30)
        self.NPbutton.setStyleSheet("background-color:#939597;font-size:14px;color:#000000;border-radius:6px")
        self.NPlabel = QLabel(text="您附近有：")
        self.NPlabel.setStyleSheet("font-size:14px;")#background-color:#939597;border-radius:6px")
        # self.NPlabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.nearproduct = "茶"
        self.nearproductlabel = QLabel(text=self.nearproduct)
        self.nearproductlabel.setStyleSheet("font-size:30px;")#background-color:#939597;border-radius:6px")
        self.nearproductlabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.NPlabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.NPvlay.addWidget(self.NPlabel,1)
        self.NPvlay.addWidget(self.nearproductlabel,4)
        self.NPvlay.addWidget(self.NPbutton,1)
        # self.NPvlay.setAlignment(Qt.AlignCenter)
        self.nearproductwidget.setLayout(self.NPvlay)
        self.nearproductwidget.setStyleSheet("border-radius: 0px;background-color:rgba(245, 200, 77,1);")
        self.show_item = None
        #按下買到了就刪除此物件。
        self.NPbutton.clicked.connect(lambda:self.delItem(self.nearproduct))


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

        self.hlay = QHBoxLayout(self)
        self.hlay.setContentsMargins(0,0,0,0)
        self.hlay.setSpacing(0)
        self.scrollarea.setContentsMargins(0,0,0,0)
        
        self.mapimg = QLabel()
        self.mapimg.setScaledContents(True)
        self.pixmap = QPixmap('./img/4F平面圖_4aps.png')
        # pixmap = QPixmap('./img/路徑地圖.jpg')
        pixmap_s = self.pixmap.scaled(433, 400, aspectRatioMode=Qt.KeepAspectRatio)
        self.mapimg.setPixmap(pixmap_s)

        self.scene = QGraphicsScene()
        self.scene.addWidget(self.mapimg)
        
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.leftLayout.addWidget(self.view)

        # self.leftLayout.addWidget(self.mapimg)
        
        self.showingFullImage = True
        # self.leftLayout.addWidget(self.mapbutton)

        # self.map_widget = MapWidget()
        # self.leftLayout.addWidget(self.map_widget)

        self.hlay.addLayout(self.leftLayout)
        self.rightLayout.addWidget(self.scrollarea,2)
        # self.rightLayout.addLayout(self.NPvlay,1)
        self.rightLayout.addWidget(self.nearproductwidget,1)
        # rightLayout.addLayout(textButtonLayout)
        # self.hlay.addWidget(self.scrollarea)
        self.hlay.addLayout(self.rightLayout)

        self.PosButton = QPushButton(self)
        self.PosButton.setStyleSheet("background-color:red;border-radius: 6px;")
        self.PosButton.setFixedSize(12,12)
        self.PosButton.move(156,550)
        self.PosButton.show()
        # self.PosButton.clicked.connect(self.delList)

        self.RealPos = QPushButton()
        self.RealPos.setStyleSheet("background-color:blue;border-radius: 5px;")
        self.RealPos.setFixedSize(10,10)
        self.RealPos.move(156,550)
        self.RealPos.show()
        self.scene.addWidget(self.RealPos)

        self.mapbutton = QPushButton(self)
        self.mapbutton.setGeometry(375,10,30,30)
        self.mapbutton.setStyleSheet("background-color:None;border-radius:0px;")
        self.mapbutton.clicked.connect(self.togglemapView)
        self.mapbutton.setIcon(QIcon('./img/zoom-in.png'))
        self.mapbutton.setIconSize(QtCore.QSize(30,30))
        # self.Target = QLabel(self)
        # self.Target.setStyleSheet("background-color:rgba(245, 223, 77,0.7);font-size:20px;border:1px solid #000;border-radius: 15px;")
        # self.Target.setFixedSize(100,60)
        # self.Target.hide()
        # self.Target_point = QLabel(self)
        # self.Target_point.setStyleSheet("background-color:rgba(0,255,0,1);border-radius: 5px;")
        # self.Target_point.setFixedSize(10,10)
        # self.Target_point.hide()

        # self.wait_pos = threading.Event()
        # self.wait_list = threading.Event()
        # self.set_path_signal = threading.Event()
        # self.lock = threading._RLock()

        # self.update_label = QThread()
        # self.update_label.run = self.set_PosButton_pos
        # self.update_label.wait
        # self.update_label.start()
        
        # self.update_pos = QThread()
        # self.update_pos.run = self.get_pos
        # self.update_pos.start()

        self.thread_wifi = QThread()
        self.thread_wifi.run = self.get_wifi_pos
        # self.thread_wifi.start()

        # self.thread_update_list = QThread()
        # self.thread_update_list.run = self.update_list

        # self.signal_set_path = QtCore.pyqtSignal()
        # self.signal_set_path.connect(self.set_path)
        self.signal_set_path.connect(self.update_list)
        self.update_label.connect(self.set_PosButton_pos)
        self.update_map.connect(self.change_map_view)

    def change_map_view(self):
        # self.fullImage = self.pixmap.scaled(433, 400, aspectRatioMode=Qt.KeepAspectRatio)
        # x = int(self.pos[0] * 13 * 3 - 433 / 2)
        # if x < 0 :
        #     x = 0
        # if x > 1232:
        #     x = 1232
        # y = 1334 - int(self.pos[1] * 13 * 3) - 200
        # if y < 0 :
        #     y = 0
        # if y > 1334:
        #     y = 1334
        # self.partialImage = self.pixmap.copy(QRect(x, y, 433, 400))
        # if self.showingFullImage:
        #     self.mapimg.setPixmap(self.fullImage)
        #     Scale_map = 13
        # else:
        #     self.mapimg.setPixmap(self.partialImage)
        #     Scale_map = 13/3
        if self.showingFullImage:
            self.view.resetTransform()
            self.view.centerOn(0,0)
            self.mapbutton.setIcon(QIcon('./img/zoom-in.png'))
        else:
            self.mapbutton.setIcon(QIcon('./img/full-screen.png'))
            self.view.resetTransform()
            x = round(self.pos[0] * Scale_map)
            y = 400-round(self.pos[1] * Scale_map)
            self.view.centerOn(x,y)
            self.view.scale(1.5, 1.5)

    def togglemapView(self):
        # self.fullImage = self.pixmap.scaled(433, 400, aspectRatioMode=Qt.KeepAspectRatio)
        # self.partialImage = self.pixmap.copy(QRect(200, 200, 433, 400))
        # if self.showingFullImage:
        #     self.mapimg.setPixmap(self.partialImage)
        #     Scale_map = 13/3
        # else:
        #     self.mapimg.setPixmap(self.fullImage)
        #     Scale_map = 13

        # if self.showingFullImage:
        #     self.view.resetTransform()
        # else:
        #     self.view.resetTransform()
        #     x = round(self.pos[0] * Scale_map)
        #     y = 400-round(self.pos[1] * Scale_map)
        #     self.view.centerOn(x,y)
        #     self.view.scale(1.5, 1.5)
        self.showingFullImage = not self.showingFullImage
        self.update_map.emit()

    def get_wifi_pos(self):
        index = 0
        orientation = 1
        while(1):
            time.sleep(0.5)
            # self.pos = (15,15)
            # self.label.setText(",100")
            # print("wifi:15,15")
            POS = WiFi.scan_wifi_position(index)
            # POS = [[10,10],[10,10]]
            # print("POS:", POS)
            self.pos = POS[0]
            self.realpos = POS[0]
            index = (index + orientation)%92
            # if (index > 654 or index < 1):
                # orientation = -orientation
            
            # name_list = [btn.text() for btn in self.ShoppingCartButton]
            # self.update_list(get_sorted_list(self,self.pos,name_list))
            # self.update_list()
            # self.wait_pos.set()
            self.update_label.emit()
            
            if self.ShoppingCartButton:
                self.signal_set_path.emit()
            else:
                if self.formLayout.rowCount() != len(self.ShoppingCartBuyed):
                    btn = self.ShoppingCartBuyed[-1]
                    btn.setStyleSheet("background-color:#DDDDDD;font-size:14px;color:#000000;text-decoration:line-through;")
                    self.formLayout.addRow(btn)
                self.clear_path()
                self.clear_nearproduct()
            # self.wait_list.set()

            self.update_map.emit()

    def set_PosButton_pos(self):
        # while(1):
        #     # self.wait_pos.wait()
        #     x = round(self.pos[0] * Scale_map)
        #     y = 400-round(self.pos[1] * Scale_map)
        #     self.PosButton.move(x,y-10)
        #     self.PosButton.hide()

        #     x2 = round(self.realpos[0] * Scale_map)
        #     y2 = 400-round(self.realpos[1] * Scale_map)
        #     self.RealPos.move(x2,y2-10)
        #     self.RealPos.show()
        print("Set Pos Label!!")
        x = round(self.pos[0] * Scale_map)
        y = 400-round(self.pos[1] * Scale_map)
        self.PosButton.move(x-5,y-5)
        self.PosButton.hide()
        x2 = round(self.realpos[0] * Scale_map)
        y2 = 400-round(self.realpos[1] * Scale_map)
        # if self.showingFullImage:
        #     x2 = round(self.realpos[0] * Scale_map)
        #     y2 = 400-round(self.realpos[1] * Scale_map)
        # else:
        #     x2 = int(433 / 2)
        #     y2 = 200
        self.RealPos.move(x2-5,y2-5)
        self.RealPos.show()

    def delItem(self,name:str):
        for item in self.ShoppingCartButton:
            if item.text() == name:
                if item.text() == self.nearproduct:
                    self.show_item = None
                    maplist.NPlabel.setText("您附近有：")
                self.delList(item)
                self.pop_up_screen.hide()
                self.wrong_name = ""

    def delList(self,item):
        idx = self.ShoppingCartButton.index(item)
        # self.formLayout.removeRow(item)
        self.formLayout.takeAt(idx)
        # print(self.ShoppingCartButton.pop(idx).text())
        self.ShoppingCartBuyed.append(self.ShoppingCartButton.pop(idx))
        # self.ShoppingCartBuyed.append(item)
        # self.ShoppingCartButton.remove(item)
        self.ShoppingCartPoint[idx].hide()
        self.ShoppingCartLabel[idx].hide()
        self.ShoppingCartPoint.pop(idx)
        self.ShoppingCartLabel.pop(idx)
        self.name_list = [btn.text() for btn in self.ShoppingCartButton]
        # print(maplist.ShoppingCartButton)
        print("delList fin")
        # for btn in self.ShoppingCartBuyed:
        #     print("Buyed",btn.text())

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
            button.setFixedWidth(210)
            if (button.isnotclass == -1):
                button.setStyleSheet("background-color:rgba(230, 119, 98,1);font-size:14px;color:#000000;")
                button.setText("\""+items[0]+"\" 可能有誤")
            # button.clicked.connect(self.showitem)
            self.ShoppingCartButton.append(button)
            self.formLayout.addRow(button)
            # self.addBtn(button)

            target_point = QLabel(self.mapimg)
            target_point.setStyleSheet("font-size:10px;background-color:rgba(0,255,0,1);border-radius: 5px;")
            target_point.setFixedSize(10,10)
            target_point.hide()
            self.ShoppingCartPoint.append(target_point)
            target = QLabel(self.mapimg)
            target.setStyleSheet("font-size:10px;background-color:rgba(245, 223, 77,1);font-size:12px;border:1px solid #000;border-radius: 15px;")
            target.setFixedSize(68,40)
            target.setAlignment(Qt.AlignCenter)
            target.hide()
            self.ShoppingCartLabel.append(target)

        print(ShopingList)

        self.formLayout.setAlignment(Qt.AlignCenter)
        self.groupBox.setLayout(self.formLayout)
        self.scrollarea.setWidget(self.groupBox)

    def update_list(self):
        print("update list!!!")
        if not self.ShoppingCartButton:
            if self.formLayout.rowCount() == self.ShoppingCartBuyed.count():
                return
            else:
                btn = self.ShoppingCartBuyed[-1]
                self.formLayout.addRow(btn)

        # while(1):
        # time.sleep(0.5)
        # self.wait_list.wait()
        self.name_list = [btn.text() for btn in self.ShoppingCartButton]
        new_order = tsp_solver.get_sorted_list(self.pos,self.name_list)
        # if self.nearproduct:
            # self.signal_set_path.emit()
            # self.set_path()
            # self.set_path_signal.set()
        # print("new:", new_order)
        # Create a dictionary for quick lookup of buttons by text
        button_dict = {btn.text(): btn for btn in self.ShoppingCartButton}
        # print(button_dict)
        # Reorder the shoppingCartButton list according to new_order
        self.ShoppingCartButton = [button_dict[text] for text in new_order]
        # Clear the form layout
        while self.formLayout.count():
            item = self.formLayout.takeAt(0)
            widget = item.widget()
            if widget:
                # widget.deleteLater()
                widget.setParent(None)
            # print(self.ShoppingCartButton)
        # Add buttons back to the form layout in new order
        # self.lock.acquire()

        for btn in self.ShoppingCartButton:
            self.formLayout.addRow(btn)
        

        for btn in self.ShoppingCartBuyed:
            # print("Buyed",self.ShoppingCartBuyed)
            btn.setStyleSheet("background-color:#DDDDDD;font-size:14px;color:#000000;text-decoration:line-through;")
            self.formLayout.addRow(btn)
        # self.lock.release()

        # set_near_product
        self.set_nearproduct()
        self.set_path()

    def clear_path(self):
        for label in self.path_label:
            label.deleteLater()
        for points in self.path_point:
            points.deleteLater()
        self.path_label = []
        self.path_point = []

    def clear_nearproduct(self):
        self.nearproduct = ""
        self.nearproductlabel.setText(self.nearproduct)
        self.nearproductlabel.show()

    def set_nearproduct(self):
        if self.show_item:
            idx = self.ShoppingCartButton.index(self.show_item)
        else:
            idx = 0
        # if self.show_idx == -1:
        #     idx = 0
        # else:
        #     idx = self.show_idx
        self.nearproduct = self.ShoppingCartButton[idx].text()
        self.nearproductlabel.setText(self.nearproduct)
        self.nearproductlabel.show()
        self.ShoppingCartButton[idx].signal_show.emit()

    def set_path(self):
        print("Set Path!!!!!")
        self.clear_path()
        path = tsp_solver.get_path(self.pos,self.nearproduct)
        # print(self.pos[0],self.pos[1])
        # print(path)
        for idx in range(0,len(path)-1):
            line = QLabel(self.mapimg)
            point = QLabel(self.mapimg)
            line.setStyleSheet("background-color:rgba(230, 119, 98,1);border:1px solid #000;")
            point.setStyleSheet("background-color:rgba(250, 250, 0,1);border:1px solid #000;border-radius:4px;")
            x1 = int(round(path[idx][0])* Scale_map)
            x2 = int(round(path[idx+1][0])* Scale_map)
            y1 = 400-int(round(path[idx][1])* Scale_map)
            y2 = 400-int(round(path[idx+1][1])* Scale_map)    
            #橫線，第一個點在左邊
            if (x1 > x2): 
                tmp = x1
                x1 = x2
                x2 = tmp
            #直線，第一個點在上面
            if (y1 > y2): # y軸是從上往下
                tmp = y1
                y1 = y2
                y2 = tmp

            if (x1 != x2):
                w = x2 - x1
                h = 8
                x = x1 
                y = y1 -4
            else:
                w = 8
                h = y2 - y1
                x = x1 - 4
                y = y1
            # print(x,y,w,h)
            line.setGeometry(x,y,w,h)
            point.setGeometry(x1-4,y1-4,8,8)
            # self.leftLayout.addWidget(line)
            self.path_label.append(line)
            self.path_point.append(point)
            line.show()
            point.show()
            
    def showitem(self:Item):
        # print(type(self))
        # print(self.pos)
        x = round(self.pos[0] * Scale_map)#19.49
        y = 400-round(self.pos[1] * Scale_map)#19.49
        isnotclass = self.isnotclass
        idx = maplist.ShoppingCartButton.index(self)
        if (maplist.ShoppingCartLabel[idx].isHidden() or (maplist.show_item == self) or (maplist.show_item == None and idx == 0)):
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
            self.setStyleSheet("background-color:rgba(245, 200, 77,1);font-size:14px;color:#000000;")
            for btn in maplist.ShoppingCartButton:
                if btn != self:
                    btn.setStyleSheet("background-color:#939597;font-size:14px;color:#000000;")
        else:
            maplist.ShoppingCartLabel[idx].hide()
            maplist.ShoppingCartPoint[idx].hide()
            self.setStyleSheet("background-color:#939597;font-size:14px;color:#000000;")

    def clickItem(self:Item):
        if(self not in maplist.ShoppingCartButton):
            return

        if maplist.show_item == self: ##關掉
            # self.setStyleSheet("background-color:#939597;font-size:14px;color:#000000;")
            # maplist.ShoppingCartButton[0].setStyleSheet("background-color:rgba(245, 200, 77,1);font-size:14px;color:#000000;")
            maplist.show_item = None
            idx = maplist.ShoppingCartButton.index(self)
            if (not maplist.ShoppingCartLabel[idx].isHidden()):
                self.signal_show.emit()
            maplist.NPlabel.setText("您附近有：")
        else: ## 換成現在的
            # self.setStyleSheet("background-color:rgba(245, 200, 77,1);font-size:14px;color:#000000;")
            maplist.NPlabel.setText("您想找的商品：")
            if maplist.show_item:
                idx = maplist.ShoppingCartButton.index(maplist.show_item)
                # maplist.show_item.setStyleSheet("background-color:#939597;font-size:14px;color:#000000;")
            else:
                # maplist.ShoppingCartButton[0].setStyleSheet("background-color:#939597;font-size:14px;color:#000000;")
                idx = 0
            maplist.show_item = self
            if maplist.ShoppingCartButton.index(self) == 0:
                print("idx == 0")
                maplist.NPlabel.setText("您附近有：")
            if (not maplist.ShoppingCartLabel[idx].isHidden()):
                maplist.ShoppingCartButton[idx].signal_show.emit()
        # for idx in range(0,len(maplist.ShoppingCartButton)):
        #     if maplist.ShoppingCartButton[idx].text() == self.text():
        #         if maplist.nearproduct == self.text() and maplist.show_idx != -1:
        #             maplist.show_idx = -1
        #         elif maplist.show_idx == -1 and idx != 0:
        #             maplist.show_idx = idx
        # print(maplist.show_idx)
        maplist.set_nearproduct()

    def returnHome(self):
        print("back to home")
        widget.setCurrentIndex(0)



os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
widget.setStyleSheet("background-color: rgb(245, 223, 77);border-radius: 15px;")
mainwindow = MainWindow()
camerascreen = CameraScreen()
showimage = ShowImage()
maplist = MapList()
login = Login()
widget.addWidget(mainwindow)
widget.addWidget(camerascreen)
widget.addWidget(showimage)
widget.addWidget(maplist)
widget.addWidget(login)
widget.setFixedHeight(400)
widget.setFixedWidth(682)
widget.show()
QApplication.processEvents()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")