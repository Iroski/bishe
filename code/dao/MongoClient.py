import pymongo

from pymongo.errors import ConnectionFailure

from config import TABLE,MONGO_SERVER,MONGO_PORT,MONGO_USERNAME,MONGO_PASSWD


class MongoClient(object):
    def __init__(self):
        self.dbClient = pymongo.MongoClient(host=MONGO_SERVER,port=MONGO_PORT)
        self.check_db_valid()
        self.db = self.dbClient[TABLE]

    @classmethod
    def get_instance(cls):
        if not hasattr(MongoClient, '_instance'):
            MongoClient._instance = MongoClient()
        return MongoClient._instance

    @classmethod
    def init(cls):
        MongoClient._instance=MongoClient()

    def check_db_valid(self):
        try:
            if MONGO_USERNAME is not None and MONGO_PASSWD is not None:
                self.dbClient.admin.authenticate(MONGO_USERNAME, MONGO_PASSWD)
            self.dbClient.admin.command('ping')
        except ConnectionFailure:
            try:
                self.dbClient.admin.command('ping')
            except ConnectionFailure:
                print("mongo db connection fail, please check host, port and proxy")
                return
            print("mongodb username or password is wrong")

