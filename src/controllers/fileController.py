#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import stat
import requests
import time
import json
from subprocess import Popen, PIPE
import shutil
from send2trash import send2trash

from Cheese.resourceManager import ResMan
from Cheese.cheeseController import CheeseController as cc
from Cheese.Logger import Logger
from Cheese.httpClientErrors import *
from Cheese.httpServerError import *

from src.propOpener import PropertiesOpener as po

class NotRemote(Exception):
    def __init__(self):
        self.description = "Host is not remote"
        self.name = "Not Remote"

#@controller /file;
class FileController(cc):

    uploadStatusDic = {}

    #@post /copy;
    @staticmethod
    def copy(server, path, auth):
        args = cc.readArgs(server)

        cc.checkJson(["PATH", "ITEMS", "FOLDER", "ORIGINS"], args)

        folder = args["PATH"]
        items = args["ITEMS"]
        folderObj = args["FOLDER"]
        origins = args["ORIGINS"]

        try:
            return FileController.uploadToCloud(folder, items, folderObj)
        except NotRemote as e:
            pass

        if (not os.path.exists(folder)):
            raise NotFound("Folder not found")

        for item, origin in zip(items, origins):
            if (origin["URL"] == ""):
                if (os.path.isfile(item)):
                    shutil.copy2(item, folder)
                elif (os.path.isdir(item)):
                    shutil.copytree(item, os.path.join(folder, ResMan.getFileName(item)))
            else:
                req = requests.get(f"{origin['URL']}/file/download?file={item}")
                if (req.status_code != 200):
                    return cc.createResponse(json.loads(req.text), req.status_code)
                else:
                    with open(ResMan.joinPath(folder, ResMan.getFileName(item)), "wb") as f:
                        f.write(req.content)

        return cc.createResponse({"STATUS": "ok"}, 200)

    #@post /move;
    @staticmethod
    def move(server, path, auth):
        args = cc.readArgs(server)

        cc.checkJson(["PATH", "ITEMS", "FOLDER"], args)

        folder = args["PATH"]
        items = args["ITEMS"]
        folderObj = args["FOLDER"]
        origins = args["ORIGINS"]

        try:
            return FileController.uploadToCloud(folder, items, folderObj)
        except NotRemote as e:
            pass

        if (not os.path.exists(folder)):
            raise NotFound("Folder not found")

        for item, origin in zip(items, origins):
            if (origin["URL"] == ""):
                if (os.path.isfile(item)):
                    shutil.copy2(item, folder)
                    if (os.path.exists(os.path.join(folder, ResMan.getFileName(item)))):
                        os.remove(item)
                elif (os.path.isdir(item)):
                    shutil.copytree(item, os.path.join(folder, ResMan.getFileName(item)))
                    if (os.path.exists(os.path.join(folder, ResMan.getFileName(item)))):
                        shutil.rmtree(item, onerror=FileController.onerror)
            else:
                req = requests.get(f"{origin['URL']}/file/download?file={item}")
                if (req.status_code != 200):
                    return cc.createResponse(json.loads(req.text), req.status_code)
                else:
                    with open(ResMan.joinPath(folder, ResMan.getFileName(item)), "wb") as f:
                        f.write(req.content)

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@get /openAs;
    @staticmethod
    def openAs(server, path, auth):
        args = cc.getArgs(path)

        cc.checkJson(["path"], args)

        file = args["path"]

        if (not os.path.exists(file)):
            raise NotFound("Folder not found")

        command = f"powershell.exe RUNDLL32.EXE SHELL32.DLL,OpenAs_RunDLL \"{file}\""

        p = Popen(command, stdout=sys.stdout, shell=True)
        p.communicate()

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@post /remove;
    @staticmethod
    def remove(server, path, auth):
        args = cc.readArgs(server)

        cc.checkJson(["PATH", "FILES"], args)

        files = args["FILES"]
        path = args["PATH"]

        for file in files:
            send2trash(file)

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@get /rename;
    @staticmethod
    def rename(server, path, auth):
        args = cc.getArgs(path)

        cc.checkJson(["path", "newName"], args)

        file = args["path"]
        newName = args["newName"]

        if (not os.path.exists(file)):
            raise NotFound("File not found")

        os.rename(file, os.path.join(*file.split("\\")[:-1], newName).replace("C:", "C:\\"))

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@get /properties;
    @staticmethod
    def properties(server, path, auth):
        args = cc.getArgs(path)

        cc.checkJson(["path"], args)

        file = args["path"]

        if (not os.path.exists(file)):
            raise NotFound("File not found")

        po.open(file)

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@get /mkdir;
    @staticmethod
    def mkdir(server, path, auth):
        args = cc.getArgs(path)

        cc.checkJson(["path"], args)

        folder = args["path"]

        if (not os.path.exists(folder)):
            raise NotFound("Folder not found")

        folderName = "New folder"
        actFolderName = folderName
        id = 0
        while (os.path.exists(os.path.join(folder, actFolderName))):
            id += 1
            actFolderName = f"{folderName} ({str(id)})"

        os.mkdir(os.path.join(folder, actFolderName))

        return cc.createResponse({"FOLDER": actFolderName}, 200)
        

    #@get /write;
    @staticmethod
    def write(server, path, auth):
        args = cc.getArgs(path)

        cc.checkJson(["path"], args)

        folder = args["path"]

        if (not os.path.exists(folder)):
            raise NotFound("Folder not found")

        folderName = "New file"
        actFolderName = folderName + ".txt"
        id = 0
        while (os.path.exists(os.path.join(folder, actFolderName))):
            id += 1
            actFolderName = f"{folderName} ({str(id)}).txt"

        open(os.path.join(folder, actFolderName), "w")

        return cc.createResponse({"FILE": actFolderName}, 200)
        
    #@get /uploadStatus;
    @staticmethod
    def uploadStatus(server, path, auth):
        args = cc.getArgs(path)
        cc.checkJson(["windowId", "oldComment"], args)

        windowId = args["windowId"]
        oldComment = args["oldComment"]

        if (windowId not in FileController.uploadStatusDic.keys()):
            raise NotFound("Session was not found")


        session = FileController.uploadStatusDic[windowId]
        if (session[0] == "Upload done"):
            resp = cc.createResponse({"STATUS": session[0], "SIZE": ResMan.convertBytes(session[2])}, 200)
            FileController.uploadStatusDic.pop(windowId)
            return resp

        oldPerc = session[3]
        while (oldComment == session[0] and oldPerc == session[3]):
            time.sleep(0.1)
            session = FileController.uploadStatusDic[windowId]

        return cc.createResponse({
                "STATUS": session[0],
                "TRANSFERED": ResMan.convertBytes(session[1]),
                "SIZE": ResMan.convertBytes(session[2]),
                "PERCENT": session[3],
                "SPEED": ResMan.convertBytes(session[4])
            }, 200)


# METHODS

    @staticmethod
    def changeStatus(comment, folderObj, transfered=0, percent=0, uploadTime=0):
        obj = FileController.uploadStatusDic[folderObj["DIV_ID"]]
        transfered += obj[1]

        FileController.uploadStatusDic[folderObj["DIV_ID"]] = (comment, int(transfered), int(obj[2]), int(percent), uploadTime)

    @staticmethod
    def uploadToCloud(path, items, folderObj):
        if (not folderObj["URL"].startswith("http")):
            raise NotRemote()

        totalSize = 0
        FileController.uploadStatusDic[folderObj["DIV_ID"]] = ("Calculating size...", 0, 0, 0, 0)
        for item in items:
            totalSize += FileController.getSize(item)

        FileController.uploadStatusDic[folderObj["DIV_ID"]] = ("Uploading...", 0, totalSize, 0, 0)

        resp = FileController.uploadFileToCloud(path, items, folderObj)
        FileController.changeStatus("Upload done", folderObj)
        return resp

    @staticmethod
    def uploadFileToCloud(path, items, folderObj):
        url = folderObj["URL"]

        for item in items:
            name = ResMan.getFileName(item)
            if (os.path.isdir(item)):
                pth = ResMan.joinPath(path)
                Logger.info(f"Making cloud directory: {pth}, {name}")
                FileController.changeStatus(f"Making directory {name}", folderObj)

                req = requests.get(f"{url}/file/mkdir?path={pth}&name={name}")
                if (req.status_code != 200):
                    Logger.fail(req.text)
                    return cc.createResponse(json.loads(req.text), req.status_code)

                itms = []
                for root, dirs, files in os.walk(item):
                    for dir in dirs:
                        itms.append(ResMan.joinPath(root, dir))
                    for file in files:
                        itms.append(ResMan.joinPath(root, file))
                    break
                FileController.uploadFileToCloud(ResMan.joinPath(path, name), itms, folderObj)
            else:
                urlData = f"?name={name}&path={path}"

                Logger.info(f"Uploading file {name} to {url} as {urlData}")

                uploader = Uploader(item, folderObj, 1024)

                req = requests.post(f"{url}/file/upload{urlData}", data=uploader)
                if (req.status_code != 200):
                    Logger.fail(req.text)
                    return cc.createResponse(json.loads(req.text), req.status_code)

        return cc.createResponse({"STATUS": "ok"}, 200)

    @staticmethod
    def getSize(start_path="."):
        total_size = 0

        if (os.path.isdir(start_path)):
            for root, dirs, files in os.walk(start_path):
                for file in files:
                    fp = os.path.join(root, file)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        else:
            return os.path.getsize(start_path)

        return total_size

    @staticmethod
    def onerror(func, path, exc_info):
        # Is the error an access error?
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise


class Uploader:

    def __init__(self, filename, session, chunksize=1 << 13):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0
        self.session = session

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            tm = time.time()
            while True:
                data = file.read(self.chunksize)
                if not data:
                    sys.stderr.write("\n")
                    break
                self.readsofar += len(data)
                percent = self.readsofar * 1e2 / self.totalsize
                yield data
                delay = time.time() - tm
                speed = 0
                if (delay != 0):
                    speed = self.readsofar//delay
                FileController.changeStatus(ResMan.getFileName(self.filename), self.session, len(data), percent, speed)

    def __len__(self):
        return self.totalsize

