from PyQt5.QtWidgets import QMainWindow, QWidget

from mainWindow import UIMainWindow
from reviewHistoryWindow import UIReviewHistoryWindow
from reviewWindow import UIReviewWindow
from viewAllWindow import UIViewAllWindow
from viewOrEdit import UiEditWindow
from writeWindow import UIWriteWindow

class myMain(QMainWindow, UIMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class myWrite(QWidget, UIWriteWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(0)
        self.setupUi(self)

class myViewAll(QWidget, UIViewAllWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(0)
        self.setupUi(self)

class myEdit(QWidget, UiEditWindow):
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