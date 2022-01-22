# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4


import time
from PyQt5 import QtCore, QtGui, QtWidgets
import myOperations as oper


class UIMainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.MainWindow.setCentralWidget(self.centralwidget)

        #timer
        self.timer = QtCore.QTimer(self.MainWindow)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start()
        
        #clock
        self.time = QtWidgets.QLCDNumber(self.centralwidget)
        self.time.setObjectName("time")
        self.time.setDigitCount(8)
        self.updateClock()
        self.gridLayout.addWidget(self.time, 0, 1, 1, 1)

        #welcome text
        self.welcomeText = QtWidgets.QLabel(self.centralwidget)
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
        self.welcomeText.setObjectName("welcomeText")
        self.gridLayout.addWidget(self.welcomeText, 0, 0, 1, 1)

        #welcome picture
        self.welcomePic = QtWidgets.QLabel(self.centralwidget)
        self.welcomePic.setText("")
        self.welcomePic.setPixmap(QtGui.QPixmap("ui\\../resource/welcome.gif"))
        self.welcomePic.setObjectName("welcomePic")
        self.gridLayout.addWidget(self.welcomePic, 1, 0, 1, 2)

        #menubar
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 23))
        self.menubar.setObjectName("menubar")
        #main
        self.main = QtWidgets.QMenu(self.menubar) #main page (1st menu)
        self.main.setObjectName("main")
        self.menubar.addAction(self.main.menuAction())
        #file
        self.file = QtWidgets.QMenu(self.menubar) #about file (1st menu)
        self.file.setObjectName("file")
        self.importf = QtWidgets.QAction(self.MainWindow) #import note from file
        self.importf.setObjectName("importf")
        #TODO: let user be able to import notes from file/folder
        self.file.addAction(self.importf)
        self.menubar.addAction(self.file.menuAction())
        #edit
        self.edit = QtWidgets.QMenu(self.menubar) #edit note (1st menu)
        self.edit.setObjectName("edit")
        self.create = QtWidgets.QAction(self.MainWindow) #create note
        self.create.setObjectName("create")
        self.create.triggered.connect(oper.write)
        self.edit.addAction(self.create)
        self.view = QtWidgets.QAction(self.MainWindow) #view all notes
        self.view.setObjectName("view")
        #TODO: let user be able to view all notes
        self.edit.addAction(self.view)
        self.menubar.addAction(self.edit.menuAction())
        #set as menubar
        self.MainWindow.setMenuBar(self.menubar)

        #status bar
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        #help button
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpButton.setObjectName("helpButton")
        self.gridLayout.addWidget(self.helpButton, 2, 0, 1, 1)
        # self.helpButton.clicked.connect() #TODO: write a help file

        #exit button
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setObjectName("exitButton")
        self.gridLayout.addWidget(self.exitButton, 2, 1, 1, 1)
        self.exitButton.clicked.connect(QtWidgets.QApplication.instance().quit)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "EasyNote"))
        self.welcomeText.setText(_translate("MainWindow", "欢迎!"))
        self.main.setTitle(_translate("MainWindow", "主页"))
        self.edit.setTitle(_translate("MainWindow", "编辑"))
        self.file.setTitle(_translate("MainWindow", "文件"))
        self.create.setText(_translate("MainWindow", "创建笔记"))
        self.view.setText(_translate("MainWindow", "浏览笔记"))
        self.importf.setText(_translate("MainWindow", "导入笔记"))
        self.exitButton.setText(_translate("MainWindow", "退出"))
        self.helpButton.setText(_translate("MainWindow", "帮助"))

    def updateClock(self):
        self.time.display(time.strftime("%H:%M:%S"))
