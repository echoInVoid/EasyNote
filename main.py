import logging as log
import sys
import time
from PyQt5.QtWidgets import QApplication

from myOperations import *
from myWindows import myMain
from settings import settings

def setUp():
    if not os.path.isdir(".\\logs"): os.mkdir(".\\logs") 
    settings.logFile = '.\\logs\\%s.log'%time.strftime(r"%Y%m%d-%Hh-%Mm")
    log.basicConfig(
        filename=settings.logFile, level=settings.logLevel, 
        format=settings.LOG_FORMAT, filemode='w', force=True
        )

    log.info("Set-Up completed.")
    clearCache()

setUp()

app = QApplication(sys.argv)
baseWid = myBase()
mainWid = myMain(baseWid)
baseWid.setCentralWidget(mainWid)
settings.baseWid = baseWid
mainWid.show()
baseWid.show()

try:
    code = app.exec()
    clearCache()
    sys.exit(code)
except Exception as e:
    import traceback as tb
    trace = tb.format_exc()
    log.fatal("\nFatal Error:\n%s\nProgram exited."%trace)
    clearCache()  
    sys.exit("\nFatal Error:\n%s\nProgram exited."%trace)