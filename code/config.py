"""mongodb的信息"""
MONGO_SERVER = "127.0.0.1"
MONGO_PORT = 27017
MONGO_USERNAME = None
MONGO_PASSWD = None
TABLE = "abc"

""" 代理路径，推荐使用代理。系统已增加断连重试机制（5次），但非代理下仍会有极大概率失败
    免费github代理：dev_sidecar 
"""
USE_PROXY = True
HTTP_PROXY = '127.0.0.1:7890'
HTTPS_PROXY = '127.0.0.1:7890'

""" diff文件存放路径，具体为“DIFF_PATH/owner/repo/x.diff”

    DIFF_PATH_DEFAULT为True代表diff_path顶层目录和code文件夹同级
    程序会自动寻找上一级文件夹并拼接相对路径
    选择False,则DIFF_PATH为绝对路径
"""
DIFF_PATH = "multi_pr_diff\\"
DIFF_PATH_DEFAULT = True

"""存放仓库的位置,每一行为owner repo, 中间用/t分隔 """
STORE_PATH = "code\store.tsv"
STORE_PATH_DEFAULT = True

LOG_PATH = "logs\\"
LOG_PATH_DEFAULT = True

"""github token可以使同token访问次数从每小时60提升至5000"""
token = ['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',
         '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',
         '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',
         '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']

"""github访问请求头"""
pr_header = {'User-Agent': 'Mozilla/5.0',
             'Authorization': '',
             'Content-Type': 'application/json',
             'Accept': 'application/vnd.github.v3+json',
             }
diff_header = {'User-Agent': 'Mozilla/5.0',
               'Authorization': '',
               'Content-Type': 'application/json',
               'Accept': 'application/vnd.github.VERSION.diff'
               }

"""需要爬取的信息列表"""
DIFF_LABELS = ["number", "url", "diff_url", "issue_url", "state", "title", "body", "created_at",
               "merged_at", "base"]
REPO_LABELS = ["id", "name", "language", "created_at"]

INVALID_WORD = ['面试', 'Leetcode', 'leetcode', '指南', '知识', '题目', 'Interview',
                '扫盲', 'interview', '排行榜', '教程', '学习', '成神']

HOT_REPO_PER_PAGE = 60
