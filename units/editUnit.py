from PyQt5 import QtWidgets, QtGui, QtCore
import markdown as md
import os
import sys

sys.path.append(os.path.abspath(".")) # Cannot import files in /EasyNote/ without this line. I know it's ugly but I have to.
import myOperations as oper
from settings import settings

class UIEditUnit():
    def setupUi(self, editWidget: QtWidgets.QWidget, canEdit=False):
        self.editWidget = editWidget
        self.canEdit = canEdit

        #main layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.editWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        #get title
        self.getTitle = QtWidgets.QLineEdit(self.editWidget)
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

        # # contain control buttons
        # self.buttons = QtWidgets.QHBoxLayout()
        # self.buttons.setObjectName("buttons")
        # self.inImage = QtWidgets.QPushButton(self.editWidget)
        # self.inImage.setObjectName("inImage")
        # self.inImage.clicked.connect(lambda x: oper.getMdImageDialog(self) if self.canEdit else None)
        # self.buttons.addWidget(self.inImage)
        # self.inCode = QtWidgets.QPushButton(self.editWidget)
        # self.inCode.setObjectName("inCode")
        # self.inCode.clicked.connect(lambda x: oper.getMdCodeDialog(self) if self.canEdit else None)
        # self.buttons.addWidget(self.inCode)
        # self.inLink = QtWidgets.QPushButton(self.editWidget)
        # self.inLink.setObjectName("inLink")
        # self.inLink.clicked.connect(lambda x: oper.getMdLinkDialog(self) if self.canEdit else None)
        # self.buttons.addWidget(self.inLink)
        # self.texts.addLayout(self.buttons)

        # tool bar
        self.setupToolBar()

        # a layout for the input area & preview area
        self.edit = QtWidgets.QHBoxLayout()
        self.edit.setObjectName("edit")
        # input area
        self.getText = QtWidgets.QPlainTextEdit(self.editWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.getText.setFont(font)
        self.getText.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.getText.setAutoFillBackground(False)
        self.getText.setObjectName("getText")
        self.getText.setReadOnly(not self.canEdit)
        self.getText.textChanged.connect(self.updatePreview)
        self.edit.addWidget(self.getText)
        # markdown preview
        self.preview = QtWidgets.QTextBrowser(self.editWidget)
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

        self.editWidget.show()
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.getTitle.setPlaceholderText(_translate("EditWindow", "编辑标题(40字符以下)"))
        # self.inImage.setText(_translate("EditWindow", "插入图片"))
        # self.inCode.setText(_translate("EditWindow", "插入代码"))
        # self.inLink.setText(_translate("EditWindow", "插入链接"))
        self.getText.setPlaceholderText(_translate("EditWindow", "Markdown代码"))
        self.preview.setPlaceholderText(_translate("EditWindow", "笔记预览"))

    def setupToolBar(self):
        # tool bar
        self.toolBar = QtWidgets.QWidget(self.editWidget)
        self.toolBar.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.toolBar.setFixedHeight(30)
        self.toolBar.setFixedSize(8*30+8*5+6, 30)
        self.toolBarLayout = QtWidgets.QHBoxLayout(self.toolBar)
        self.toolBarLayout.setContentsMargins(3,0,0,3)
        self.verticalLayout.addWidget(self.toolBar)

        # buttons
        self.setBold = QtWidgets.QToolButton(self.toolBar)
        self.setBold.setObjectName("setBold")
        self.setBold.clicked.connect(lambda x: self.wrapSelectedText("**"))
        self.setupBtn(self.setBold, "bold.png", "加粗选中文本")
        self.toolBarLayout.addWidget(self.setBold)

        self.setItalic = QtWidgets.QToolButton(self.toolBar)
        self.setItalic.setObjectName("setItalic")
        self.setItalic.clicked.connect(lambda x: self.wrapSelectedText("*"))
        self.setupBtn(self.setItalic, "italic.png", "倾斜选中文本")
        self.toolBarLayout.addWidget(self.setItalic)
        
        self.setUnderline = QtWidgets.QToolButton(self.toolBar)
        self.setUnderline.setObjectName("setUnderline")
        self.setUnderline.clicked.connect(lambda x: self.wrapSelectedText2("<u>", "</u>"))
        self.setupBtn(self.setUnderline, "underline.png", "为选中文本添加下划线")
        self.toolBarLayout.addWidget(self.setUnderline)

        self.switchTitle = QtWidgets.QToolButton(self.toolBar)
        self.switchTitle.setObjectName("switchTitle")
        self.switchTitle.clicked.connect(self.switchRowTitle)
        self.setupBtn(self.switchTitle, "h.png", "切换当前行标题级数")
        self.toolBarLayout.addWidget(self.switchTitle)

        self.setDelLine = QtWidgets.QToolButton(self.toolBar)
        self.setDelLine.setObjectName("setDelLine")
        self.setDelLine.clicked.connect(lambda x: self.wrapSelectedText("~"))
        self.setupBtn(self.setDelLine, "delLine.png", "为选中文本添加删除线")
        self.toolBarLayout.addWidget(self.setDelLine)

        self.inImage = QtWidgets.QToolButton(self.toolBar)
        self.inImage.setObjectName("inImage")
        self.inImage.clicked.connect(lambda x: oper.getMdImageDialog(self) if self.canEdit else None)
        self.setupBtn(self.inImage, "image.png", "插入图片")
        self.toolBarLayout.addWidget(self.inImage)

        self.inCode = QtWidgets.QToolButton(self.toolBar)
        self.inCode.setObjectName("inCode")
        self.inCode.clicked.connect(lambda x: oper.getMdCodeDialog(self) if self.canEdit else None)
        self.setupBtn(self.inCode, "code.png", "插入代码")
        self.toolBarLayout.addWidget(self.inCode)

        self.inLink = QtWidgets.QToolButton(self.toolBar)
        self.inLink.setObjectName("inLink")
        self.inLink.clicked.connect(lambda x: oper.getMdLinkDialog(self) if self.canEdit else None)
        self.setupBtn(self.inLink, "link.png", "插入链接")
        self.toolBarLayout.addWidget(self.inLink)

    def setupBtn(self, btn: QtWidgets.QToolButton, icon, tip='', size=[30,30]):
        btn.setFixedSize(*size)
        btn.setIcon(QtGui.QIcon(".\\resource\\buttons\\%s"%icon))
        btn.setIconSize(QtCore.QSize(*size))
        btn.setToolTip(tip)
    
    def wrapSelectedText(self, w: str):
        """用 w 包裹选中的文本"""
        self.wrapSelectedText2(w, w)

    def wrapSelectedText2(self, wStart: str, wEnd: str):
        """在选中的文本两端分别插入 wStart 和 wEnd"""
        if (not self.getText.textCursor().hasSelection()):
            return
        
        srt = self.getText.textCursor().selectionStart()
        end = self.getText.textCursor().selectionEnd()
        text = self.getText.toPlainText()
        text = "%s%s%s%s%s"%(text[:srt], wStart, text[srt:end], wEnd, text[end:])
        self.getText.setPlainText(text)
    
    def switchRowTitle(self):
        cursor = self.getText.textCursor()
        start = cursor.block().position()
        text = self.getText.toPlainText()
        print(cursor.block().length()) 
        if (cursor.block().length()<=1): # 空行
            return

        # 统计块开头有多少个#
        cnt = 0
        while (text[start+cnt] == '#'):
            cnt += 1
        if (cnt==5): # 到达5级标题，去除标题
            text = text[:start]+text[start+cnt:]
        else:
            text = text[:start] + '#' + text[start:] # 增加一级标题

        self.getText.setPlainText(text)

    def switchEdit(self):
        self.canEdit = not self.canEdit
        self.getText.setReadOnly(not self.canEdit)

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


class myEditUnit(QtWidgets.QWidget, UIEditUnit):
    def __init__(self, parent=None, canEdit=False):
        super().__init__(parent)
        self.setupUi(self, canEdit)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    wid = myEditUnit(None ,True)
    app.exec_()