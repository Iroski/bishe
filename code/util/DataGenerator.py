class DataGenerator:
    diff_labels = ["number", "url", "diff_url", "issue_url", "state", "title", "body", "created_at",
                   "merged_at", "base"]
    repo_lavels = ["id", "name", "language", "created_at"]

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
    def generate_repo_head_data(cls, data):
        result = {}
        for label in DataGenerator.repo_lavels:
            result[label] = data[label]
        return result
