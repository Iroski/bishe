import requests
from bs4 import BeautifulSoup
import os
import subprocess


class gitip:
    def __init__(self, ip_list):
        super().__init__()
        self.ip_list = ip_list
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        self.ip_1 = 'https://github.com.ipaddress.com/'  # github.com

    def get_1(self):  # github.com
        response = requests.get(self.ip_1, headers=self.header)
        soup = BeautifulSoup(response.text, features='lxml')
        # print(soup.find_all('ul', {'class': 'comma-separated'})[0].text + '    github.com')
        return soup.find_all('ul', {'class': 'comma-separated'})[0].text

def get_github_ip():
    ip_list = []
    error = 0
    github = gitip(ip_list)
    try:
        ip=github.get_1()
        return ip
    except:
        print('github.com 申请出错')
        return '140.82.114.4'

