#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cheese.ErrorCodes import Error
from cheese.resourceManager import ResMan
from cheese.modules.cheeseController import CheeseController as cc

from python.iconFinder import IconFinder

#@controller /main
class MainController(cc):

	#@get /init
	@staticmethod
	def init(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 401)
			return

		homeFolder = "C:\\Users\\Jakub Anderle\\Downloads"

		response = cc.createResponse({"PATH": homeFolder}, 200)
		cc.sendResponse(server, response)

	#@get /ls
	@staticmethod
	def ls(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 401)
			return

		args = cc.getArgs(path)

		if (not cc.validateJson(['folder'], args)):
			Error.sendCustomError(server, "Wrong json structure", 400)
			return

		folder = args["folder"].replace("%20", " ")

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
						"IMAGE": icon.find(name.split(".")[-1]) + "Icon.png",
						"SIZE": ResMan.convertBytes(os.path.getsize(os.path.join(root, name))),
						"TYPE": "FILE"
					}
				)
			break
			

		response = cc.createResponse(jsonResponse, 200)
		cc.sendResponse(server, response)

	#@get /open
	@staticmethod
	def open(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 401)
			return

		args = cc.getArgs(path)

		if (not cc.validateJson(['file'], args)):
			Error.sendCustomError(server, "Wrong json structure", 400)
			return

		file = args["file"].replace("%20", " ")

		os.startfile(file)

		response = cc.createResponse({'STATUS': 'ok'}, 200)
		cc.sendResponse(server, response)

	#@get /file
	@staticmethod
	def file(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 401)
			return

		args = cc.getArgs(path)

		if (not cc.validateJson(['file'], args)):
			Error.sendCustomError(server, "Wrong json structure", 400)
			return

		file = args["file"]

		response = cc.createResponse({'FILE': {'NAME': 'str', 'CONTENT': 'str'}}, 200)
		cc.sendResponse(server, response)


	# METHODS

	def getSize(startPath = '.'):
		return 0
		total_size = 0
		for dirpath, dirnames, filenames in os.walk(startPath):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				# skip if it is symbolic link
				if not os.path.islink(fp):
					total_size += os.path.getsize(fp)

		return total_size
