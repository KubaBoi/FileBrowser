#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import stat
import requests
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
        



# METHODS

    @staticmethod
    def uploadToCloud(path, items, folderObj):
        if (not folderObj["URL"].startswith("http")):
            raise NotRemote()

        url = folderObj["URL"]

        for item in items:
            fileName = ResMan.getFileName(item)
            urlData = f"?name={fileName}&path={path}"

            Logger.info(f"Uploading file {fileName} to {url} as {urlData}")

            with open(item, "rb") as f:
                data = f.read()

            req = requests.post(f"{url}/file/upload{urlData}", data=data)
            if (req.status_code == 200):
                continue
            else:
                return cc.createResponse(json.loads(req.text), req.status_code)

        return cc.createResponse({"STATUS": "ok"}, 200)

    @staticmethod
    def onerror(func, path, exc_info):
        # Is the error an access error?
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

