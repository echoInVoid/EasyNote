# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/write.ui'
#
# Created by: PyQt5 UI code generator 5.15.4


import logging
from PyQt5 import QtCore, QtGui, QtWidgets
import myOperations as oper


class UIWriteWindow(object):
    def setupUi(self, WriteWindow):
        self.WriteWindow = WriteWindow
        self.WriteWindow.setObjectName("WriteWindow")
        self.WriteWindow.resize(760, 600)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.WriteWindow)
        self.buttonBox.setGeometry(QtCore.QRect(350, 540, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.WriteWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 691, 511))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.create = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(26)
        self.create.setFont(font)
        self.create.setIndent(7)
        self.create.setObjectName("create")
        self.verticalLayout.addWidget(self.create)

        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setIndent(12)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.getTitle = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.getTitle.setFont(font)
        self.getTitle.setObjectName("getTitle")
        self.getTitle.setMaxLength(15)
        self.getTitle.setPlaceholderText("输入标题（不超过50字符）")
        self.verticalLayout.addWidget(self.getTitle)

        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)

        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setIndent(12)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.getText = QtWidgets.QTextEdit(self.verticalLayoutWidget)

        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.getText.setFont(font)
        self.getText.setObjectName("getText")
        self.getText.setPlaceholderText("输入标题（不超过400字符）")
        self.verticalLayout.addWidget(self.getText)

        self.retranslateUi(self.WriteWindow)
        self.buttonBox.accepted.connect(self.WriteWindow.access)
        self.buttonBox.rejected.connect(self.WriteWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(self.WriteWindow)

    def retranslateUi(self, WriteWindow):
        _translate = QtCore.QCoreApplication.translate
        WriteWindow.setWindowTitle(_translate("WriteWindow", "EasyNote - 写笔记"))
        self.create.setText(_translate("WriteWindow", "创建笔记"))
        self.label_2.setText(_translate("WriteWindow", "标题"))
        self.label_3.setText(_translate("WriteWindow", "内容"))
        
    def kill(self):
        del self.WriteWindow
        del self

    def access(self):
        title = self.getTitle.text()
        text = self.getText.toPlainText()
        if len(title) + len(text) != 0:
            oper.save(title, text)
            self.kill()

    def reject(self):
        logging.info("Save Canceled.")
        self.kill()
