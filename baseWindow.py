from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QMenuBar
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
import myOperations as oper
from settings import settings

class UIBaseWindow(object):
    def setupUi(self, baseWid: QMainWindow):
        self.baseWid = baseWid
        self.baseWid.resize(*settings.baseWindowSize)
        self.baseWid.setWindowTitle("EasyNote")
        self.baseWid.setWindowIcon(QIcon(".\\resource\\icon.png"))

        #menubar
        menubar = QMenuBar(self.baseWid)
        menubar.setGeometry(QRect(0, 0, 840, 25))
        menubar.setObjectName("menubar")
        #main
        main_ = QMenu(menubar) # main page (1st menu)
        main_.setObjectName("main")
        main_.setTitle("主页")
        main_.triggered.connect(oper.returnToMain)
        menubar.addAction(main_.menuAction())
        #edit
        edit = QMenu(menubar) # edit note (1st menu)
        edit.setObjectName("edit")
        edit.setTitle("编辑")
        create = QAction(self.baseWid) # create note
        create.setObjectName("create")
        create.setText("创建笔记")
        create.triggered.connect(lambda x: oper.writeNote())
        edit.addAction(create)
        view = QAction(self.baseWid) # view all notes
        view.setObjectName("view")
        view.setText("浏览笔记")
        view.triggered.connect(lambda x: oper.viewAll())
        edit.addAction(view)
        menubar.addAction(edit.menuAction())
        #file operation
        file = QMenu(menubar)
        file.setObjectName("file")
        file.setTitle("本地文件")
        importNote = QAction(self.baseWid)
        importNote.setObjectName("importNote")
        importNote.setText("导入笔记")
        importNote.triggered.connect(lambda x: oper.importNote())
        file.addAction(importNote)
        menubar.addAction(file.menuAction())
        # set as menubar
        self.baseWid.setMenuBar(menubar)