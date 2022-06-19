#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import win32gui, win32con
import threading
import subprocess
import requests
import time
import json

from Cheese.cheese import CheeseBurger
from Cheese.appSettings import Settings
from Cheese.resourceManager import ResMan

"""
File generated by Cheese Framework

main file of Cheese Application
"""

if ("-nocons" in sys.argv):
    prog = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(prog, win32con.SW_HIDE)

def runFileServer():
    subprocess.call(ResMan.joinPath(ResMan.resources(), "fileServer.bat"))

if __name__ == "__main__":
    CheeseBurger.init()

    i = 0
    while i < 10:
        try:
            req = {
                "name": Settings.name,
                "port": Settings.port,
                "icon": "/images/folder.png",
                "color": "FF0000"
            }
            requests.post(f"http://localhost/services/doYouKnowMe", json=req)
            break
        except:
            i += 1
            time.sleep(1)

    i = 0
    while i < 10:
        break
        try:
            with open(ResMan.resources("iconDictionary.json"), "r") as f:
                data = json.loads(f.read())
            req = {"ICONS": data}
            rep = requests.post("http://frogie.cz:7997/main/syncIconJson", json=req)

            for root, dirs, files in os.walk(ResMan.web("images")):
                for file in files:
                    pth = ResMan.getRelativePathFrom(ResMan.joinPath(root, file), ResMan.web("images"))
                    with open(ResMan.joinPath(root, file), "rb") as f:
                        fileData = f.read()
                    requests.post(f"http://frogie.cz:7997/main/syncIcons?path={pth}", data=fileData)

            break
        except Exception as e:
            print(e)
            i += 1
            time.sleep(1)

    x = threading.Thread(target=runFileServer)
    x.start()

    CheeseBurger.serveForever()