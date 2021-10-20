from urllib.request import urlopen
from urllib.request import Request
import json

from util.DataGenerator import DataGenerator

pr_header = {'User-Agent': 'Mozilla/5.0',
             'Authorization': 'token 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',
             'Content-Type': 'application/json',
             'Accept': 'application/vnd.github.v3+json'
             }
diff_header = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token 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',
               'Content-Type': 'application/json',
               'Accept': 'application/vnd.github.VERSION.diff'
               }


class Crawler(object):
    def __init__(self, owner, repo, diff_path=None, *token):
        self.owner = owner
        self.repo = repo
        self.pr_header = pr_header
        self.diff_header = diff_header
        if token is not None:
            self.token = token
        if diff_path is not None:
            self.diff_path = diff_path

    def validate_repo(self):
        url = 'https://api.github.com/repos/{owner}/{repo}'.format(
            owner=self.owner, repo=self.repo)
        req = Request(url, headers=self.pr_header)
        response = urlopen(req).read()
        result = json.loads(response.decode())
        if 'message' in result:
            print(result['message'])
            return False
        return True

    def get_pr_page_results_not_deal(self):
        result = []
        page = 1
        while page == 1 or result != []:
            url = 'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&page={page}&sort=updated'.format(
                owner=self.owner, repo=self.repo, page=page)
            req = Request(url, headers=self.pr_header)
            response = urlopen(req).read()
            result = json.loads(response.decode())
            yield result
            page = page + 1

    def deal_diff(self, item):
        path = self.diff_path + '/' + self.owner + '/' + self.repo + '/' + item["number"] + ".diff"
        url = 'https://github.com/{owner}/{repo}/pull/{number}.diff'.format(
            owner=self.owner, repo=self.repo, number=item["number"])
        req = Request(url, headers=diff_header)
        response = urlopen(req).read()
        with open(path, 'w') as f:
            print(response.decode(), file=f)
        item["diff_local_path"] = path
        return item

    def get_repo_info(self):
        url = 'https://api.github.com/repos/{owner}/{repo}'.format(
            owner=self.owner, repo=self.repo)
        req = Request(url, headers=self.pr_header)
        response = urlopen(req).read()
        result = json.loads(response.decode())
        return DataGenerator.generate_repo_head_data(result)