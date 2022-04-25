#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import requests
from pathlib import Path

from cheese.resourceManager import ResMan
from cheese.appSettings import Settings
from cheese.server.cheeseServer import *
from cheese.databaseControll.database import Database
from cheese.modules.cheeseRepository import CheeseRepository
from cheese.ErrorCodes import Error
from cheese.Logger import Logger
"""
File generated by Cheese Framework

initialize Cheese Application
"""

class Cheese:

    @staticmethod
    def init():
        # initialization of root directory
        ResMan.setPath(Path(__file__).parent.parent.parent)

        # loads application settings
        Settings.loadSettings()

        #init logger
        Logger.initLogger()

        # init errors
        Error.init()

        # check licence
        Cheese.loadLicence()
        Cheese.printInit()

        # log new line
        Logger.info(10*"=" + f"Start in file {ResMan.path}" + 10*"=" + "\n", False, False)

        # connect to database
        if (Settings.allowDB):
            Logger.warning("Initializing database connection...", silence=False)
            try:
                db = Database()
                db.connect()
                db.close()
                Logger.okBlue(f"CONNECTED TO {Settings.dbHost}:{Settings.dbPort} {Settings.dbName}", silence=False)
            except Exception as e:
                Logger.fail(f"CONNECTION TO {Settings.dbHost}:{Settings.dbPort} {Settings.dbName} CANNOT BE DONE:{Logger.WARNING}\n{str(e)}", silence=False)
        else:
            Logger.warning("Database connection is turned off", silence=False)

        #initialization of repositories
        CheeseRepository.initRepositories()

        # initialization of server
        Cheese.initServer()

    # initialization application server
    @staticmethod
    def initServer():
        if (Settings.allowMultiThreading):
            Cheese.server = CheeseServerMulti((Settings.host, Settings.port), CheeseHandler)
        else:
            Cheese.server = CheeseServer((Settings.host, Settings.port), CheeseHandler)

    # start server
    @staticmethod
    def serveForever():
        Logger.info(f"Server Starts - {Settings.host}:{Settings.port}", silence=False)
        try:
            Cheese.server.serve_forever()
        except KeyboardInterrupt:
            pass
        except OSError:
            Logger.warning("SHUTING SERVER DOWN")
        except Exception as e:
            Logger.fail("UNKNOWN ERROR WHILE RUNNING SERVER ", e)
        Logger.info(f"Server Stops - {Settings.host}:{Settings.port}", silence=False)
        sys.exit()

    # init print
    @staticmethod
    def printInit():
        with open(f"{ResMan.cheese()}/initString.txt", "r") as f:
            print(f.read())
        with open(f"{ResMan.cheese()}/cheeseproperties.json", "r") as f:
            properties = json.loads(f.read())
            print(f"Cheese Framework            (v{properties['release']})")
            print(properties['documentation'])
            print("License: " + Settings.activeLicense)
            print("")

    # loads licence
    @staticmethod
    def loadLicence():
        try:
            r = requests.get(f"http://frogie.cz:6969/licence/authLic?code={Settings.licenseCode}")
            Settings.activeLicense = json.loads(r.text)["LICENCE"]
        except Exception as e:
            Logger.warning("Unable to contact licensing server", silence=False)

    

