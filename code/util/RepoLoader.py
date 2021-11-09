from service.Crawler import Crawler
from util.ConfigDealer import ConfigDealer
from math import ceil
from pandas import concat
from util.RepoGenerator import RepoGenerator
from util.decorator.reportLoaderDecorator import catch_repo_loader_error


class RepoLoader(object):
    def __init__(self, language, num, data, per_page=60, start_page=0):
        self.language = language
        self.num = num
        self.data = data
        self.per_page = per_page
        self.start_page = start_page
        self.crawler = Crawler(' ', ' ',0,"hot repo")

    @catch_repo_loader_error
    def get_popular_repo(self):
        pages = ceil(self.num / self.per_page)
        for i in range(self.start_page, self.start_page + pages):
            result = self.get_popular_repo_per_page(i)
            self.data = concat([self.data, result])
        self.data.drop_duplicates(inplace=True)
        ConfigDealer.store_local_repos(self.data)

    def get_popular_repo_per_page(self, cur_page):
        result = self.crawler.get_popular_repo_per_page(self.language, cur_page, self.per_page)
        page_data = RepoGenerator.generate_repo_header(result)
        return page_data

    @classmethod
    def init(cls, data, language, num,
             per_page=ConfigDealer.get_per_page_for_hot_repo(), start_page=0):
        loader = RepoLoader(language, num, data, per_page, start_page)
        loader.get_popular_repo()
        return loader.data
