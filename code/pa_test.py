# -*- coding: utf-8 -*-

import json
from util.DataGenerator import DataGenerator
from service.DataService import DataService
from Crawler import Crawler
class DataLoader:
    def __init__(self, owner, repo, diff_path=None, *token):
        assert (owner, str)
        assert (repo, str)
        self.owner = owner
        self.repo = repo
        self.diff_path = 'pr_diff'
        self.data_service = DataService(self.owner, self.repo)
        self.crawler=Crawler(owner,repo,diff_path,token)



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
        checked = False
        dbMaxNum = -1
        label=-1
        for results in self.get_pr_page_results():
            if not checked:
                checked = True
                is_latest, dbMaxNum = self.data_service.validate_repo_latest(results)
                if is_latest:
                    return #没有更新的pr
            for i in range(len(results)):
                if results[i]["number"]==dbMaxNum:#当前i项是已有的
                    label=-1
                    break
                results[i] = self.crawler.deal_diff(results[i])
            if label!=-1:
                results=results[:label]

            self.data_service.insert_or_update_repo(results)

    def test_pr_results(self) -> None:
        result = self.get_pr_page_results()
        with open('test/pr.txt', 'w')as f:
            print(result, file=f)


if __name__ == '__main__':
    a = DataLoader('Iroski', 'SE-group-90')
    a.test_pr_results()
    # results = a.get_pr_results( pr_header)
#     count = 0
#     for item in results:
#         if count is 27 or count is 28:
#             pprint.pprint(item)
#             path = 'pr_json/' + str(140 - count) + '.json'
#             json.dump(item, open(path, "w"))
#             if count is 28:
#                 break
#         count = count + 1
