import json
import logging as log
import time
import os
from myWindows import myWrite

def save(title, text):
    if (not os.path.exists(".\\notes")):
        os.mkdir(".\\notes")
        log.warn("Folder '.\\notes' not found!")
        log.info("Created Folder '.\\notes' .")
    
    contain = {"title": title, "text": text, "time": time.strftime(r"%Y.%m.%d %H:%M:%S")}
    filename = "%s_%s_%s.json"%(title, time.strftime(r"%Y%m%d"), time.strftime(r"%Hh%Mm"))
    with open(".\\notes\\"+filename, 'w') as f:
        json.dump(contain, f)
        log.info("Saved '%s' ."%filename)
    return 0

def write():
    writeWid = myWrite()
    writeWid.show()
    return writeWid

def viewAll():
    pass