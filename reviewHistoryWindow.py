# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\reviewHistory.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



# 导入matplotlib模块并使用Qt5Agg
import time
import matplotlib
matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets, QtGui
import matplotlib.pyplot as plt
import logging as log
import myOperations as oper


class UIReviewHistoryWindow(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(760, 600)

        # widgets for matplotlib
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        plt.rcParams["font.family"] = "SimHei"
        plt.title("历史复习分数")
        plt.ylabel("分数")
        plt.xlabel("时间")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.Dialog)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.canvas)

        self.clear = QtWidgets.QPushButton(self.Dialog)
        self.clear.setStyleSheet("font-family: 微软雅黑; font-size: x-large;")
        self.clear.setText("清除历史")
        self.clear.clicked.connect(self.clearHistory)
        self.verticalLayout.addWidget(self.clear)

        self.retranslateUi(self.Dialog)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "EasyNote - 复习历史"))

    def setupNote(self, scores: list, title):
        # widgets for matplotlib
        plt.clf()

        self.title = title
        t = [time.strftime("%Y%m%d-%H:%M:%S", tuple(i[0])) for i in scores]
        scores = [i[1] for i in scores]
        plt.plot(t, scores, 'bo-')
        self.canvas.draw()

    def clearHistory(self):
        oper.delHistory(self.title)
        self.setupNote([], self.title)
