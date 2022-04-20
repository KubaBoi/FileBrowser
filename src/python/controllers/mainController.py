#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cheese.ErrorCodes import Error
from cheese.modules.cheeseController import CheeseController as cc

#@controller /main
class MainController(cc):

	#@get /ls
	@staticmethod
	def ls(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 400)
			return

		args = cc.getArgs(path)

		if (not cc.validateJson(['folder'], args)):
			Error.sendCustomError(server, "Wrong json structure", 400)
			return

		folder = args["folder"]

		jsonResponse = {}
		jsonResponse["FOLDER"] = []

		for root, dirs, files in os.walk(folder):
			for name in dirs:
					jsonResponse["FOLDER"].append(
					{
						"NAME": name,
						"SIZE": MainController.getSize(os.path.join(folder, name))
					}
				)

			for name in files:
				jsonResponse["FOLDER"].append(
					{
						"NAME": name,
						"SIZE": os.path.getsize(os.path.join(root, name))
					}
				)
			

		response = cc.createResponse(jsonResponse, 200)
		cc.sendResponse(server, response)

	#@get /open
	@staticmethod
	def open(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 400)
			return

		args = cc.getArgs(path)

		if (not cc.validateJson(['file'], args)):
			Error.sendCustomError(server, "Wrong json structure", 400)
			return

		file = args["file"]

		response = cc.createResponse({'STATUS': 'ok'}, 200)
		cc.sendResponse(server, response)

	#@get /file
	@staticmethod
	def file(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 400)
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
		total_size = 0
		for dirpath, dirnames, filenames in os.walk(startPath):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				# skip if it is symbolic link
				if not os.path.islink(fp):
					total_size += os.path.getsize(fp)

		return total_size
