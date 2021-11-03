import pandas as pd
from util.ConfigDealer import ConfigDealer


class RepoGenerator(object):

    @classmethod
    def generate_repo_header(cls, result):
        items = result['items']
        df = pd.DataFrame(columns=['owner', 'repo'])
        for item in items:
            if cls.check_repo_valid(item['full_name'], item['description']):
                continue
            url = item['url']
            labels = url.split('/')
            line = {'owner': labels[-2], 'repo': labels[-1]}
            df = df.append(line, ignore_index=True)
        return df

    @classmethod
    def check_repo_valid(cls, name, description):
        invalid_word = ConfigDealer.get_invalid_word()
        for word in invalid_word:
            if word in name or word in description:
                return True
        return False
