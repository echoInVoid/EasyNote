import logging
from PyQt5 import QtCore, QtGui, QtWidgets
import myOperations as oper
from note import Note
from settings import settings
from units.editUnit import myEditUnit

class UIWriteWindow(object):
    def setupUi(self, WriteWindow: QtWidgets.QWidget):
        self.WriteWindow = WriteWindow
        self.WriteWindow.setObjectName("WriteWindow")
        self.WriteWindow.resize(*settings.windowSize)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.WriteWindow)
        self.verticalLayout.setContentsMargins(*settings.windowContentMargin)
        self.verticalLayout.setObjectName("verticalLayout")

        self.create = QtWidgets.QLabel(self.WriteWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(26)
        self.create.setFont(font)
        self.create.setIndent(7)
        self.create.setObjectName("create")
        self.verticalLayout.addWidget(self.create)

        self.line = QtWidgets.QFrame(self.WriteWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        # edit unit
        self.editUnit = myEditUnit(self.WriteWindow, True)
        self.verticalLayout.addWidget(self.editUnit)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(self.WriteWindow)
        self.buttonBox.setGeometry(QtCore.QRect(370, 540, 341, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self.WriteWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.WriteWindow.setWindowTitle(_translate("WriteWindow", "EasyNote - 写笔记"))
        self.create.setText(_translate("WriteWindow", "创建笔记"))
        
    def kill(self):
        oper.returnToMain()

    def accept(self):
        title = self.editUnit.getTitle.text()
        text = self.editUnit.getText.toPlainText()
        if len(title):
            oper.save(Note(title, text, []))
            self.kill()

    def reject(self):
        logging.info("Save Canceled.")
        self.kill()
