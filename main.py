import progressbar
bar = progressbar.ProgressBar(maxval=100)
print("加载中……")
bar.start()

import logging as log
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore
bar.update(5)

from myOperations import *
bar.update(10)
from myWindows import myMain
bar.update(20)

from settings import settings
def setUp():
    if not os.path.isdir(".\\logs"): os.mkdir(".\\logs") 
    log.basicConfig(filename='.\\logs\\%s.log'%time.strftime(r"%Y%m%d-%Hh-%Mm"), level=settings.logLevel, format=settings.LOG_FORMAT, filemode='w')

    log.info("Set-Up completed.")
    clearCache()

setUp()
bar.update(25)

app = QApplication(sys.argv)
baseWid = QMainWindow()
baseWid.resize(*settings.welcomeWindowSize)
baseWid.setWindowTitle("EasyNote")

#menubar
menubar = QtWidgets.QMenuBar(baseWid)
menubar.setGeometry(QtCore.QRect(0, 0, 840, 25))
menubar.setObjectName("menubar")
#main
main_ = QtWidgets.QMenu(menubar) # main page (1st menu)
main_.setObjectName("main")
main_.setTitle("主页")
menubar.addAction(main_.menuAction())
#edit
edit = QtWidgets.QMenu(menubar) # edit note (1st menu)
edit.setObjectName("edit")
edit.setTitle("编辑")
create = QtWidgets.QAction(baseWid) # create note
create.setObjectName("create")
create.setText("创建笔记")
create.triggered.connect(lambda x: writeNote(baseWid))
edit.addAction(create)
view = QtWidgets.QAction(baseWid) # view all notes
view.setObjectName("view")
view.setText("浏览笔记")
view.triggered.connect(lambda x: viewAll(baseWid))
edit.addAction(view)
menubar.addAction(edit.menuAction())
# set as menubar
baseWid.setMenuBar(menubar)

bar.update(50)
mainWid = myMain(baseWid)
baseWid.setCentralWidget(mainWid)
bar.update(70)
settings.baseWid = baseWid
mainWid.show()
baseWid.show()
bar.update(100)
print("加载完成")

try:
    code = app.exec()
    sys.exit(code)  
except Exception as e:
    import traceback as tb
    trace = tb.format_exc()
    log.fatal("\nFatal Error:\n%s\nProgram exited."%trace)
    clearCache()
    sys.exit("\nFatal Error:\n%s\nProgram exited."%trace)