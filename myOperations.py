import json
import logging as log
from shutil import copytree, rmtree
import time
import os
from myWindows import *

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
            except:
                log.error("%s is not a readable json file."%file)
            else:
                noteList.append(note)
    
    return noteList

def save(title, text, ctime=time.localtime(time.time())):
    filename = "%s"%title

    if (not os.path.exists(".\\notes")):
        os.mkdir(".\\notes")
        log.warn("Folder '.\\notes' not found!")
        log.info("Created Folder '.\\notes' .")
    
    contain = {"title": title, "text": text, "time": tuple(ctime)}
    
    if os.path.exists(".\\notes\\"+filename): rmtree(".\\notes\\"+filename)
    os.mkdir(".\\notes\\"+filename)
    with open(".\\notes\\%s\\note.json"%filename, 'w') as f:
        j = json.dumps(contain, sort_keys=True, indent=4, separators=(',', ':'))
        f.write(j)

    if os.path.isdir(".\\cache"): copytree('.\\cache', '.\\notes\\%s\\images'%filename)
    else: os.mkdir(".\\%s\\images"%filename)

    clearCache()
    log.info("Saved '%s' ."%filename)
    return 0

def write():
    writeWid = myWrite()
    writeWid.show()
    return writeWid

def viewAll():
    viewWid = myViewAll()
    viewWid.show()
    return viewWid

def viewFile(file):
    filepath = ".\\notes\\%s"%file.data(5)
    if os.path.exists(filepath):
        clearCache()
        os.rmdir(".\\cache")
        copytree(filepath+"\\images", ".\\cache")

        viewWid = myEdit()
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
        viewWid = myReview()
        viewWid.show()

        with open(filepath+"\\note.json", 'r') as f:
            viewWid.setupForm(json.loads(f.read()))

        return viewWid

    else:
        log.error("File %s doesn't exist!"%filepath)
        return None


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

def clearCache():
    if os.path.isdir(".\\cache"):
        rmtree(".\\cache")
        os.mkdir(".\\cache")
        log.info("Cleared cache.")