import logging
from PyQt5 import QtCore, QtGui, QtWidgets
import myOperations as oper
from settings import settings


class UIViewAllWindow(object):
    def setupUi(self, Widget: QtWidgets.QWidget):
        self.Widget = Widget
        self.Widget.setObjectName("Widget")
        self.Widget.resize(*settings.windowSize)

        # layout
        self.layout = QtWidgets.QVBoxLayout(self.Widget)
        self.layout.setContentsMargins(*settings.windowContentMargin)
        self.layout.setObjectName("layout")

        # title
        self.title = QtWidgets.QLabel(self.Widget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(28)
        self.title.setFont(font)
        self.title.setIndent(6)
        self.title.setObjectName("title")
        self.layout.addWidget(self.title)

        # HLine
        self.line = QtWidgets.QFrame(self.Widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layout.addWidget(self.line)

        # search layout
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setObjectName("searchLayout")
        # search box
        self.key = QtWidgets.QLineEdit(self.Widget)
        self.key.setObjectName("key")
        self.searchLayout.addWidget(self.key)
        # search button
        self.searchButton = QtWidgets.QPushButton(self.Widget)
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.updateList)
        self.searchLayout.addWidget(self.searchButton)
        self.layout.addLayout(self.searchLayout)

        # list widget
        self.listWidget = QtWidgets.QListWidget(self.Widget)
        self.listWidget.setObjectName("listWidget")
        self.layout.addWidget(self.listWidget)
        self.updateList()

        # buttons
        self.operations = QtWidgets.QHBoxLayout()
        self.operations.setObjectName("operations")
        # spacer
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.operations.addItem(spacerItem)
        # open button
        self.open_ = QtWidgets.QPushButton(self.Widget)
        self.open_.setObjectName("open_")
        self.open_.clicked.connect(self.openNote)
        self.operations.addWidget(self.open_)
        # review button
        self.review = QtWidgets.QPushButton(self.Widget)
        self.review.setObjectName("review")
        self.review.clicked.connect(self.reviewNote)
        self.operations.addWidget(self.review)
        # review history
        self.reviewH = QtWidgets.QPushButton(self.Widget)
        self.reviewH.setObjectName("review")
        self.reviewH.clicked.connect(self.reviewHistory)
        self.operations.addWidget(self.reviewH)
        # delete button
        self.delete = QtWidgets.QPushButton(self.Widget)
        self.delete.setObjectName("delete")
        self.delete.clicked.connect(self.delNote)
        self.operations.addWidget(self.delete)
        # cancel button
        self.cancel = QtWidgets.QPushButton(self.Widget)
        self.cancel.setObjectName("cancel")
        self.cancel.clicked.connect(self.kill)
        self.operations.addWidget(self.cancel)
        self.layout.addLayout(self.operations)

        self.retranslateUi(self.Widget)
        QtCore.QMetaObject.connectSlotsByName(self.Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "EasyNote - 所有笔记"))
        self.title.setText(_translate("Widget", "所有笔记"))
        self.key.setPlaceholderText(_translate("Widget", "搜索"))
        self.searchButton.setText(_translate("Widget", "搜索"))
        self.open_.setText(_translate("Widget", "打开"))
        self.review.setText(_translate("Widget", "复习"))
        self.reviewH.setText(_translate("Widget", "复习历史"))
        self.delete.setText(_translate("Widget", "删除"))
        self.cancel.setText(_translate("Widget", "取消"))

    def updateList(self):
        while self.listWidget.count():
            self.listWidget.takeItem(0)

        notes = oper.readNotesList()
        key = self.key.text()
        for note in notes:
            if key in note['title']:
                item = QtWidgets.QListWidgetItem(note['title'], self.listWidget)
                filename = note['title']
                item.setData(5, filename)

    def openNote(self):
        if len(self.listWidget.selectedItems()) == 1:
            oper.viewFile(self.listWidget.selectedItems()[0])

    def reviewNote(self):
        if len(self.listWidget.selectedItems()) == 1:
            self.reviewWid = oper.reviewNote(self.listWidget.selectedItems()[0].data(5))

    def reviewHistory(self):
        if len(self.listWidget.selectedItems()) == 1:
            oper.showScore(self.listWidget.selectedItems()[0].data(5))

    def delNote(self):
        if len(self.listWidget.selectedItems()) == 1:
            oper.delNote(self.listWidget.selectedItems()[0].data(5))
            logging.info("Deleted note %s"%self.listWidget.selectedItems()[0].data(5))
            self.updateList()

    def kill(self):
        oper.returnToMain()
