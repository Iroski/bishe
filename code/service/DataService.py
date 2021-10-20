import Crawler
from dao.DataDao import DataDao


class DataService(object):
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.data_Dao = DataDao()

    def validate_repo_latest(self, results):
        if not results:
            print("[WARNING]: " + self.owner + " " + self.repo + " cannot get prs")
            return True
        if not self.data_Dao.is_repo_exist(self.owner, self.repo):
            return False, -1
        firstNum = results[0]["number"]
        dbMaxNum = self.data_Dao.find_repo_max_pr(self.owner, self.repo)
        return firstNum == dbMaxNum, dbMaxNum

    def insert_or_update_repo(self, results, crawler: Crawler.Crawler):
        if self.data_Dao.is_repo_exist(self.owner, self.repo):
            return self.update_repo(results)
        else:
            item = crawler.get_repo_info()
            item["diff_list"] = results
            return self.insert_repo(item)

    def insert_repo(self, results):
        return self.data_Dao.insert_data(results)

    def update_repo(self, results):
        item = self.data_Dao.find_repo(self.owner, self.repo)
        item["diff_list"].append(results)
        return self.data_Dao.update_data(item)
