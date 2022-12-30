import logging as log
import time

class Note:
    def __init__(self, title: str, text: str, score=[], time=list(time.localtime(time.time()))):
        if (not self.checkArgs(title, text, time, score)):
            raise ValueError("Invalid note args.")
        
        self.title = title
        self.text = text
        self.ctime = time
        self.score = score
    
    def checkArgs(self, title: str, text: str, ctime: list, score: list):
        titleValid = type(title)==str and len(title)>0
        textValid = type(text)==str
        timeValid = type(ctime)==list and len(ctime)==9
        scoreValid = type(score)==list

        if (titleValid and textValid and timeValid and scoreValid):
            return True
        else:
            log.error("Invalid note args. [%d %d %d %d]"%(titleValid, textValid, timeValid, scoreValid))
            return False
    
    def toDict(self):
        return {"title": self.title, "text": self.text, "time": self.ctime, "score": self.score}
