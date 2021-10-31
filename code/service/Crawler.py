import http
from urllib.request import urlopen
from urllib.request import Request
import json
from util.ConfigDealer import ConfigDealer
import os

import requests
from util.DataGenerator import DataGenerator
import ssl

# https://github.com容易访问超时，需要爬取可用ip，但会引发证书失效问题，需要手动关闭证书验证
context = ssl._create_unverified_context()


class Crawler(object):
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.configDealer=ConfigDealer.get_instance()
        self.pr_header, self.diff_header = self.configDealer.get_headers()
        self.diff_path = self.configDealer.get_diff_path()
        self.proxies = self.configDealer.get_proxy()

        self.check_and_make_dirs_exist()

    def check_and_make_dirs_exist(self):
        path = self.diff_path + '/' + self.owner + '/' + self.repo
        if not os.path.exists(path):
            os.makedirs(path)

    def validate_repo(self, times=0):
        try:
            url = 'https://api.github.com/repos/{owner}/{repo}'.format(
                owner=self.owner, repo=self.repo)
            r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
            result = r.json()
            if 'message' in result:
                print(result['message'])
                return False
            return True
        except Exception as e:
            if times < 5:
                print('error validation')
                times += 1
                self.validate_repo(times)
            else:
                print(
                    "[ERROR] time out at validate repo with " + self.owner + " " + self.repo)
            raise Exception

    def get_pr_page_results_not_deal(self, times=0):
        try:
            result = []
            page = 1
            while page == 1 or result != []:
                url = 'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&page={page}&direction=asc'.format(
                    owner=self.owner, repo=self.repo, page=page)
                r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
                result = r.json()
                yield result
                page = page + 1
        except Exception as e:
            if times < 5:
                print('error get per page')
                times += 1
                self.get_pr_page_results_not_deal(times)
            else:
                print(
                    "[ERROR] time out at getting repo page result with " + self.owner + " " + self.repo)
            raise Exception

    def deal_diff(self, item, times=0):
        try:
            path = self.diff_path + '/' + self.owner + '/' + self.repo + '/' + str(item["number"]) + ".diff"
            url = 'https://github.com/{owner}/{repo}/pull/{number}.diff' \
                .format(owner=self.owner, repo=self.repo, number=item["number"])
            print(item["number"])
            # req = Request(url, headers=diff_header)
            # # req.set_proxy('127.0.0.1:7890', 'https')  # todo 抽离代理输入位置
            # response = urlopen(req, timeout=30).read()
            r = requests.get(url, headers=self.diff_header, proxies=self.proxies)
            response = r.text
            with open(path, 'w', encoding='utf-8') as f:
                print(response, file=f)
            item["diff_local_path"] = path
            return item
        except Exception as e:
            if times < 5:
                print('error getting diff')
                times += 1
                self.deal_diff(item, times)
            else:
                print(
                    "[ERROR] time out at getting diff files with " + self.owner + " " + self.repo + " diff number:" + str(
                        item["number"]))
            raise Exception

    def get_repo_info(self, times=0):
        try:
            url = 'https://api.github.com/repos/{owner}/{repo}'.format(
                owner=self.owner, repo=self.repo)
            r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
            result = r.json()
            return DataGenerator.generate_repo_head_data(result, self.owner)
        except Exception as e:
            if times < 5:
                print('error get repo info')
                times += 1
                self.get_repo_info(times)
            else:
                print(
                    "[ERROR] time out at getting repo info with " + self.owner + " " + self.repo)
            raise Exception

    def get_max_pr_num(self, times=0):
        try:
            url = 'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed'.format(
                owner=self.owner, repo=self.repo)
            r = requests.get(url, headers=self.pr_header, proxies=self.proxies)
            result = r.json()
            return result[0]["number"]
        except Exception as e:
            if times < 5:
                print('error get per page')
                times += 1
                self.get_pr_page_results_not_deal(times)
            else:
                print(
                    "[ERROR] time out at getting max pr num with " + self.owner + " " + self.repo)
            raise Exception
