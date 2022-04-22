#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from cheese.ErrorCodes import Error
from cheese.resourceManager import ResMan
from cheese.modules.cheeseController import CheeseController as cc


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
            shutil.copy2(item, folder)

        response = cc.createResponse({"STATUS": "ok"}, 200)
        cc.sendResponse(server, response)

