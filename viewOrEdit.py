# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\viewOrEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.4


import logging
from PyQt5 import QtCore, QtGui, QtWidgets

import myOperations as oper

class UiEditWindow(object):
    def setupUi(self, EditWindow: QtWidgets.QWidget):
        self.EditWindow = EditWindow
        self.EditWindow.setObjectName("EditWindow")
        self.EditWindow.resize(760, 606)

        self.canEdit = False

        self.buttonBox = QtWidgets.QDialogButtonBox(self.EditWindow)
        self.buttonBox.setGeometry(QtCore.QRect(350, 540, 341, 32))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        #main layout
        self.verticalLayoutWidget = QtWidgets.QWidget(self.EditWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 691, 511))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        #title
        self.title = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(26)
        self.title.setFont(font)
        self.title.setIndent(7)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)

        #head layout (for edit state switch)
        self.head = QtWidgets.QHBoxLayout()
        self.head.setObjectName("head")
        #show edit state
        self.editState = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.editState.setFont(font)
        self.editState.setIndent(9)
        self.editState.setObjectName("editState")
        self.head.addWidget(self.editState)
        #button to switch edit state
        self.switchEditButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.switchEditButton.setFont(font)
        self.switchEditButton.setObjectName("switchEditButton")
        self.switchEditButton.clicked.connect(self.switchEdit)
        self.head.addWidget(self.switchEditButton)
        self.verticalLayout.addLayout(self.head)

        #a simple line between INFO area and EDIT area
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        #get title
        self.getTitle = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.getTitle.sizePolicy().hasHeightForWidth())
        self.getTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.getTitle.setFont(font)
        self.getTitle.setMaxLength(40)
        self.getTitle.setObjectName("getTitle")
        self.getTitle.setReadOnly(not self.canEdit)
        self.verticalLayout.addWidget(self.getTitle)

        #get text
        self.text = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.text.setFont(font)
        self.text.setObjectName("text")
        self.text.setReadOnly(not self.canEdit)
        self.text.setUndoRedoEnabled(True)
        self.verticalLayout.addWidget(self.text)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.access)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self.EditWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.EditWindow.setWindowTitle(_translate("EditWindow", "EasyLog - 查看&编辑"))
        self.title.setText(_translate("EditWindow", "浏览&编辑笔记"))
        self.editState.setText(_translate("EditWindow", "编辑: 禁用"))
        self.switchEditButton.setText(_translate("EditWindow", "切换编辑"))
        self.getTitle.setPlaceholderText(_translate("EditWindow", "编辑标题(40字符以下)"))
        self.text.setPlaceholderText(_translate("EditWindow", "编辑正文"))

    def switchEdit(self):
        self.canEdit = not self.canEdit
        self.text.setReadOnly(not self.canEdit)

        _translate = QtCore.QCoreApplication.translate
        if self.canEdit:
            self.editState.setText(_translate("EditWindow", "编辑: 启用"))
        else:
            self.editState.setText(_translate("EditWindow", "编辑: 禁用"))

    def setFile(self, file):
        self.file = file
        self.getTitle.setText(file['title'])
        self.text.setText(file['text'])
    
    def kill(self):
        self.EditWindow.destroy()
        del self

    def access(self):
        title = self.getTitle.text()
        text = self.text.toPlainText()
        oper.save(title, text, tuple(self.file['time']))
        self.kill()

    def reject(self):
        logging.info("Save Canceled.")
        self.kill()