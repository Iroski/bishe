from dao.MongoClient import MongoClient

#todo 考虑是否继续使用单例模式
class DataDao(object):
    sheet = 'item'

    def __init__(self):
        self.db = MongoClient.get_instance().db

    @classmethod
    def get_instance(cls):
        if not hasattr(DataDao, '_instance'):
            DataDao._instance = DataDao()
        return DataDao._instance

    @classmethod
    def find_repo(cls, owner, repo):
        itemCol = cls.get_instance().db[cls.sheet]
        query = {"owner": owner, "name": repo}
        result = itemCol.find_one(query)
        return result

    @classmethod
    def find_repo_max_pr(cls, owner, repo) -> int:
        item = cls.find_repo(owner, repo)
        if item == None:
            return -1
        return item["latest_pr_num"]

    @classmethod
    def is_repo_exist(cls, owner, repo) -> bool:
        return DataDao.find_repo(owner, repo) is not None

    @classmethod
    def insert_data(cls, data) -> bool:
        itemCol = cls.get_instance().db[cls.sheet]
        result = itemCol.insert_one(data)
        return result is not None

    @classmethod
    def update_data(cls, data):
        dataId = data["_id"]
        itemCol = cls.get_instance().db[cls.sheet]
        result = itemCol.update_one({"_id": dataId}, {"$set":{"diff_list":data["diff_list"],"latest_pr_num":data["latest_pr_num"]}})
        return result is not None
