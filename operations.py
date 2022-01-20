import json
import time
import easygui as gui
import os

def save(title, text):
    if (not os.path.exists(".\\notes")): 
        os.mkdir(".\\notes")
    
    contain = {"title": title, "text": text, "time": time.strftime(r"%Y.%m.%d %H:%M:%S")}
    filename = ".\\notes\\%s_%s_%s.json"%(title, time.strftime(r"%Y%m%d"), time.strftime(r"%Hh%Mm"))
    if (not gui.ccbox("文件名将是:%s\n确定保存?"%filename, "保存", ("保存", "取消"))):
        gui.msgbox("已取消。")
        return 1
    with open(filename, 'a') as f:
        json.dump(contain, f)
    gui.msgbox("已保存。")
    return 0

def write():
    title = gui.enterbox("输入标题", "新建")
    text = gui.codebox("输入内容", "新建")
    result = save(title, text)

def view():
    pass