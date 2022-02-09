from PyQt5.QtWidgets import QMainWindow, QWidget

from mainWindow import UIMainWindow
from reviewWindow import UIReviewWindow
from viewAllWindow import UI_viewAllWidget
from viewOrEdit import Ui_EditWindow
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

class myViewAll(QWidget, UI_viewAllWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(0)
        self.setupUi(self)

class myEdit(QWidget, Ui_EditWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(0)
        self.setupUi(self)

class myReview(QWidget, UIReviewWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(0)
        self.setupUi(self)