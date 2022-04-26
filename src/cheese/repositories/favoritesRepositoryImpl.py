#!/usr/bin/env python
# -*- coding: utf-8 -*-
#AUTOGENERATED FILE

from cheese.databaseControll.database import Database
from cheese.Logger import Logger
from python.models.favorites import Favorites


class FavoritesRepositoryImpl:

    @staticmethod
    def init():
        FavoritesRepositoryImpl.table = "favorites"
        FavoritesRepositoryImpl.scheme = "(id,name,path)"
        FavoritesRepositoryImpl.schemeNoBrackets = "id,name,path"

    @staticmethod
    def convert(var):
        if (type(var) is int):
            var = int(var)
        elif (type(var) is float):
            var = float(var)
        return var

    @staticmethod
    def toJson(object):
        scheme = FavoritesRepositoryImpl.schemeNoBrackets.split(",")
        ret = {}
        for s, o in zip(scheme, list(object)):
            try:
                ret[s] = int(o)
            except:
                ret[s] = o
        return ret

    @staticmethod
    def toModel(obj):
        model = Favorites()
        model.id = FavoritesRepositoryImpl.convert(obj[0])
        model.name = FavoritesRepositoryImpl.convert(obj[1])
        model.path = FavoritesRepositoryImpl.convert(obj[2])
        return model

    @staticmethod
    def fromModel(model):
        tuple = (
            model.id,
            model.name,
            model.path
        )
        return tuple

    @staticmethod
    def findAll(args):

        response = None
        try:
            db = Database()
            response = db.query(f"select {FavoritesRepositoryImpl.schemeNoBrackets} from favorites;")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

            raise SystemError("An error occurred while query request", e)

        if (response == None): return response
        resp = []
        for a in response:
            resp.append(FavoritesRepositoryImpl.toModel(a))
        return resp

    @staticmethod
    def find(args):
        id = args[0]

        response = None
        try:
            db = Database()
            response = db.query(f"select {FavoritesRepositoryImpl.schemeNoBrackets} from favorites where id={id};")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

            raise SystemError("An error occurred while query request", e)

        if (response == None): return response
        if (len(response) > 0):
            return FavoritesRepositoryImpl.toModel(response[0])
        else: return None

    @staticmethod
    def findBy(args):
        columnName = args[0]
        value = args[1]

        response = None
        try:
            db = Database()
            response = db.query(f"select {FavoritesRepositoryImpl.schemeNoBrackets} from favorites where {columnName}={value};")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

            raise SystemError("An error occurred while query request", e)

        if (response == None): return response
        resp = []
        for a in response:
            resp.append(FavoritesRepositoryImpl.toModel(a))
        return resp

    @staticmethod
    def findNewId(args):

        response = None
        try:
            db = Database()
            response = db.query(f"select max(id) from {FavoritesRepositoryImpl.table};")
            db.done()
        except Exception as e:
            Logger.fail("An error occurred while query request", str(e))

            raise SystemError("An error occurred while query request", e)

        if (response == None): return response
        try: return int(response[0][0])
        except: return -1

    @staticmethod
    def save(args):
        obj = FavoritesRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"insert into {FavoritesRepositoryImpl.table} {FavoritesRepositoryImpl.scheme} values {obj};")
            db.done()
            return True
        except Exception as e:
            Logger.fail("An error occurred while commit request", str(e))
            return False

    @staticmethod
    def update(args):
        obj = FavoritesRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"update {FavoritesRepositoryImpl.table} set {FavoritesRepositoryImpl.scheme} = {obj} where id={obj[0]};")
            db.done()
            return True
        except Exception as e:
            Logger.fail("An error occurred while commit request", str(e))
            return False

    @staticmethod
    def delete(args):
        obj = FavoritesRepositoryImpl.fromModel(args[0])

        try:
            db = Database()
            db.commit(f"delete from {FavoritesRepositoryImpl.table} where id={obj[0]};")
            db.done()
            return True
        except Exception as e:
            Logger.fail("An error occurred while commit request", str(e))
            return False

