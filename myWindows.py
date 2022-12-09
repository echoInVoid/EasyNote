import sys
from PyQt5.QtWidgets import QMainWindow, QWidget

from mainWindow import UIMainWindow
from reviewHistoryWindow import UIReviewHistoryWindow
from reviewWindow import UIReviewWindow
from viewAllWindow import UIViewAllWindow
from viewOrEdit import UIEditWindow
from writeWindow import UIWriteWindow

class myMain(QWidget, UIMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    # def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
    #     sys.exit(0)

class myWrite(QWidget, UIWriteWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setWindowModality(0)
        self.setupUi(self)

class myViewAll(QWidget, UIViewAllWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(0)
        self.setupUi(self)

class myEdit(QWidget, UIEditWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(0)
        self.setupUi(self)

class myReview(QWidget, UIReviewWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(0)
        self.setupUi(self)

class myReviewHistory(QWidget, UIReviewHistoryWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(0)
        self.setupUi(self)