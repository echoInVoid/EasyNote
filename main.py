import logging as log
import sys

from PyQt5.QtWidgets import QApplication

from myOperations import *
from myWindows import myMain


def setUp():
    LOG_FORMAT = "[%(asctime)s][%(levelname)s] %(message)s"
    log.basicConfig(filename='logs\\%s.log'%time.strftime(r"%Y%m%d-%Hh-%Mm"), level=log.INFO, format=LOG_FORMAT)

    log.info("Set-Up completed.")

def main():
    setUp()

    try:
        app = QApplication(sys.argv)
        mainWid = myMain()
        mainWid.show()
        sys.exit(app.exec_())
    except Exception as e:
        log.fatal("\n\tFatal Error: %s\n\tProgram exited."%str(e))
        sys.exit()

if __name__ == "__main__":
    main()