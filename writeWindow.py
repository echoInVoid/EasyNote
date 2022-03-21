# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/write.ui'
#
# Created by: PyQt5 UI code generator 5.15.4


import logging
import os
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets
import myOperations as oper
import markdown as md


class UIWriteWindow(object):
    def setupUi(self, WriteWindow: QtWidgets.QWidget):
        self.WriteWindow = WriteWindow
        self.WriteWindow.setObjectName("WriteWindow")
        self.WriteWindow.resize(760, 600)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.WriteWindow)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
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

        self.label_2 = QtWidgets.QLabel(self.WriteWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setIndent(12)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.getTitle = QtWidgets.QLineEdit(self.WriteWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.getTitle.setFont(font)
        self.getTitle.setText("")
        self.getTitle.setMaxLength(50)
        self.getTitle.setDragEnabled(True)
        self.getTitle.setClearButtonEnabled(True)
        self.getTitle.setObjectName("getTitle")
        self.verticalLayout.addWidget(self.getTitle)

        self.line_2 = QtWidgets.QFrame(self.WriteWindow)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)

        self.label_3 = QtWidgets.QLabel(self.WriteWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setIndent(12)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        # a layout for all text inputing & previewing
        self.texts = QtWidgets.QVBoxLayout()
        self.texts.setObjectName("texts")

        # contain control buttons
        self.buttons = QtWidgets.QHBoxLayout()
        self.buttons.setObjectName("buttons")
        self.inImage = QtWidgets.QPushButton(self.WriteWindow)
        self.inImage.setObjectName("inImage")
        self.inImage.clicked.connect(self.addImage)
        self.buttons.addWidget(self.inImage)
        self.inCode = QtWidgets.QPushButton(self.WriteWindow)
        self.inCode.setObjectName("inCode")
        self.inCode.clicked.connect(self.addCode)
        self.buttons.addWidget(self.inCode)
        self.inLink = QtWidgets.QPushButton(self.WriteWindow)
        self.inLink.setObjectName("inLink")
        self.inLink.clicked.connect(self.addLink)
        self.buttons.addWidget(self.inLink)
        self.texts.addLayout(self.buttons)

        # a layout for the input area & preview area
        self.edit = QtWidgets.QHBoxLayout()
        self.edit.setObjectName("edit")
        # input area
        self.getText = QtWidgets.QTextEdit(self.WriteWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.getText.setFont(font)
        self.getText.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.getText.setAutoFillBackground(False)
        self.getText.setObjectName("getText")
        self.getText.setAcceptRichText(False)
        self.getText.textChanged.connect(self.updatePreview)
        self.edit.addWidget(self.getText)
        # markdown preview
        self.preview = QtWidgets.QTextBrowser(self.WriteWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.preview.setFont(font)
        self.preview.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.preview.setOpenLinks(False)
        self.preview.anchorClicked.connect(self.openLink)
        self.preview.setObjectName("preview")
        self.edit.addWidget(self.preview)

        self.texts.addLayout(self.edit)
        self.verticalLayout.addLayout(self.texts)
        
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
        self.label_2.setText(_translate("WriteWindow", "标题"))
        self.getTitle.setPlaceholderText(_translate("WriteWindow", "输入标题"))
        self.label_3.setText(_translate("WriteWindow", "正文"))
        self.inImage.setText(_translate("WriteWindow", "插入图片"))
        self.inCode.setText(_translate("WriteWindow", "插入代码"))
        self.inLink.setText(_translate("WriteWindow", "插入链接"))
        self.getText.setPlaceholderText(_translate("WriteWindow", "Markdown代码"))
        self.preview.setPlaceholderText(_translate("WriteWindow", "笔记预览"))
        
    def kill(self):
        self.WriteWindow.destroy()
        del self

    def accept(self):
        title = self.getTitle.text()
        text = self.getText.toPlainText()
        if len(title) + len(text) != 0:
            oper.save(title, text)
            self.kill()

    def reject(self):
        logging.info("Save Canceled.")
        self.kill()

    def updatePreview(self):
        richText = str(md.markdown(
            self.getText.toPlainText(),
            extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite', 'markdown.extensions.extra', ]
        ))
        self.preview.setHtml(richText)

    def openLink(self, link: QtCore.QUrl):
        os.system('start "" "%s"'%link.url())

    def addCode(self):
        self.inputDialog = QtWidgets.QDialog()
        self.inputDialog.setObjectName("Dialog")
        self.inputDialog.resize(400, 300)
        buttonBox = QtWidgets.QDialogButtonBox(self.inputDialog)
        buttonBox.setGeometry(QtCore.QRect(30, 260, 341, 32))
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        buttonBox.setObjectName("buttonBox")

        verticalLayoutWidget = QtWidgets.QWidget(self.inputDialog)
        verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 241))
        verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout.setObjectName("verticalLayout")

        label = QtWidgets.QLabel(verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        label.setFont(font)
        label.setObjectName("label")
        verticalLayout.addWidget(label)
        lineEdit = QtWidgets.QLineEdit(verticalLayoutWidget)
        lineEdit.setObjectName("lineEdit")
        verticalLayout.addWidget(lineEdit)
        line = QtWidgets.QFrame(verticalLayoutWidget)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        verticalLayout.addWidget(line)
        label_2 = QtWidgets.QLabel(verticalLayoutWidget)
        label_2.setFont(font)
        label_2.setObjectName("label_2")
        verticalLayout.addWidget(label_2)
        textEdit = QtWidgets.QTextEdit(verticalLayoutWidget)
        textEdit.setObjectName("textEdit")
        textEdit.setAcceptRichText(False)
        verticalLayout.addWidget(textEdit)

        self.inputDialog.setWindowTitle("插入代码")
        label.setText("语言（可选的）")
        label_2.setText("代码")

        def insertCode():
            if textEdit.toPlainText():
                code = "```%s\n%s\n```"%(lineEdit.text(), textEdit.toPlainText())
                self.getText.textCursor().insertText(code)
                self.inputDialog.destroy()
        buttonBox.accepted.connect(insertCode)
        buttonBox.rejected.connect(self.inputDialog.destroy)

        self.inputDialog.show()


    def addImage(self):
        self.inputDialog = QtWidgets.QDialog()
        self.inputDialog.setObjectName("Dialog")
        self.inputDialog.resize(400, 300)
        buttonBox = QtWidgets.QDialogButtonBox(self.inputDialog)
        buttonBox.setGeometry(QtCore.QRect(30, 260, 341, 32))
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        buttonBox.setObjectName("buttonBox")

        verticalLayoutWidget = QtWidgets.QWidget(self.inputDialog)
        verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 241))
        verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout.setObjectName("verticalLayout")

        label = QtWidgets.QLabel(verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        label.setFont(font)
        label.setObjectName("label")
        verticalLayout.addWidget(label)
        getImageURL = QtWidgets.QLineEdit(verticalLayoutWidget)
        getImageURL.setObjectName("getImageURL")
        getImageURL.setClearButtonEnabled(True)
        verticalLayout.addWidget(getImageURL)
        line = QtWidgets.QFrame(verticalLayoutWidget)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        verticalLayout.addWidget(line)
        label_2 = QtWidgets.QLabel(verticalLayoutWidget)
        label_2.setFont(font)
        label_2.setObjectName("label_2")
        verticalLayout.addWidget(label_2)
        getImageText = QtWidgets.QLineEdit(verticalLayoutWidget)
        getImageText.setObjectName("getImageText")
        getImageText.setClearButtonEnabled(True)
        verticalLayout.addWidget(getImageText)

        self.inputDialog.setWindowTitle("插入图片")
        label.setText("图片路径")
        label_2.setText("图片描述（可选的）")

        def insertImage():
            path = getImageURL.text()
            if os.path.isfile(path):
                fType = os.path.splitext(path)[-1]
                cPath = ".\\\\cache\\\\%d%s"%(hash(path), fType)
                shutil.copyfile(path, cPath)
                
                text = '![%s](%s "%s")'%(getImageText.text().replace(' ', '-'), cPath, getImageText.text())
                self.getText.textCursor().insertText(text)
                self.inputDialog.destroy()
                return
            else:
                box = QtWidgets.QMessageBox()
                box.setWindowTitle("警告")
                box.setText("%s不可写入"%path)
                box.exec()
                logging.warning('"%s" cannot be copied!'%path)
        buttonBox.accepted.connect(insertImage)
        buttonBox.rejected.connect(self.inputDialog.destroy)

        self.inputDialog.show()

    def addLink(self):
            self.inputDialog = QtWidgets.QDialog()
            self.inputDialog.setObjectName("Dialog")
            self.inputDialog.resize(400, 300)
            buttonBox = QtWidgets.QDialogButtonBox(self.inputDialog)
            buttonBox.setGeometry(QtCore.QRect(30, 260, 341, 32))
            buttonBox.setOrientation(QtCore.Qt.Horizontal)
            buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
            buttonBox.setObjectName("buttonBox")

            verticalLayoutWidget = QtWidgets.QWidget(self.inputDialog)
            verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 241))
            verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
            verticalLayout.setContentsMargins(0, 0, 0, 0)
            verticalLayout.setObjectName("verticalLayout")

            label = QtWidgets.QLabel(verticalLayoutWidget)
            font = QtGui.QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(11)
            label.setFont(font)
            label.setObjectName("label")
            verticalLayout.addWidget(label)
            getLinkName = QtWidgets.QLineEdit(verticalLayoutWidget)
            getLinkName.setObjectName("getLinkName")
            getLinkName.setClearButtonEnabled(True)
            verticalLayout.addWidget(getLinkName)
            line = QtWidgets.QFrame(verticalLayoutWidget)
            line.setFrameShape(QtWidgets.QFrame.HLine)
            line.setFrameShadow(QtWidgets.QFrame.Sunken)
            line.setObjectName("line")
            verticalLayout.addWidget(line)
            label_2 = QtWidgets.QLabel(verticalLayoutWidget)
            label_2.setFont(font)
            label_2.setObjectName("label_2")
            verticalLayout.addWidget(label_2)
            getLinkURL = QtWidgets.QLineEdit(verticalLayoutWidget)
            getLinkURL.setObjectName("getLinkURL")
            getLinkURL.setClearButtonEnabled(True)
            verticalLayout.addWidget(getLinkURL)

            self.inputDialog.setWindowTitle("插入链接")
            label.setText("链接名称（可选的）")
            label_2.setText("链接地址")

            def insertLink():
                if getLinkURL.text():
                    self.getText.textCursor().insertText("[%s](%s)"%(getLinkName.text(), getLinkURL.text()))
            buttonBox.accepted.connect(insertLink)
            buttonBox.rejected.connect(self.inputDialog.destroy)
            
            self.inputDialog.show()