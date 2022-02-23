from fileinput import filename
import json
import logging as log
import time
import os
from myWindows import *

def readNotesList():
    noteList = []

    if (not os.path.exists(".\\notes")):
        log.warn("Folder '.\\notes' not found!")
        return []
    
    for file in os.listdir(".\\notes"):
        file = ".\\notes\\%s"%file
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
    filename = "%s_%s.json"%(title, time.strftime(r"%Y%m%d_%H%M%S", ctime))

    if (not os.path.exists(".\\notes")):
        os.mkdir(".\\notes")
        log.warn("Folder '.\\notes' not found!")
        log.info("Created Folder '.\\notes' .")
    
    contain = {"title": title, "text": text, "time": tuple(ctime)}
    
    with open(".\\notes\\"+filename, 'w') as f:
        j = json.dumps(contain, sort_keys=True, indent=4, separators=(',', ':'))
        f.write(j)
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
    if os.path.exists(filepath) and os.path.isfile(filepath):
        viewWid = myEdit()
        viewWid.show()

        with open(filepath, 'r') as f:
            viewWid.setFile(json.loads(f.read()))

        return viewWid

    else:
        log.error("File %s doesn't exist!"%filepath)
        return None

def reviewNote(file):
    filepath = ".\\notes\\%s"%file
    if os.path.exists(filepath) and os.path.isfile(filepath):
        viewWid = myReview()
        viewWid.show()

        with open(filepath, 'r') as f:
            viewWid.setupForm(json.loads(f.read()))

        return viewWid

    else:
        log.error("File %s doesn't exist!"%filepath)
        return None


def saveScore(title: str, score: int, ctime):
    if not os.path.isfile(".\\score.json"):
        f = open(".\\score.json", "w")
        f.write(r"{}")
        f.close()
    
    with open(".\\score.json", 'r') as f:
        a = json.loads(f.read())

    with open('.\\score.json', 'w') as f:
        if title not in a.keys():
            a[title] = []
        a[title].append([tuple(ctime), score])

        j = json.dumps(a, sort_keys=True, indent=4, separators=(',', ':'))
        f.write(j)

def showScore(title):
    if not os.path.isfile(".\\score.json"):
        log.error("File score.json doesn't exist!")
        return None

    with open(".\\notes\\%s"%title, 'r') as f:
        title = json.loads(f.read())["title"]

    try:
        with open(".\\score.json") as f:
            scores = json.loads(f.read())[title]
            log.info("Opened score record for '%s'."%title)
    except KeyError:
        log.error("No reviewing record for '%s'."%title)
        scores = []

    historyWid = myReviewHistory()
    historyWid.setupNote(scores, title)
    historyWid.show()
    return historyWid

def delHistory(title):
    if not os.path.isfile(".\\score.json"):
        log.error("File score.json doesn't exist!")
        return None

    with open(".\\score.json", "r") as f:
        file = json.loads(f.read())
    
    if title in file.keys():
        del file[title]
    
    with open(".\\score.json", 'w') as f:
        j = json.dumps(file, sort_keys=True, indent=4, separators=(',', ':'))
        f.write(j)

def delNote(fileName):
    if (os.path.isfile(".\\notes\\%s"%fileName)):
        with open(".\\notes\\%s"%fileName, 'r') as f:
            try:
                name = json.loads(f.read())
            except:
                log.error("%s is not a readable json file."%fileName)
            else:
                delHistory(name['title'])
        os.remove(".\\notes\\%s"%fileName)
