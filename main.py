from functools import wraps
import progressbar
bar = progressbar.ProgressBar(max_value=100)
print("加载中……")

import logging as log
import sys

from PyQt5.QtWidgets import QApplication
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

def main():
    setUp()
    bar.update(25)

    try:
        app = QApplication(sys.argv)
        bar.update(50)
        mainWid = myMain()
        bar.update(70)
        mainWid.show()
        bar.update(100)
        print("加载完成")
        code = app.exec()
        sys.exit(code)
    except Exception as e:
        import traceback as tb
        trace = tb.format_exc()
        log.fatal("\nFatal Error:\n%s\nProgram exited."%trace)
        clearCache()
        sys.exit("\nFatal Error:\n%s\nProgram exited."%trace)

if __name__ == "__main__":
    main()