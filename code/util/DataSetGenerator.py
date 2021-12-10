import re

from service.Crawler import Crawler
from config import DIFF_LABELS, REPO_LABELS


class DataSetGenerator:
    diff_labels = DIFF_LABELS
    repo_labels = REPO_LABELS

    @classmethod
    def generate_set_info(cls, data, crawler):
        pr_text = data['title'] + ' '
        if data['body'] is not None:
            pr_text = pr_text + data['body'] + ' '
        pr_labels = data['labels']
        pr_label = ''
        for i in pr_labels:
            pr_label = pr_label + i['name'] + ' '
        related_issue = re.findall("#\d+", pr_text)
        issue_text, issue_labels = cls.get_issues_info(related_issue, crawler)
        result_str = pr_text + issue_text + pr_label + issue_labels
        result_str = str(result_str).replace("\n", " ")
        return result_str

    @classmethod
    def get_issues_info(cls, related_issue, crawler):
        issue_text = ''
        issue_label = ''
        for i in range(len(related_issue)):
            related_issue[i] = related_issue[i][1:]
            result = crawler.get_issue(related_issue[i])
            issue_text = issue_text + result['title'] + ' '
            if result['body'] is not None:
                issue_text = issue_text + result['body'] + ' '
            for i in result['labels']:
                issue_label = issue_label + i['name'] + ' '
        return issue_text, issue_label
