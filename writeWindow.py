import logging
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import myOperations as oper
import markdown as md
from note import Note
from settings import settings


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
        self.inImage.clicked.connect(lambda x: oper.getMdImageDialog(self))
        self.buttons.addWidget(self.inImage)
        self.inCode = QtWidgets.QPushButton(self.WriteWindow)
        self.inCode.setObjectName("inCode")
        self.inCode.clicked.connect(lambda x: oper.getMdCodeDialog(self))
        self.buttons.addWidget(self.inCode)
        self.inLink = QtWidgets.QPushButton(self.WriteWindow)
        self.inLink.setObjectName("inLink")
        self.inLink.clicked.connect(lambda x: oper.getMdLinkDialog(self))
        self.buttons.addWidget(self.inLink)
        self.texts.addLayout(self.buttons)

        # a layout for the input area & preview area
        self.edit = QtWidgets.QHBoxLayout()
        self.edit.setObjectName("edit")
        # input area
        self.getText = QtWidgets.QPlainTextEdit(self.WriteWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.getText.setFont(font)
        self.getText.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.getText.setAutoFillBackground(False)
        self.getText.setObjectName("getText")
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
        oper.returnToMain()

    def accept(self):
        title = self.getTitle.text()
        text = self.getText.toPlainText()
        if len(title):
            oper.save(Note(title, text, []))
            self.kill()

    def reject(self):
        logging.info("Save Canceled.")
        self.kill()

    def updatePreview(self):
        richText = str(md.markdown( 
            self.getText.toPlainText(),
            extensions=settings.markdownExt
        ))
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