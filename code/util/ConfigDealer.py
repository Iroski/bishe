import config
from threading import RLock
import pandas as pd
import os


class ConfigDealer(object):
    def __init__(self):
        self.token_pointer = 0
        self.token_size = len(config.token)
        self.repo_pointer = 0
        self.rlock = RLock()
        self.path = os.path.abspath("..") + '\\'

    @classmethod
    def init(cls):
        ConfigDealer._instance = ConfigDealer()

    @classmethod
    def get_instance(cls):
        if not hasattr(ConfigDealer, '_instance'):
            ConfigDealer._instance = ConfigDealer()
        return ConfigDealer._instance

    def get_diff_path(self):
        path=self.path + config.DIFF_PATH if config.DIFF_PATH_DEFAULT else config.DIFF_PATH
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_token(self,id):
        return config.token[id]

    def get_token_ptr(self):
        self.token_pointer = (self.token_pointer + 1) % self.token_size
        return self.token_pointer

    def get_headers(self,token_ptr):
        self.rlock.acquire()
        try:
            token = self.get_token(token_ptr)
            pr_header = config.pr_header
            diff_header = config.diff_header
            pr_header['Authorization'] = 'token ' + str(token)
            diff_header['Authorization'] = 'token ' + str(token)
        finally:
            self.rlock.release()
        return pr_header, diff_header

    def get_proxy(self):
        if not config.USE_PROXY:
            return None
        proxies = {'http': config.HTTP_PROXY, 'https': config.HTTPS_PROXY}
        return proxies

    @classmethod
    def load_local_repos(cls) -> pd.DataFrame:
        path = cls.get_instance().path + config.STORE_PATH if config.STORE_PATH_DEFAULT else config.STORE_PATH
        return pd.read_csv(path, sep='\t')

    @classmethod
    def store_local_repos(cls, data: pd.DataFrame):
        path = cls.get_instance().path + config.STORE_PATH if config.STORE_PATH_DEFAULT else config.STORE_PATH
        data.to_csv(path, index=False, sep='\t')

    @classmethod
    def get_log_path(cls):
        path=cls.get_instance().path + config.LOG_PATH if config.LOG_PATH_DEFAULT else config.LOG_PATH
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @classmethod
    def get_invalid_word(cls):
        return config.INVALID_WORD

    @classmethod
    def get_per_page_for_hot_repo(cls):
        return config.HOT_REPO_PER_PAGE
