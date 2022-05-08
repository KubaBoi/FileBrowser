#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from Cheese.ErrorCodes import Error
from Cheese.resourceManager import ResMan
from Cheese.appSettings import Settings
from Cheese.cheeseController import CheeseController as cc

from src.repositories.favoritesRepository import FavoritesRepository

from src.iconFinder import IconFinder

#@controller /main;
class MainController(cc):

	#@get /init;
	@staticmethod
	def init(server, path, auth):
		homeFolder = Settings.settings["initPath"]
		root = Settings.settings["root"]

		return cc.createResponse({"ROOT": root, "PATH": homeFolder}, 200)

	#@get /ls;
	@staticmethod
	def ls(server, path, auth):
		args = cc.getArgs(path)

		if (not cc.validateJson(["path"], args)):
			return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

		folder = args["path"]

		jsonResponse = {}
		jsonResponse["FOLDER"] = []

		icon = IconFinder()

		for root, dirs, files in os.walk(folder):
			for name in dirs:
					jsonResponse["FOLDER"].append(
					{
						"NAME": name,
						"IMAGE": "folder.png",
						"SIZE": "",
						"TYPE": "FOLDER"
					}
				)

			for name in files:
				jsonResponse["FOLDER"].append(
					{
						"NAME": name,
						"IMAGE": icon.find(os.path.join(root, name)),
						"SIZE": ResMan.convertBytes(os.path.getsize(os.path.join(root, name))),
						"TYPE": "FILE"
					}
				)
			break
			

		return cc.createResponse(jsonResponse, 200)

	#@get /open;
	@staticmethod
	def open(server, path, auth):
		args = cc.getArgs(path)

		if (not cc.validateJson(["path"], args)):
			return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

		file = args["path"]

		os.startfile(file)

		return cc.createResponse({'STATUS': 'ok'}, 200)

	#@get /exists;
	@staticmethod
	def exists(server, path, auth):
		args = cc.getArgs(path)

		if (not cc.validateJson(["path"], args)):
			return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

		file = args["path"]

		return cc.createResponse({'EXISTS': os.path.exists(file)}, 200)

	#TODO
	#@get /file;
	@staticmethod
	def file(server, path, auth):
		args = cc.getArgs(path)

		if (not cc.validateJson(["path"], args)):
			return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

		file = args["path"]

		return cc.createResponse({'FILE': {'NAME': 'str', 'CONTENT': 'str'}}, 200)

	#@get /favorites;
	@staticmethod
	def favorites(server, path, auth):
		fav = FavoritesRepository.findAll()

		jsonResponse = cc.modulesToJsonArray(fav)

		return cc.createResponse({"FAVOURITES": jsonResponse}, 200)

	#@get /cmd;
	@staticmethod
	def file(server, path, auth):
		args = cc.getArgs(path)

		if (not cc.validateJson(['path'], args)):
			return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

		path = args["path"]
		if (not os.path.exists(path)):	
			return cc.createResponse({"ERROR": "Folder not found"}, 404)

		command = f"start cmd /K cd \"{path}\""
		os.system(command)

		return cc.createResponse({"STATUS": "ok"}, 200)

	#@get /code;
	@staticmethod
	def code(server, path, auth):
		args = cc.getArgs(path)

		if (not cc.validateJson(['path'], args)):
			return cc.createResponse({"ERROR": "Wrong json structure"}, 400)

		path = args["path"]
		if (not os.path.exists(path)):	
			return cc.createResponse({"ERROR": "Folder not found"}, 404)

		command = f"code -n \"{path}\""
		os.system(command)

		return cc.createResponse({"STATUS": "ok"}, 200)

	# METHODS
