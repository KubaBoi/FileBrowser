#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import stat
from subprocess import Popen, PIPE
import shutil
from send2trash import send2trash

from Cheese.resourceManager import ResMan
from Cheese.cheeseController import CheeseController as cc

from src.propOpener import PropertiesOpener as po


#@controller /file;
class FileController(cc):

    #@post /copy;
    @staticmethod
    def copy(server, path, auth):
        args = cc.readArgs(server)

        if (not cc.validateJson(["PATH", "ITEMS"], args)):
            return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

        folder = args["PATH"]
        items = args["ITEMS"]

        if (not os.path.exists(folder)):
            return cc.createResponse({"ERROR": "Folder not found"}, 404)

        for item in items:
            if (os.path.isfile(item)):
                shutil.copy2(item, folder)
            elif (os.path.isdir(item)):
                shutil.copytree(item, os.path.join(folder, ResMan.getFileName(item)))

        return cc.createResponse({"STATUS": "ok"}, 200)

    #@post /move;
    @staticmethod
    def move(server, path, auth):
        args = cc.readArgs(server)

        if (not cc.validateJson(["PATH", "ITEMS"], args)):
            return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

        folder = args["PATH"]
        items = args["ITEMS"]

        if (not os.path.exists(folder)):
            return cc.createResponse({"ERROR": "Folder not found"}, 404)

        for item in items:
            if (os.path.isfile(item)):
                shutil.copy2(item, folder)
                if (os.path.exists(os.path.join(folder, ResMan.getFileName(item)))):
                    os.remove(item)
            elif (os.path.isdir(item)):
                shutil.copytree(item, os.path.join(folder, ResMan.getFileName(item)))
                if (os.path.exists(os.path.join(folder, ResMan.getFileName(item)))):
                    shutil.rmtree(item, onerror=FileController.onerror)

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@get /openAs;
    @staticmethod
    def openAs(server, path, auth):
        args = cc.getArgs(path)

        if (not cc.validateJson(["path"], args)):
            return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

        file = args["path"]

        if (not os.path.exists(file)):
            return cc.createResponse({"ERROR": "Folder not found"}, 404)

        command = f"powershell.exe RUNDLL32.EXE SHELL32.DLL,OpenAs_RunDLL \"{file}\""

        p = Popen(command, stdout=sys.stdout, shell=True)
        p.communicate()

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@post /remove;
    @staticmethod
    def remove(server, path, auth):
        args = cc.readArgs(server)

        if (not cc.validateJson(["PATH", "FILES"], args)):
            return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

        files = args["FILES"]
        path = args["PATH"]

        for file in files:
            send2trash(file)

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@get /rename;
    @staticmethod
    def rename(server, path, auth):
        args = cc.getArgs(path)

        if (not cc.validateJson(["path", "newName"], args)):
            return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

        file = args["path"]
        newName = args["newName"]

        if (not os.path.exists(file)):
            return cc.createResponse({"ERROR": "File not found"}, 404)

        os.rename(file, os.path.join(*file.split("\\")[:-1], newName).replace("C:", "C:\\"))

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@get /properties;
    @staticmethod
    def properties(server, path, auth):
        args = cc.getArgs(path)

        if (not cc.validateJson(["path"], args)):
            return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

        file = args["path"]

        if (not os.path.exists(file)):
            return cc.createResponse({"ERROR": "File not found"}, 404)

        po.open(file)

        return cc.createResponse({"STATUS": "ok"}, 200)
        

    #@get /mkdir;
    @staticmethod
    def mkdir(server, path, auth):
        args = cc.getArgs(path)

        if (not cc.validateJson(["path"], args)):
            return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

        folder = args["path"]

        if (not os.path.exists(folder)):
            return cc.createResponse({"ERROR": "Folder not found"}, 404)

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

        if (not cc.validateJson(["path"], args)):
            return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

        folder = args["path"]

        if (not os.path.exists(folder)):
            return cc.createResponse({"ERROR": "Folder not found"}, 404)

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
    def onerror(func, path, exc_info):
        # Is the error an access error?
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

