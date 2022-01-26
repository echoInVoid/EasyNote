from asyncio.log import logger
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
                log.error("%s is not a readable json file.")
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
        json.dump(contain, f)
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