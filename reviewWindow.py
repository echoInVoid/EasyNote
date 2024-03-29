import logging
import time
from PyQt5 import QtCore, QtWidgets, QtGui
import markdown as md
from random import random

import jieba

from note import Note
jieba.set_dictionary('.\\dict.txt')
jieba.setLogLevel(logging.INFO)
import jieba.analyse
jieba.analyse.set_idf_path('.\\idf.txt')
jieba.initialize()

import myOperations as oper
from cleanHTML import clean_html

from settings import settings


class UIReviewWindow(object):
    def setupUi(self, ReviewWindow: QtWidgets.QWidget):
        ReviewWindow.setObjectName("ReviewWindow")
        ReviewWindow.resize(*settings.windowSize)

        self.mainLayout = QtWidgets.QVBoxLayout(ReviewWindow)
        self.mainLayout.setContentsMargins(*settings.windowContentMargin)
        self.mainLayout.setObjectName("mainLayout")

        #title
        self.title = QtWidgets.QLabel(ReviewWindow)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(26)
        self.title.setFont(font)
        self.title.setIndent(7)
        self.title.setMaximumHeight(40)
        self.title.setObjectName("title")
        self.mainLayout.addWidget(self.title)

        # HLine
        self.line = QtWidgets.QFrame(ReviewWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.mainLayout.addWidget(self.line)

        self.score = QtWidgets.QLabel()
        self.score.setStyleSheet("font-size: 30px; font-family: Microsoft YaHei UI;")
        self.score.setText("分数：N/A")
        self.score.setMaximumHeight(40)
        self.mainLayout.addWidget(self.score)

        self.text = QtWidgets.QTextBrowser(ReviewWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text.sizePolicy().hasHeightForWidth())
        self.text.setSizePolicy(sizePolicy)
        self.text.setMinimumSize(QtCore.QSize(0, 350))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(15)
        self.text.setFont(font)
        self.text.setObjectName("text")
        self.mainLayout.addWidget(self.text)

        # a ScrollArea for form
        self.formArea = QtWidgets.QScrollArea(ReviewWindow)
        self.formArea.setWidgetResizable(True)
        self.formArea.setObjectName("formArea")
        self.formArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.formArea.setMaximumHeight(250)
        # child widget for form
        self.formWid = QtWidgets.QWidget()
        self.formWid.setGeometry(QtCore.QRect(0, 0, 707, 172))
        self.formWid.setObjectName("formWid")
        # layout for form
        self.form = QtWidgets.QFormLayout(self.formWid)
        self.formWid.setLayout(self.form)
        self.form.setContentsMargins(0, 0, 0, 0)
        self.form.setObjectName("form")
        self.formArea.setWidget(self.formWid)
        self.mainLayout.addWidget(self.formArea)

        self.checkBtn = QtWidgets.QPushButton()
        self.checkBtn.setObjectName("checkBtn")
        self.checkBtn.clicked.connect(self.check)
        self.mainLayout.addWidget(self.checkBtn)

        self.retranslateUi(ReviewWindow)
        QtCore.QMetaObject.connectSlotsByName(ReviewWindow)

    def retranslateUi(self, ReviewWindow):
        _translate = QtCore.QCoreApplication.translate
        ReviewWindow.setWindowTitle(_translate("ReviewWindow", "EasyNote - 复习"))
        self.title.setText(_translate("title", "复习"))
        self.checkBtn.setText(_translate("checkBtn" ,"检查"))

    def isValidWord(self, word: str):
        if set(word) & set(settings.enPuncs): return False # English puncs
        chineseP = settings.zhPuncs
        if set(word) & set(chineseP): return False # Chinese puncs
        if word in settings.specialWords: return False
        if ' ' in word: return False
        if word.strip() == '': return False
        if len(word) <= 1: return False
        return True

    def setupForm(self, file: Note):
        self.file = file
        self.file.text = md.markdown(
            self.file.text,
            extensions=settings.markdownExt
        )
        
        pureText = clean_html(self.file.text)

        filecut = jieba.lcut(pureText)
        self.spaces = []
        for word in filecut:
            if random()<=settings.reviewWordProbability and self.isValidWord(word):
                self.spaces.append(word)
        logging.debug(self.spaces)

        for i in range(len(self.spaces)):
            self.file.text = self.file.text.replace(self.spaces[i], "___%d___"%(i+1))

        richText = str(md.markdown(
            self.file.text,
            extensions=settings.markdownExt
        ))
        self.text.setHtml(richText)

        self.inputs = []
        for i in range(len(self.spaces)):
            line = QtWidgets.QLineEdit()
            line.setFixedHeight(20)
            line.setStyleSheet("background-color: white;")
            self.inputs.append(line)
            self.form.addRow('%d: '%(i+1), line)
    
    def check(self):
        if self.form.rowCount() < 1: return
        score = 0
        for i in range(self.form.rowCount()):
            textField = self.inputs[i]
            if textField.text() == self.spaces[i]:
                score += 1
                textField.setStyleSheet("background-color: rgba(58,255,78,97);")
                t = self.text.toHtml().replace("___%d___"%i, "<strong style=background-color:rgba(58,255,78,97)>___%d___</strong>"%i)
                self.text.setHtml(t)
            else:
                textField.setStyleSheet("background-color: rgba(255,135,143,147);")
                t = self.text.toHtml().replace("___%d___"%i, "<strong style=background-color:rgba(255,135,143,147)>___%d___</strong>"%i)
                self.text.setHtml(t)
        
        score = score / self.form.rowCount() * 10
        self.score.setText("分数：%d"%score)
        
        oper.saveScore(self.file.title, score, time.localtime(time.time()))