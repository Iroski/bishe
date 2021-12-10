import json

from util.ConfigDealer import ConfigDealer
import os
from util.decorator.crawlerDecorator import *

import requests
from util.DataGenerator import DataGenerator
import ssl

# https://github.com容易访问超时，需要爬取可用ip，但会引发证书失效问题，需要手动关闭证书验证
context = ssl._create_unverified_context()


class Crawler(object):
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.configDealer = ConfigDealer.get_instance()
        self.pr_header, self.diff_header = self.configDealer.get_headers()
        self.diff_path = self.configDealer.get_diff_path()
        self.proxies = self.configDealer.get_proxy()

        self.check_and_make_dirs_exist()

    def check_and_make_dirs_exist(self):
        path = self.diff_path + '/' + self.owner + '/' + self.repo
        if not os.path.exists(path):
            os.makedirs(path)

    @catch_validation_error
    def validate_repo(self):
        # try:
        url = 'https://api.github.com/repos/{owner}/{repo}'.format(
            owner=self.owner, repo=self.repo)
        r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
        result = r.json()
        if 'message' in result:
            return result['message']
        return True

    @catch_get_pr_page_results_not_deal_error
    def get_pr_page_results_not_deal(self, page):
        url = 'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&page={page}&direction=asc'.format(
            owner=self.owner, repo=self.repo, page=page)
        r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
        result = r.json()
        return result

    @catch_get_pr_page_results_not_deal_error
    def get_pr_page_results(self, page):
        url = 'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&page={page}&direction=asc'.format(
            owner=self.owner, repo=self.repo, page=page)
        r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
        result = r.json()
        return result

    @catch_get_issue_error
    def get_issue(self, number):
        url = 'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}'.format(
            owner=self.owner, repo=self.repo, issue_number=str(number))
        r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
        result = r.json()
        return result

    @catch_deal_diff_error
    def deal_diff(self, item):

        path = self.diff_path + self.owner + '\\' + self.repo + '\\' + str(item["number"]) + ".diff"
        url = 'https://github.com/{owner}/{repo}/pull/{number}.diff' \
            .format(owner=self.owner, repo=self.repo, number=item["number"])
        r = requests.get(url, headers=self.diff_header, proxies=self.proxies)
        response = r.text
        with open(path, 'w', encoding='utf-8') as f:
            print(response, file=f)
        item["diff_local_path"] = path
        return item

    @catch_get_repo_info_error
    def get_repo_info(self):
        url = 'https://api.github.com/repos/{owner}/{repo}'.format(
            owner=self.owner, repo=self.repo)
        r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
        result = r.json()
        return DataGenerator.generate_repo_head_data(result, self.owner)

    @catch_get_max_pr_num_error
    def get_max_pr_num(self, page=0):
        result = []
        while page == 0 or result != []:
            url = 'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&page={page}'.format(
                owner=self.owner, repo=self.repo, page=page)
            r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
            result = r.json()
            page += 1
            if 'message' in result:
                return result
            for item in result:
                if item['merged_at'] is not None:
                    return item['number']
        return result

    @catch_get_popular_repo_per_page_error
    def get_popular_repo_per_page(self, language, page, per_page):
        url = 'https://api.github.com/search/repositories?q=language:{language}&sort=stars&page={page}' \
              '&per_page={per_page}'.format(language=language, page=page, per_page=per_page)
        r = requests.get(url, headers=self.configDealer.get_headers()[0], proxies=self.proxies)
        result = r.json()
        return result

    def get_judgement(self, word):
        url = ConfigDealer.get_client_website()
        data = {'word': word}
        r = requests.post(url, json=json.dumps(data))
        result = r.json()
        return result
