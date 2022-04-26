#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import Popen, PIPE
import shutil
from send2trash import send2trash

from cheese.ErrorCodes import Error
from cheese.resourceManager import ResMan
from cheese.modules.cheeseController import CheeseController as cc

from python.propOpener import PropertiesOpener as po


#@controller /file
class FileController(cc):

    #@post /copy
    @staticmethod
    def copy(server, path, auth):
        if (auth["role"] > 0):
            Error.sendCustomError(server, "Unauthorized", 401)
            return

        args = cc.readArgs(server)

        if (not cc.validateJson(["FOLDER", "ITEMS"], args)):
            Error.sendCustomError(server, "Wrong json structure", 400)
            return

        folder = args["FOLDER"].replace("%20", " ")
        items = args["ITEMS"]

        if (not os.path.exists(folder)):
            Error.sendCustomError(server, "Folder not found", 404)
            return

        for item in items:
            item = item.replace("%20", " ")
            if (os.path.isfile(item)):
                shutil.copy2(item, folder)
            elif (os.path.isdir(item)):
                shutil.copytree(item, os.path.join(folder, ResMan.getFileName(item)))

        response = cc.createResponse({"STATUS": "ok"}, 200)
        cc.sendResponse(server, response)

    #@post /move
    @staticmethod
    def move(server, path, auth):
        if (auth["role"] > 0):
            Error.sendCustomError(server, "Unauthorized", 401)
            return

        args = cc.readArgs(server)

        if (not cc.validateJson(["FOLDER", "ITEMS"], args)):
            Error.sendCustomError(server, "Wrong json structure", 400)
            return

        folder = args["FOLDER"].replace("%20", " ")
        items = args["ITEMS"]

        if (not os.path.exists(folder)):
            Error.sendCustomError(server, "Folder not found", 404)
            return

        for item in items:
            item = item.replace("%20", " ")
            if (os.path.isfile(item)):
                shutil.copy2(item, folder)
                if (os.path.exists(os.path.join(folder, ResMan.getFileName(item)))):
                    os.remove(item)
            elif (os.path.isdir(item)):
                shutil.copytree(item, os.path.join(folder, ResMan.getFileName(item)))
                if (os.path.exists(os.path.join(folder, ResMan.getFileName(item)))):
                    shutil.rmtree(item, onerror=FileController.onerror)

        response = cc.createResponse({"STATUS": "ok"}, 200)
        cc.sendResponse(server, response)

    #@get /openAs
    @staticmethod
    def openAs(server, path, auth):
        if (auth["role"] > 0):
            Error.sendCustomError(server, "Unauthorized", 401)
            return

        args = cc.getArgs(path)

        if (not cc.validateJson(["file"], args)):
            Error.sendCustomError(server, "Wrong json structure", 400)
            return

        file = args["file"].replace("%20", " ")

        if (not os.path.exists(file)):
            Error.sendCustomError(server, "Folder not found", 404)
            return

        command = f"powershell.exe RUNDLL32.EXE SHELL32.DLL,OpenAs_RunDLL \"{file}\""

        p = Popen(command, stdout=sys.stdout, shell=True)
        p.communicate()

        response = cc.createResponse({"STATUS": "ok"}, 200)
        cc.sendResponse(server, response)

    #@post /remove
    @staticmethod
    def remove(server, path, auth):
        if (auth["role"] > 0):
            Error.sendCustomError(server, "Unauthorized", 401)
            return

        args = cc.readArgs(server)

        if (not cc.validateJson(["FILES"], args)):
            Error.sendCustomError(server, "Wrong json structure", 400)
            return

        files = args["FILES"]

        for file in files:
            send2trash(file)

        response = cc.createResponse({"STATUS": "ok"}, 200)
        cc.sendResponse(server, response)

    #@get /rename
    @staticmethod
    def rename(server, path, auth):
        if (auth["role"] > 0):
            Error.sendCustomError(server, "Unauthorized", 401)
            return

        args = cc.getArgs(path)

        if (not cc.validateJson(["file", "newName"], args)):
            Error.sendCustomError(server, "Wrong json structure", 400)
            return

        file = args["file"].replace("%20", " ")
        newName = args["newName"].replace("%20", " ")

        if (not os.path.exists(file)):
            Error.sendCustomError(server, "File not found", 404)
            return

        os.rename(file, os.path.join(*file.split("\\")[:-1], newName).replace("C:", "C:\\"))

        response = cc.createResponse({"STATUS": "ok"}, 200)
        cc.sendResponse(server, response)

    #@get /properties
    @staticmethod
    def properties(server, path, auth):
        if (auth["role"] > 0):
            Error.sendCustomError(server, "Unauthorized", 401)
            return

        args = cc.getArgs(path)

        if (not cc.validateJson(["file"], args)):
            Error.sendCustomError(server, "Wrong json structure", 400)
            return

        file = args["file"].replace("%20", " ")

        if (not os.path.exists(file)):
            Error.sendCustomError(server, "File not found", 404)
            return

        po.open(file)

        response = cc.createResponse({"STATUS": "ok"}, 200)
        cc.sendResponse(server, response)


# METHODS

    @staticmethod
    def onerror(func, path, exc_info):
        import stat
        # Is the error an access error?
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise
