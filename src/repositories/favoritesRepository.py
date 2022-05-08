#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cheese.cheeseRepository import CheeseRepository

#@repository favorites;
#@dbscheme (id, name, path);
#@dbmodel Favorites;
class FavoritesRepository(CheeseRepository):



	#GENERATED METHODS

	#@query "select * from favorites;";
	#@return array;
	@staticmethod
	def findAll():
		return CheeseRepository.query()

	#@query "select * from favorites where id=:id;";
	#@return one;
	@staticmethod
	def find(id):
		return CheeseRepository.query(id=id)

	#@query "select * from favorites where :columnName=:value;";
	#@return array;
	@staticmethod
	def findBy(columnName, value):
		return CheeseRepository.query(columName=columnName, value=value)

