# -*- coding: utf-8 -*-

from util.DataGenerator import DataGenerator
from service.DataService import DataService
from service.Crawler import Crawler
from pprint import pprint

class DataLoader:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.data_service = DataService(self.owner, self.repo)
        self.crawler = Crawler(owner, repo)


    def get_pr_page_results(self) -> list:
        result = []
        if not self.crawler.validate_repo():
            return result

        for items in self.crawler.get_pr_page_results_not_deal():
            result = []
            for item in items:
                result.append(DataGenerator.generate_diff_data(item))
            yield result

    def get_result(self):
        label = -1
        is_latest, dbMaxNum = self.data_service.validate_repo_latest(self.crawler.get_max_pr_num())
        if is_latest:
            print("没有更新的repo")
            return
        for results in self.get_pr_page_results():
            for i in range(len(results)):
                if results[i]["number"] == dbMaxNum:  # 当前i项是已有的
                    label = -1
                    break
                results[i] = self.crawler.deal_diff(results[i])
            if label != -1:
                results = results[:label]

            self.data_service.insert_or_update_repo(results, self.crawler)

    def test_pr_results(self) -> None:
        result = self.get_pr_page_results()
        with open('../test/pr.txt', 'w')as f:
            print(result, file=f)


def start_getting_info(arg):
    # pprint("1")
    # pprint(arg[0])
    # pprint(arg[1])
    a = DataLoader(arg[0], arg[1])
    a.get_result()
