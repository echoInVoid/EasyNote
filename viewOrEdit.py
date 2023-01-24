import logging
from PyQt5 import QtCore, QtGui, QtWidgets

import myOperations as oper
from note import Note
from settings import settings
from units.editUnit import myEditUnit

class UIEditWindow(object):
    def setupUi(self, EditWindow: QtWidgets.QWidget):
        self.EditWindow = EditWindow
        self.EditWindow.setObjectName("EditWindow")
        self.EditWindow.resize(*settings.windowSize)
        
        #main layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.EditWindow)
        self.verticalLayout.setContentsMargins(*settings.windowContentMargin)
        self.verticalLayout.setObjectName("verticalLayout")

        #title
        self.title = QtWidgets.QLabel(self.EditWindow)
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
        self.editState = QtWidgets.QLabel(self.EditWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.editState.setFont(font)
        self.editState.setIndent(9)
        self.editState.setObjectName("editState")
        self.head.addWidget(self.editState)
        #button to switch edit state
        self.switchEditButton = QtWidgets.QPushButton(self.EditWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.switchEditButton.setFont(font)
        self.switchEditButton.setObjectName("switchEditButton")
        self.switchEditButton.clicked.connect(self.switchEdit)
        self.head.addWidget(self.switchEditButton)
        self.verticalLayout.addLayout(self.head)

        #a simple line between INFO area and EDIT area
        self.line = QtWidgets.QFrame(self.EditWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        # editUnit
        self.editUnit = myEditUnit(self.EditWindow)
        self.verticalLayout.addWidget(self.editUnit)

        # dialog buttonbox
        self.buttonBox = QtWidgets.QDialogButtonBox(self.EditWindow)
        self.buttonBox.setGeometry(QtCore.QRect(350, 540, 341, 32))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.EditWindow.show()

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self.EditWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.EditWindow.setWindowTitle(_translate("EditWindow", "EasyNote - 查看&编辑"))
        self.title.setText(_translate("EditWindow", "浏览&编辑笔记"))
        self.editState.setText(_translate("EditWindow", "编辑: 禁用"))
        self.switchEditButton.setText(_translate("EditWindow", "切换编辑"))

    def switchEdit(self):
        self.editUnit.canEdit = not self.editUnit.canEdit
        self.editUnit.getText.setReadOnly(not self.editUnit.canEdit)

        _translate = QtCore.QCoreApplication.translate
        if self.editUnit.canEdit:
            self.editState.setText(_translate("EditWindow", "编辑: 启用"))
        else:
            self.editState.setText(_translate("EditWindow", "编辑: 禁用"))

    def setFile(self, file: Note):
        self.file = file
        self.editUnit.getTitle.setText(file.title)
        self.editUnit.getText.setPlainText(file.text)
            
    def kill(self):
        oper.returnToMain()

    def accept(self):
        title = self.editUnit.getTitle.text()
        text = self.editUnit.getText.toPlainText()
        if len(title) != 0:
            oper.save(Note(title, text, []))
            self.kill()

    def reject(self):
        logging.info("Save Canceled.")
        self.kill()
