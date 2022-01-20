import sys
import easygui as gui

from basicOperations import *

def main():
    while True:
        operation = gui.buttonbox("执行操作", "简单笔记", ("写", "查看", "退出"), image="resource/welcome.gif")
        if (operation == "写"):
            write()
        elif (operation == "查看"):
            view()
        else:
            return


if __name__ == "__main__":
    main()
    sys.exit(0)