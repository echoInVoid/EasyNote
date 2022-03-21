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
bar.update(15)



def setUp():
    LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s"
    log.basicConfig(filename='logs\\%s.log'%time.strftime(r"%Y%m%d-%Hh-%Mm"), level=log.INFO, format=LOG_FORMAT)

    log.info("Set-Up completed.")
    clearCache()

def main():
    setUp()
    bar.update(20)

    try:
        app = QApplication(sys.argv)
        bar.update(50)
        mainWid = myMain()
        bar.update(70)
        mainWid.show()
        bar.update(100)
        print("加载完成")
        sys.exit(app.exec_())
    except Exception as e:
        log.fatal("\n\tFatal Error: %s\n\tProgram exited."%str(e))
        sys.exit()

if __name__ == "__main__":
    main()