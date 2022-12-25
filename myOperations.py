import json
import logging as log
from shutil import copytree, rmtree
import shutil
import string
import time
import os
import zipfile
from myWindows import *
from settings import settings

def clearCache():
    if os.path.isdir(".\\cache"):
        rmtree(".\\cache")
        os.mkdir(".\\cache")
        log.info("Cleared cache.")

def readNotesList():
    noteList = []

    if (not os.path.exists(".\\notes")):
        log.warn("Folder '.\\notes' not found!")
        return []
    
    for file in os.listdir(".\\notes"):
        file = ".\\notes\\%s\\note.json"%file
        if (os.path.isfile(file)):
            try:
                with open(file, 'r') as f:
                    note = json.load(f)
            except Exception as e:
                log.error("%s is not a readable json file. Message: %s"%(file, str(e)))
            else:
                noteList.append(note)
    
    return noteList

def save(title:str, text:str, ctime=time.localtime(time.time())):
    filename = "%s"%title

    if (not os.path.exists(".\\notes")):
        os.mkdir(".\\notes")
        log.warn("Folder '.\\notes' not found!")
        log.info("Created Folder '.\\notes' .")
    
    contain = {"title": title, "text": text, "time": tuple(ctime)}
    
    if os.path.exists(".\\notes\\"+filename): rmtree(".\\notes\\"+filename)
    os.mkdir(".\\notes\\"+filename)
    with open(".\\notes\\%s\\note.json"%filename, 'w') as f:
        j = json.dumps(contain, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        f.write(j)

    if os.path.isdir(".\\cache"): copytree('.\\cache', '.\\notes\\%s\\images'%filename)
    else: os.mkdir(".\\%s\\images"%filename)

    clearCache()
    log.info("Saved '%s' ."%filename)
    return 0

def setCurrentWid(widget):
    baseWid = settings.baseWid
    baseWid.setCentralWidget(widget)

def writeNote():
    baseWid = settings.baseWid
    writeWid = myWrite(baseWid)
    setCurrentWid(writeWid)
    writeWid.show()
    return writeWid

def viewAll():
    baseWid = settings.baseWid
    viewWid = myViewAll(baseWid)
    setCurrentWid(viewWid)
    viewWid.show()
    return viewWid

def viewFile(file):
    filepath = ".\\notes\\%s"%file.data(5)
    if os.path.exists(filepath):
        clearCache()
        os.rmdir(".\\cache")
        copytree(filepath+"\\images", ".\\cache")

        viewWid = myEdit(settings.baseWid)
        setCurrentWid(viewWid)
        viewWid.show()

        with open(filepath+"\\note.json", 'r') as f:
            viewWid.setFile(json.loads(f.read()))

        return viewWid

    else:
        log.error("File %s doesn't exist!"%filepath)
        return None

def reviewNote(file):
    filepath = ".\\notes\\%s"%file
    if os.path.exists(filepath):
        clearCache()
        os.rmdir(".\\cache")
        copytree(filepath+"\\images", ".\\cache")
        viewWid = myReview(settings.baseWid)
        setCurrentWid(viewWid)
        viewWid.show()

        with open(filepath+"\\note.json", 'r') as f:
            viewWid.setupForm(json.loads(f.read()))

        return viewWid

    else:
        log.error("File %s doesn't exist!"%filepath)
        return None

def returnToMain():
    baseWid = settings.baseWid
    baseWid.centralWidget().destroy()
    mainWid = myMain(baseWid)
    baseWid.setCentralWidget(mainWid)
    mainWid.show()
    baseWid.show()

def saveScore(title: str, score: int, ctime):
    path = ".\\notes\\%s\\note.json"%title
    with open(path, 'r') as f:
        a = json.loads(f.read())

    with open(path, 'w') as f:
        if 'score' not in a.keys(): a['score'] = []
        a['score'].append([tuple(ctime), score])

        j = json.dumps(a, sort_keys=True, indent=4, separators=(',', ':'))
        f.write(j)

def showScore(title):
    path = ".\\notes\\%s\\note.json"%title
    if not os.path.isfile(path):
        log.error("File %s doesn't exist!"%path)
        return None

    with open(".\\notes\\%s\\note.json"%title, 'r') as f:
        title = json.loads(f.read())["title"]

    try:
        with open(path) as f:
            scores = json.loads(f.read())['score']
            log.info("Opened score record for '%s'."%title)
    except KeyError:
        log.error("No reviewing record for '%s'."%title)
        scores = []

    historyWid = myReviewHistory()
    historyWid.setupNote(scores, title)
    historyWid.show()
    return historyWid

def delHistory(title):
    path = ".\\notes\\%s\\note.json"%title
    if not os.path.isfile(path):
        log.error("File %s doesn't exist!"%path)
        return None

    with open(path, "r") as f:
        file = json.loads(f.read())
    
    if 'score' in file.keys():
        del file['score']
    
    with open(path, 'w') as f:
        j = json.dumps(file, sort_keys=True, indent=4, separators=(',', ':'))
        f.write(j)

def delNote(fileName):
    if (os.path.isdir(".\\notes\\%s"%fileName)):
        with open(".\\notes\\%s\\note.json"%fileName, 'r') as f:
            try:
                name = json.loads(f.read())
            except:
                log.error("%s is not a readable json file."%fileName)
            else:
                delHistory(name['title'])
        rmtree(".\\notes\\%s"%fileName)

def importNote():
    from PyQt5.QtWidgets import QFileDialog, QMessageBox
    path = QFileDialog.getExistingDirectory(None, "选择笔记", ".\\notes")
    if (os.path.exists(path) and os.path.isdir(path+"\\images") and os.path.isfile(path+"\\note.json")):
        try:
            print(path)
            with open(path+"\\note.json", 'r') as f:
                data = json.loads(f.read())
            if (type(data["text"])==str and type(data["time"]in [list, tuple] and type(data["title"])==str)):
                if (len(data["time"])==9):
                    pass
                else:
                    QMessageBox().warning(None, "警告", "%s 不是合法的笔记目录 a"%path)
                    raise
            else:
                QMessageBox().warning(None, "警告", "%s 不是合法的笔记目录 b"%path)
                raise
        except:
            QMessageBox().warning(None, "警告", "%s 不是合法的笔记目录 c"%path)
        else:
            shutil.copytree(path, ".\\notes\\%s"%os.path.split(path)[-1])
            log.info("Imported %s as a note."%path)
            QMessageBox().information(None, "提示", "导入成功")
    else:
        QMessageBox().warning(None, "警告", "%s 不是合法的笔记目录 d"%path)

def exportNote(noteName):
    from PyQt5.QtWidgets import QFileDialog, QMessageBox
    target = QFileDialog.getSaveFileName(None, "选择导出路径", ".", "文件夹")
    target = target[0]
    src_dir = ".\\notes\\%s"%noteName
    shutil.copytree(src_dir, target)

    QMessageBox().information(None, "提示", "已将 %s 导出至 %s"%(noteName, target))
    log.info("Exported %s to %s.", noteName, target)

def getMdCodeDialog(callWid):
    from PyQt5 import QtWidgets, QtCore, QtGui

    inputDialog = QtWidgets.QDialog()
    inputDialog.setObjectName("Dialog")
    inputDialog.resize(400, 300)
    buttonBox = QtWidgets.QDialogButtonBox(inputDialog)
    buttonBox.setGeometry(QtCore.QRect(30, 260, 341, 32))
    buttonBox.setOrientation(QtCore.Qt.Horizontal)
    buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    buttonBox.setObjectName("buttonBox")

    verticalLayoutWidget = QtWidgets.QWidget(inputDialog)
    verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 241))
    verticalLayoutWidget.setObjectName("verticalLayoutWidget")
    verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
    verticalLayout.setContentsMargins(0, 0, 0, 0)
    verticalLayout.setObjectName("verticalLayout")

    label = QtWidgets.QLabel(verticalLayoutWidget)
    font = QtGui.QFont()
    font.setFamily("Microsoft YaHei UI")
    font.setPointSize(11)
    label.setFont(font)
    label.setObjectName("label")
    verticalLayout.addWidget(label)
    lineEdit = QtWidgets.QLineEdit(verticalLayoutWidget)
    lineEdit.setObjectName("lineEdit")
    verticalLayout.addWidget(lineEdit)
    line = QtWidgets.QFrame(verticalLayoutWidget)
    line.setFrameShape(QtWidgets.QFrame.HLine)
    line.setFrameShadow(QtWidgets.QFrame.Sunken)
    line.setObjectName("line")
    verticalLayout.addWidget(line)
    label_2 = QtWidgets.QLabel(verticalLayoutWidget)
    label_2.setFont(font)
    label_2.setObjectName("label_2")
    verticalLayout.addWidget(label_2)
    textEdit = QtWidgets.QTextEdit(verticalLayoutWidget)
    textEdit.setObjectName("textEdit")
    textEdit.setAcceptRichText(False)
    verticalLayout.addWidget(textEdit)

    inputDialog.setWindowTitle("插入代码")
    label.setText("语言（可选的）")
    label_2.setText("代码")

    def getCode():
        rtValue = ["",""]
        rtValue[0] = lineEdit.text()
        rtValue[1] = textEdit.toPlainText()
        if rtValue[1]:
            callWid.addCode(*rtValue)
            inputDialog.destroy()

    buttonBox.accepted.connect(getCode)
    buttonBox.rejected.connect(inputDialog.destroy)

    inputDialog.show()

def getMdLinkDialog(callWid):
    from PyQt5 import QtWidgets, QtCore, QtGui

    inputDialog = QtWidgets.QDialog()
    inputDialog.setObjectName("Dialog")
    inputDialog.resize(400, 300)
    buttonBox = QtWidgets.QDialogButtonBox(inputDialog)
    buttonBox.setGeometry(QtCore.QRect(30, 260, 341, 32))
    buttonBox.setOrientation(QtCore.Qt.Horizontal)
    buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    buttonBox.setObjectName("buttonBox")

    verticalLayoutWidget = QtWidgets.QWidget(inputDialog)
    verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 241))
    verticalLayoutWidget.setObjectName("verticalLayoutWidget")
    verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
    verticalLayout.setContentsMargins(0, 0, 0, 0)
    verticalLayout.setObjectName("verticalLayout")

    label = QtWidgets.QLabel(verticalLayoutWidget)
    font = QtGui.QFont()
    font.setFamily("Microsoft YaHei UI")
    font.setPointSize(11)
    label.setFont(font)
    label.setObjectName("label")
    verticalLayout.addWidget(label)
    getLinkName = QtWidgets.QLineEdit(verticalLayoutWidget)
    getLinkName.setObjectName("getLinkName")
    getLinkName.setClearButtonEnabled(True)
    verticalLayout.addWidget(getLinkName)
    line = QtWidgets.QFrame(verticalLayoutWidget)
    line.setFrameShape(QtWidgets.QFrame.HLine)
    line.setFrameShadow(QtWidgets.QFrame.Sunken)
    line.setObjectName("line")
    verticalLayout.addWidget(line)
    label_2 = QtWidgets.QLabel(verticalLayoutWidget)
    label_2.setFont(font)
    label_2.setObjectName("label_2")
    verticalLayout.addWidget(label_2)
    getLinkURL = QtWidgets.QLineEdit(verticalLayoutWidget)
    getLinkURL.setObjectName("getLinkURL")
    getLinkURL.setClearButtonEnabled(True)
    verticalLayout.addWidget(getLinkURL)

    inputDialog.setWindowTitle("插入链接")
    label.setText("链接名称（可选的）")
    label_2.setText("链接地址")

    def insertLink():
        rtValue = ["",""]
        rtValue[0] = getLinkName.text()
        rtValue[1] = getLinkURL.text()
        if rtValue[1]:
            callWid.addLink(*rtValue)
            inputDialog.destroy()
            
    buttonBox.accepted.connect(insertLink)
    buttonBox.rejected.connect(inputDialog.destroy)
    
    inputDialog.show()

def getMdImageDialog(callWid):
    from PyQt5 import QtWidgets, QtCore, QtGui
    
    inputDialog = QtWidgets.QDialog()
    inputDialog.setObjectName("Dialog")
    inputDialog.resize(400, 300)
    buttonBox = QtWidgets.QDialogButtonBox(inputDialog)
    buttonBox.setGeometry(QtCore.QRect(30, 260, 341, 32))
    buttonBox.setOrientation(QtCore.Qt.Horizontal)
    buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    buttonBox.setObjectName("buttonBox")

    verticalLayoutWidget = QtWidgets.QWidget(inputDialog)
    verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 241))
    verticalLayoutWidget.setObjectName("verticalLayoutWidget")
    verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
    verticalLayout.setContentsMargins(0, 0, 0, 0)
    verticalLayout.setObjectName("verticalLayout")

    label = QtWidgets.QLabel(verticalLayoutWidget)
    font = QtGui.QFont()
    font.setFamily("Microsoft YaHei UI")
    font.setPointSize(11)
    label.setFont(font)
    label.setObjectName("label")
    verticalLayout.addWidget(label)
    getImageURL = QtWidgets.QLineEdit(verticalLayoutWidget)
    getImageURL.setObjectName("getImageURL")
    getImageURL.setClearButtonEnabled(True)
    verticalLayout.addWidget(getImageURL)
    getImageButton = QtWidgets.QPushButton()
    getImageButton.setObjectName("getImageButton")
    getImageButton.setText("选择文件")
    verticalLayout.addWidget(getImageButton)
    line = QtWidgets.QFrame(verticalLayoutWidget)
    line.setFrameShape(QtWidgets.QFrame.HLine)
    line.setFrameShadow(QtWidgets.QFrame.Sunken)
    line.setObjectName("line")
    verticalLayout.addWidget(line)
    label_2 = QtWidgets.QLabel(verticalLayoutWidget)
    label_2.setFont(font)
    label_2.setObjectName("label_2")
    verticalLayout.addWidget(label_2)
    getImageText = QtWidgets.QLineEdit(verticalLayoutWidget)
    getImageText.setObjectName("getImageText")
    getImageText.setClearButtonEnabled(True)
    verticalLayout.addWidget(getImageText)

    inputDialog.setWindowTitle("插入图片")
    label.setText("图片路径")
    label_2.setText("图片描述（可选的）")

    def openImage():
        get = QtWidgets.QFileDialog()
        get.setWindowTitle("选择图片")
        get.setWindowFilePath(".")
        get.setNameFilters(['*.png', '*.jpg', '*.bmp', '*.gif'])

        get.exec()
        while 1:
            if len(get.selectedFiles()):
                getImageURL.setText(get.selectedFiles()[0])
                return
    
    def insertImage():
        path = getImageURL.text()
        if os.path.isfile(path):
            fType = os.path.splitext(path)[-1]
            cPath = "./cache/%d%s"%(hash(path), fType)
            shutil.copyfile(path, cPath)
            
            text = '<img src="%s" alt="%s" width=450 />'%(cPath, getImageText.text())
            callWid.addImage(text)
            inputDialog.destroy()
        else:
            QtWidgets.QMessageBox().warning(None, "警告", "%s不是支持的文件"%path)
            log.warning('"%s" cannot be copied!'%path)
    
    getImageButton.clicked.connect(openImage)
    buttonBox.accepted.connect(insertImage)
    buttonBox.rejected.connect(inputDialog.destroy)

    inputDialog.show()