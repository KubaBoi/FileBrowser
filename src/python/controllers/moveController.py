#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.ErrorCodes import Error
from cheese.modules.cheeseController import CheeseController as cc

#@controller /move
class MoveController(cc):

	#@get /in
	@staticmethod
	def inside(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 400)
			return

		args = cc.getArgs(path)

		if (not cc.validateJson(['folder'], args)):
			Error.sendCustomError(server, "Wrong json structure", 400)
			return

		folder = args["folder"]

		

		response = cc.createResponse({'FOLDER': [{'NAME': 'str', 'SIZE': 0}]}, 200)
		cc.sendResponse(server, response)

	#@get /out
	@staticmethod
	def out(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 400)
			return

		args = cc.getArgs(path)

		if (not cc.validateJson(['folder'], args)):
			Error.sendCustomError(server, "Wrong json structure", 400)
			return

		folder = args["folder"]

		response = cc.createResponse({'FOLDER': [{'NAME': 'str', 'SIZE': 0}]}, 200)
		cc.sendResponse(server, response)

