# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/viewAll.ui'
#
# Created by: PyQt5 UI code generator 5.15.4


from re import search
from PyQt5 import QtCore, QtGui, QtWidgets
import myOperations as oper


class UI_viewAllWidget(object):
    def setupUi(self, Widget):
        self.Widget = Widget
        self.Widget.setObjectName("Widget")
        self.Widget.resize(760, 600)

        #layout
        self.centralWidget = QtWidgets.QWidget(self.Widget)
        self.centralWidget.setGeometry(QtCore.QRect(20, 20, 711, 551))
        self.centralWidget.setObjectName("centralWidget")
        self.layout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setObjectName("layout")

        #title
        self.title = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(28)
        self.title.setFont(font)
        self.title.setIndent(6)
        self.title.setObjectName("title")
        self.layout.addWidget(self.title)

        #HLine
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layout.addWidget(self.line)

        #search layout
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setObjectName("searchLayout")
        #search box
        self.key = QtWidgets.QLineEdit(self.centralWidget)
        self.key.setObjectName("key")
        self.searchLayout.addWidget(self.key)
        #search button
        self.searchButton = QtWidgets.QPushButton(self.centralWidget)
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.updateList)
        self.searchLayout.addWidget(self.searchButton)
        self.layout.addLayout(self.searchLayout)

        #list widget
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setObjectName("listWidget")
        self.layout.addWidget(self.listWidget)
        self.updateList()

        #buttons
        self.operations = QtWidgets.QDialogButtonBox(self.centralWidget)
        self.operations.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Open)
        self.operations.clicked.connect
        self.operations.setObjectName("operations")
        self.layout.addWidget(self.operations)

        self.retranslateUi(self.Widget)
        QtCore.QMetaObject.connectSlotsByName(self.Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "easyNote - 所有笔记"))
        self.title.setText(_translate("Widget", "所有笔记"))
        self.key.setPlaceholderText(_translate("Widget", "搜索"))
        self.searchButton.setText(_translate("Widget", "搜索"))
    
    def updateList(self):
        while self.listWidget.count():
            self.listWidget.takeItem(0)

        notes = oper.readNotesList()
        key = self.key.text()
        for note in notes:
            if key in note['title']:
                QtWidgets.QListWidgetItem(note['title'], self.listWidget)