#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cheese.ErrorCodes import Error
from cheese.modules.cheeseController import CheeseController as cc

#@controller /tree
class TreeController(cc):

	#@get /get
	@staticmethod
	def get(server, path, auth):
		if (auth["role"] > 0):
			Error.sendCustomError(server, "Unauthorized", 400)
			return

		args = cc.getArgs(path)

		if (not cc.validateJson(['folder'], args)):
			Error.sendCustomError(server, "Wrong json structure", 400)
			return

		folder = args["folder"]

		treeModel = TreeRepository.find(folder)
		jsonResponse = {}
		jsonResponse["TREE"] = treeModel.toJson()

		response = cc.createResponse(jsonResponse, 200)
		cc.sendResponse(server, response)

