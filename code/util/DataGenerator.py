from config import DIFF_LABELS,REPO_LABELS
class DataGenerator:
    diff_labels = DIFF_LABELS
    repo_labels = REPO_LABELS

    def __init__(self, *dlabels):
        if dlabels is not None:
            DataGenerator.diff_labels = dlabels

    # 生成一条diff文件信息
    @classmethod
    def generate_diff_data(cls, data):
        result = {}
        for label in DataGenerator.diff_labels:
            if label != "base":
                result[label] = data[label]
            else:
                result["base"] = data[label]["ref"]
        return result

    @classmethod
    def generate_repo_head_data(cls, data, owner):
        result = {}
        for label in DataGenerator.repo_labels:
            result[label] = data[label]
        result["owner"] = owner
        result["latest_pr_num"] = 0
        return result
