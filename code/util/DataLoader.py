# -*- coding: utf-8 -*-
from time import sleep

from util.DataGenerator import DataGenerator
from service.DataService import DataService
from service.Crawler import Crawler
from util.logUtil import init_logger
from util.decorator.dataLoaderDecorator import catch_data_loader_error
from pprint import pprint
import threading

from util.logUtil import init_logger

REPO_IS_LATEST = -3


class DataLoader:
    def __init__(self, owner, repo, token_ptr,process):
        self.owner = owner
        self.repo = repo
        self.process=process
        self.data_service = DataService(self.owner, self.repo)
        self.crawler = Crawler(owner, repo, token_ptr,process)

    def get_pr_page_results(self) -> list:
        page=1

        items=self.crawler.get_pr_page_results_not_deal(page)
        while len(items) !=0:
            result = []
            for item in items:
                result.append(DataGenerator.generate_diff_data(item))
            yield result
            page+=1
            items = self.crawler.get_pr_page_results_not_deal(page)


    @catch_data_loader_error
    def get_result(self):
        if self.crawler.validate_repo():
            is_latest, dbMaxNum = self.data_service.validate_repo_latest(self.crawler.get_max_pr_num())
            if is_latest:
                return REPO_IS_LATEST
            for results in self.get_pr_page_results():
                if len(results) !=0:
                    if results[-1]["number"] <= dbMaxNum:
                        continue
                    merged_result = []
                    for i in range(len(results)):
                        if results[i]['merged_at'] is None:  # 当前第i项是已有的或者被关闭没有合并
                            continue
                        # 5次访问失败抛出DiffException异常，停止该repo爬取,爬取下一个
                        # 如果是反爬问题会在下一个repo验证中被拦截，停止系统
                        results[i] = self.crawler.deal_diff(results[i])
                        merged_result.append(results[i])
                    if len(merged_result) != 0:
                        self.data_service.insert_or_update_repo(merged_result, self.crawler)

    def test_pr_results(self) -> None:
        result = self.get_pr_page_results()


def start_getting_info(owner,repo,token_ptr,process,log_name):
    # print(owner)
    # print(repo)
    # print(token_ptr)
    # print(process)
    init_logger(log_name)
    a = DataLoader(owner, repo,token_ptr,process)
    a.get_result()
