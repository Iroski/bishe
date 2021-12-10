# -*- coding: utf-8 -*-

from util.DataGenerator import DataGenerator
import pandas as pd
from service.DataService import DataService
from service.Crawler import Crawler
from util.DataSetGenerator import DataSetGenerator
from util.decorator.dataLoaderDecorator import catch_data_loader_error
from pprint import pprint
import threading

REPO_IS_LATEST = -3


class DataLoader:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.crawler = Crawler(owner, repo)
        self.df = pd.DataFrame(columns=['label', 'str'])

    def get_pr_page_results(self) -> list:
        page = 1
        items = self.crawler.get_pr_page_results(page)
        while len(items) != 0:
            result = []
            for item in items:
                # todo 新增一个处理数据方法
                result.append(DataSetGenerator.generate_set_info(item,self.crawler))
            yield result
            page += 1
            items = self.crawler.get_pr_page_results(page)

    @catch_data_loader_error
    def get_result(self):
        if self.crawler.validate_repo():
            for results in self.get_pr_page_results():
                tmp_df = pd.DataFrame(results,columns=['str'])
                tmp_df['label']=0
                tmp_df=tmp_df.iloc[:,[1,0]]
                self.df=self.df.append(tmp_df,ignore_index=True)
        self.df.to_csv('test.tsv', index=False, sep='\t')

    def test_pr_results(self) -> None:
        result = self.get_pr_page_results()


def start_getting_info(arg):
    # pprint(threading.current_thread().name)
    # pprint("1")
    # pprint(arg[0])
    # pprint(arg[1])
    a = DataLoader(arg[0], arg[1])
    a.get_result()
