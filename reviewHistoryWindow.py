# 导入matplotlib模块并使用Qt5Agg
import time
import matplotlib
matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
import myOperations as oper
from settings import settings


class UIReviewHistoryWindow(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(*settings.infoDialogSize)

        # widgets for matplotlib
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        plt.rcParams["font.family"] = "SimHei"
        plt.title("历史复习分数")
        plt.ylabel("分数")
        plt.xlabel("时间")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.Dialog)
        self.verticalLayout.setContentsMargins(*settings.windowContentMargin)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.canvas)

        self.clear = QtWidgets.QPushButton(self.Dialog)
        self.clear.setStyleSheet("font-family: Microsoft YaHei UI; font-size: x-large;")
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
