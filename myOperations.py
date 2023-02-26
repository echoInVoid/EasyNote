import json
import logging as log
import os
import shutil
import sys
import time
import markdown as md
import pdfkit as pdf
import zipfile as zpf
from shutil import copytree, rmtree
from hashlib import sha1

from myWindows import *
from note import Note
from settings import settings


def logError(func):
    """作为装饰器使用，将被装饰函数抛出的异常捕获并记录，然后退出"""
    import functools
    @functools.wraps(func)
    def dec(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.basicConfig(
                filename=settings.logFile, level=settings.logLevel, 
                format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]\n%(message)s", filemode='a', force=True
                )
            import traceback as tb
            log.critical(f"------EASYNOTE CRASH LOG------\nTraceback below:\n{tb.format_exc()}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                QMessageBox(), "致命错误", 
                f"程序发生了一个异常，即将退出。\n详情请查阅{os.path.abspath(settings.logFile)}中的日志。\n错误信息摘要：{str(e)}"
                )
            sys.exit(1)
    return dec

@logError
def clearCache():
    if os.path.isdir(".\\cache"):
        rmtree(".\\cache")
        os.mkdir(".\\cache")
        log.info("Cleared cache.")

@logError
def readNotesList():
    noteList = []

    if (not os.path.exists(".\\notes")):
        log.warn("Folder '.\\notes' not found!")
        return []
    
    for file in os.listdir(".\\notes"):
        fDir = file
        file = ".\\notes\\%s\\note.json"%file
        if (os.path.isfile(file)):
            try:
                with open(file, 'r') as f:
                    note = json.load(f)
                note['dir'] = fDir
            except Exception as e:
                log.error("%s is not a readable json file. Message: %s"%(file, str(e)))
            else:
                noteList.append(note)
    
    return noteList

@logError
def save(note: Note):
    filename = "%s"%note.title

    if (not os.path.exists(".\\notes")):
        os.mkdir(".\\notes")
        log.warn("Folder '.\\notes' not found!")
        log.info("Created Folder '.\\notes' .")
    
    contain = note.toDict()
    
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

@logError
def exportNoteToZip(notePath, zipPath):
    if (not os.path.isdir(notePath) or not isValidNotePath(notePath)):
        log.error("Zipnote failed. Invalid note path: %s", notePath)
        return
    elif (not os.path.isdir(os.path.dirname(zipPath))):
        log.error("Zipnote failed. Invalid zip path: %s", zipPath)
        return
    
    with zpf.ZipFile(zipPath, "w") as z:
        arcRoot = os.path.split(notePath)[-1]
        noteRoot = os.path.abspath(notePath)
        z.write(noteRoot+"\\note.json", arcRoot+"\\note.json")

        for f in os.listdir(noteRoot+"\\images"):
            z.write(noteRoot+"\\images\\"+f, arcRoot+"\\images\\"+f)
        if len(os.listdir(noteRoot+"\\images"))==0:
            clearCache()
            with open(".\\cache\\placeholder.txt", 'w') as f:
                f.write("placeholder")
            z.write(".\\cache\\placeholder.txt", arcRoot+"\\images\\placeholder.txt")
    log.info("Successfully zipped %s to %s", notePath, zipPath)

@logError
def exportNoteToPdf(notePath, pdfPath):
    if (not os.path.isdir(notePath) or not isValidNotePath(notePath)):
        log.error("Pdfnote failed. Invalid note path: %s", notePath)
        return
    elif (not os.path.isdir(os.path.dirname(pdfPath))):
        log.error("Zipnote failed. Invalid pdf path: %s", pdfPath)
        return
    
    clearCache()
    imagePath = os.path.join(os.path.abspath(notePath), "images")
    imageList = os.listdir(imagePath)
    for i in imageList:
        if os.path.isfile(imagePath+'\\'+i):
            shutil.copyfile(imagePath+'\\'+i, ".\\cache\\%s"%i)

    with open(notePath+"\\note.json", "r") as f:
        noteJson = json.loads(f.read())
    htmlStr = md.markdown(
        "#%s\n##%s\n\n"%(noteJson["title"], time.strftime(r"%Y/%m/%d(%a) %H:%M", tuple(noteJson["time"]))) + noteJson["text"],
        extensions=settings.markdownExt
        )
    htmlStr = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8"/>
        </head>
        <body>
            %s
        </body>
    </html>
    """%htmlStr
    options = {"enable-local-file-access": True}
    config = pdf.configuration(wkhtmltopdf=".\\resource\\wk\\wkhtmltopdf.exe")
    pdf.from_string(htmlStr, pdfPath, configuration=config, options=options, css=".\\resource\\pdf.css")
    log.info("Successfully PDFed %s to %s", notePath, pdfPath)
    clearCache()

@logError
def setCurrentWid(widget):
    baseWid = settings.baseWid
    baseWid.setCentralWidget(widget)

@logError
def writeNote():
    baseWid = settings.baseWid
    writeWid = myWrite(baseWid)
    setCurrentWid(writeWid)
    writeWid.show()
    return writeWid

@logError
def viewAll():
    baseWid = settings.baseWid
    viewWid = myViewAll(baseWid)
    setCurrentWid(viewWid)
    viewWid.show()
    return viewWid

@logError
def viewFile(file):
    filepath = ".\\notes\\%s"%file
    if os.path.exists(filepath):
        clearCache()
        os.rmdir(".\\cache")
        copytree(filepath+"\\images", ".\\cache")

        viewWid = myEdit(settings.baseWid)
        setCurrentWid(viewWid)
        viewWid.show()

        with open(filepath+"\\note.json", 'r') as f:
            note = Note(**json.loads(f.read()))
            viewWid.setFile(note)

        return viewWid

    else:
        log.error("File %s doesn't exist!"%filepath)
        return None

@logError
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
            note = Note(**json.loads(f.read()))
            viewWid.setupForm(note)

        return viewWid

    else:
        log.error("File %s doesn't exist!"%filepath)
        return None

@logError
def returnToMain():
    baseWid = settings.baseWid
    baseWid.centralWidget().destroy()
    mainWid = myMain(baseWid)
    baseWid.setCentralWidget(mainWid)
    mainWid.show()
    baseWid.show()

@logError
def saveScore(title: str, score: int, ctime):
    path = ".\\notes\\%s\\note.json"%title
    with open(path, 'r') as f:
        a = json.loads(f.read())

    with open(path, 'w') as f:
        if 'score' not in a.keys(): a['score'] = []
        a['score'].append([tuple(ctime), score])

        j = json.dumps(a, sort_keys=True, indent=4, separators=(',', ':'))
        f.write(j)

@logError
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

@logError
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

@logError
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

@logError
def isValidNotePath(path) -> bool:
    flag = True
    abspath = os.path.abspath(path)

    # 检查文件夹结构
    flag = flag and os.path.isdir(os.path.join(abspath, "images"))
    flag = flag and os.path.isfile(os.path.join(abspath, "note.json"))
    
    # 检查note.json
    try:
        with open(os.path.join(abspath, "note.json"), "r") as f:
            data = json.loads(f.read())
        
        flag = flag and type(data["text"])==str
        flag = flag and (type(data["time"]) in [list, tuple])
        flag = flag and type(data["title"]) == str
        flag = flag and len(data["time"])==9
    except:
        flag = False
        return flag

    return flag

@logError
def importNote():
    from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog
    path = QFileDialog.getOpenFileName(None, "选择笔记", ".\\notes", "EasyNote笔记文件(*.ezn)")[0]
    if (not os.path.isfile(path)):
        log.warning("No such file: %s"%path)
        return

    clearCache()
    with zpf.ZipFile(path, 'r') as z:
        z.extractall(".\\cache")
    noteName = os.listdir(".\\cache")[0]
    if (not isValidNotePath(".\\cache\\"+noteName)):
        QMessageBox.warning(None, "警告", "不合法的笔记！文件可能已损坏。\n%s"%path)
        log.warning("Bad note file: %s"%noteName)
        return

    noteDir = ".\\notes\\"+noteName
    while os.path.isdir(noteDir):
        choice = QMessageBox.question(
            None, "同名笔记",
            "检测到当前笔记目录中存在与将要导入的笔记同名的笔记。点击 Yes 覆盖，点击 No 为将要导入的笔记重命名。"
            )
        if (choice==QMessageBox.Yes):
            shutil.rmtree(noteDir)
        else:
            name = QInputDialog.getText(None, "输入文件夹名", "提示，最简单的方式为在原名结尾处加上数字。", text=noteName)
            if name[1]:
                noteName = name[0]
            noteDir = ".\\notes\\"+noteName

    shutil.copytree(".\\cache\\"+os.listdir(".\\cache")[0], noteDir)
    clearCache()
    
    QMessageBox.information(None, "导入成功", "已将 %s 导入到 %s。"%(path, noteDir))
    log.info("Successfully imported %s from %s。"%(noteDir, path))

@logError
def exportNote(noteName):
    from PyQt5.QtWidgets import QFileDialog, QMessageBox
    target = QFileDialog.getSaveFileName(None, "选择导出路径", "%s.ezn"%noteName, "EasyNote笔记文件(*.ezn)\nPDF文件(*.pdf)")
    if (len(target[0]) == 0): return

    src_dir = ".\\notes\\%s"%noteName
    if ".ezn" in target[1]:
        target = target[0]
        exportNoteToZip(src_dir, target)

        QMessageBox().information(None, "提示", "已将 %s 导出至 %s"%(noteName, target))
        log.info("Exported %s to %s.", noteName, target)
    elif ".pdf" in target[1]:
        target = target[0]
        exportNoteToPdf(src_dir, target)
        QMessageBox().information(None, "提示", "已将 %s 导出至 %s"%(noteName, target))
        log.info("Exported %s to %s.", noteName, target)

@logError
def getMdCodeDialog(callWid):
    if not callWid.canEdit: return
    
    from PyQt5 import QtCore, QtGui, QtWidgets

    inputDialog = QtWidgets.QDialog()
    inputDialog.setObjectName("Dialog")
    inputDialog.setFixedSize(400, 300)
    inputDialog.setWindowIcon(QtGui.QIcon(settings.icon))
    buttonBox = QtWidgets.QDialogButtonBox(inputDialog)
    buttonBox.setGeometry(QtCore.QRect(30, 260, 340, 30))
    buttonBox.setOrientation(QtCore.Qt.Horizontal)
    buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    buttonBox.setObjectName("buttonBox")

    verticalLayoutWidget = QtWidgets.QWidget(inputDialog)
    verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 360, 240))
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

@logError
def getMdLinkDialog(callWid):
    if not callWid.canEdit: return

    from PyQt5 import QtCore, QtGui, QtWidgets

    inputDialog = QtWidgets.QDialog()
    inputDialog.setObjectName("Dialog")
    inputDialog.setFixedSize(400, 200)
    inputDialog.setWindowIcon(QtGui.QIcon(settings.icon))
    buttonBox = QtWidgets.QDialogButtonBox(inputDialog)
    buttonBox.setGeometry(QtCore.QRect(30, 160, 340, 30))
    buttonBox.setOrientation(QtCore.Qt.Horizontal)
    buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    buttonBox.setObjectName("buttonBox")

    verticalLayoutWidget = QtWidgets.QWidget(inputDialog)
    verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 360, 150))
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

@logError
def getMdImageDialog(callWid):
    if not callWid.canEdit: return

    from PyQt5 import QtCore, QtGui, QtWidgets
    
    inputDialog = QtWidgets.QDialog()
    inputDialog.setObjectName("Dialog")
    inputDialog.setFixedSize(400, 200)
    inputDialog.setWindowIcon(QtGui.QIcon(settings.icon))
    buttonBox = QtWidgets.QDialogButtonBox(inputDialog)
    buttonBox.setGeometry(QtCore.QRect(30, 160, 340, 30))
    buttonBox.setOrientation(QtCore.Qt.Horizontal)
    buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    buttonBox.setObjectName("buttonBox")

    verticalLayoutWidget = QtWidgets.QWidget(inputDialog)
    verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 360, 150))
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
        filepath, filetype = QtWidgets.QFileDialog.getOpenFileName(None, "选择图片", ".", "Images: (*.png *.jpg *.bmp *.gif)")
        
        if len(filepath):
            getImageURL.setText(filepath)
    
    def insertImage():
        path = getImageURL.text()
        if os.path.isfile(path):
            fType = os.path.splitext(path)[-1]
            targetName = sha1()
            targetName.update(path.encode("utf-8"))
            targetName = targetName.hexdigest()
            cPath = os.path.abspath("./cache/%s%s"%(targetName, fType))
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
