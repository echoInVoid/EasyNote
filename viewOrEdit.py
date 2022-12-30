import logging
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import markdown as md

import myOperations as oper
from note import Note
from settings import settings

class UIEditWindow(object):
    def setupUi(self, EditWindow: QtWidgets.QWidget):
        self.EditWindow = EditWindow
        self.EditWindow.setObjectName("EditWindow")
        self.EditWindow.resize(*settings.windowSize)

        self.canEdit = False
        
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

        #get title
        self.getTitle = QtWidgets.QLineEdit(self.EditWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.getTitle.sizePolicy().hasHeightForWidth())
        self.getTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(20)
        self.getTitle.setFont(font)
        self.getTitle.setMaxLength(40)
        self.getTitle.setObjectName("getTitle")
        self.getTitle.setReadOnly(not self.canEdit)
        self.verticalLayout.addWidget(self.getTitle)

        # a layout for all text inputing & previewing
        self.texts = QtWidgets.QVBoxLayout()
        self.texts.setObjectName("texts")

        # contain control buttons
        self.buttons = QtWidgets.QHBoxLayout()
        self.buttons.setObjectName("buttons")
        self.inImage = QtWidgets.QPushButton(self.EditWindow)
        self.inImage.setObjectName("inImage")
        self.inImage.clicked.connect(lambda x: oper.getMdImageDialog(self))
        self.buttons.addWidget(self.inImage)
        self.inCode = QtWidgets.QPushButton(self.EditWindow)
        self.inCode.setObjectName("inCode")
        self.inCode.clicked.connect(lambda x: oper.getMdCodeDialog(self))
        self.buttons.addWidget(self.inCode)
        self.inLink = QtWidgets.QPushButton(self.EditWindow)
        self.inLink.setObjectName("inLink")
        self.inLink.clicked.connect(lambda x: oper.getMdLinkDialog(self))
        self.buttons.addWidget(self.inLink)
        self.texts.addLayout(self.buttons)

        # a layout for the input area & preview area
        self.edit = QtWidgets.QHBoxLayout()
        self.edit.setObjectName("edit")
        # input area
        self.getText = QtWidgets.QPlainTextEdit(self.EditWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.getText.setFont(font)
        self.getText.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.getText.setAutoFillBackground(False)
        self.getText.setObjectName("getText")
        self.getText.setReadOnly(True)
        self.getText.textChanged.connect(self.updatePreview)
        self.edit.addWidget(self.getText)
        # markdown preview
        self.preview = QtWidgets.QTextBrowser(self.EditWindow)
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
        self.getTitle.setPlaceholderText(_translate("EditWindow", "编辑标题(40字符以下)"))
        self.inImage.setText(_translate("EditWindow", "插入图片"))
        self.inCode.setText(_translate("EditWindow", "插入代码"))
        self.inLink.setText(_translate("EditWindow", "插入链接"))
        self.getText.setPlaceholderText(_translate("EditWindow", "Markdown代码"))
        self.preview.setPlaceholderText(_translate("EditWindow", "笔记预览"))

    def switchEdit(self):
        self.canEdit = not self.canEdit
        self.getText.setReadOnly(not self.canEdit)

        _translate = QtCore.QCoreApplication.translate
        if self.canEdit:
            self.editState.setText(_translate("EditWindow", "编辑: 启用"))
        else:
            self.editState.setText(_translate("EditWindow", "编辑: 禁用"))

    def setFile(self, file: Note):
        self.file = file
        self.getTitle.setText(file.title)
        self.getText.setPlainText(file.text)
            
    def kill(self):
        oper.returnToMain()

    def accept(self):
        title = self.getTitle.text()
        text = self.getText.toPlainText()
        if len(title) != 0:
            oper.save(Note(title, text, []))
            self.kill()

    def reject(self):
        logging.info("Save Canceled.")
        self.kill()

    def updatePreview(self):
        richText = str(md.markdown(
            self.getText.toPlainText(),
            extensions=settings.markdownExt
        )).replace('\x0245', '\\').replace('\x03', '-')
        self.preview.setHtml(richText)

    def openLink(self, link: QtCore.QUrl):
        os.system('start "" "%s"'%link.url())

    def addCode(self, lang, code):
        mdCode = "```{ .%s }\n%s\n```"%(lang, code)
        self.getText.textCursor().insertText(mdCode)

    def addImage(self, text):
        self.getText.textCursor().insertText(text)

    def addLink(self, name, url):
        if url and name:
            self.getText.textCursor().insertText("[%s](%s)"%(name, url))
        else: self.getText.textCursor().insertText("<%s>"%(url))