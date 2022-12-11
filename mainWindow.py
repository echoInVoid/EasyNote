import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from settings import settings


class UIMainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QWidget):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(*settings.welcomeWindowSize)

        self.layout = QtWidgets.QVBoxLayout(self.MainWindow)
        self.layout.setObjectName("layout")
        self.layout.setContentsMargins(*settings.windowContentMargin)
        MainWindow.setLayout(self.layout)

        #timer
        self.timer = QtCore.QTimer(self.MainWindow)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start()
        
        # layout of welcome
        self.welcome = QtWidgets.QHBoxLayout(self.MainWindow)
        self.welcome.setObjectName("welcome")
        self.layout.addLayout(self.welcome)

        #welcome text
        self.welcomeText = QtWidgets.QLabel(self.MainWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.welcomeText.setFont(font)
        self.welcomeText.setWhatsThis("")
        self.welcomeText.setTextFormat(QtCore.Qt.RichText)
        self.welcomeText.setScaledContents(False)
        self.welcomeText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.welcomeText.setIndent(4)
        self.welcomeText.setMaximumHeight(70)
        self.welcomeText.setObjectName("welcomeText")
        self.welcome.addWidget(self.welcomeText)

        #clock
        self.time = QtWidgets.QLCDNumber(self.MainWindow)
        self.time.setObjectName("time")
        self.time.setDigitCount(8)
        self.time.setMaximumHeight(70)
        self.updateClock()
        self.welcome.addWidget(self.time)

        #welcome picture
        self.welcomePic = QtWidgets.QLabel(self.MainWindow)
        self.welcomePic.setText("")
        self.welcomePic.setPixmap(QtGui.QPixmap(".\\resource\\welcome.gif"))
        self.welcomePic.setScaledContents(True)
        self.welcomePic.setObjectName("welcomePic")
        self.welcomePic.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(self.welcomePic)

        # control layout
        self.buttons = QtWidgets.QHBoxLayout()
        self.buttons.setObjectName("buttons")
        self.layout.addLayout(self.buttons)

        #help button
        self.helpButton = QtWidgets.QPushButton(self.MainWindow)
        self.helpButton.setObjectName("helpButton")
        self.buttons.addWidget(self.helpButton)
        self.helpButton.clicked.connect(self.openHelp)

        #exit button
        self.exitButton = QtWidgets.QPushButton(self.MainWindow)
        self.exitButton.setObjectName("exitButton")
        self.buttons.addWidget(self.exitButton)
        self.exitButton.clicked.connect(QtWidgets.QApplication.instance().quit)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "EasyNote简单笔记"))
        self.welcomeText.setText(_translate("MainWindow", "欢迎!"))
        self.exitButton.setText(_translate("MainWindow", "退出"))
        self.helpButton.setText(_translate("MainWindow", "帮助"))

    def updateClock(self):
        self.time.display(time.strftime("%H:%M:%S"))

    def openHelp(self):
        if os.path.isfile('..\\readme.html'):
            os.system("..\\readme.html")