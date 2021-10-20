import pymongo
import pprint
import config


class MongoClient(object):
    def __init__(self):
        self.dbClient = pymongo.MongoClient()
        self.db = self.dbClient["bug_lib"]

    @classmethod
    def get_instance(cls):
        if not hasattr(MongoClient, '_instance'):
            MongoClient._instance = MongoClient()
        return MongoClient._instance
