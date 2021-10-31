import json
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import ProxyHandler, build_opener
from pprint import pprint
import socket
import socks
import ssl
import requests

# # socks.set_default_proxy(socks.SOCKS5,"localhost",10808)
# # socket.socket=socks.socksocket
context = ssl._create_unverified_context()
diff_header = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token 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',
               'Content-Type': 'application/json',
               'Accept': 'application/vnd.github.VERSION.diff'
               }

# url = 'https://github.com/{owner}/{repo}/pull/{number}.diff'. \
#     format(ip='140.82.114.3', owner='Iroski',
#            repo='SE-group-90', number='139')
proxies = {'http': '127.0.0.1:1181', 'https': '127.0.0.1:1181'}
# r = requests.get(url, headers=diff_header, proxies=proxies)
# print(r.text)
# req = Request(url, headers=diff_header)
# response = urlopen(req, timeout=30).read()
# print(response.decode())


pr_header = {'User-Agent': 'Mozilla/5.0',
             'Authorization': 'token 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',
             'Content-Type': 'application/json',
             'Accept': 'application/vnd.github.v3+json'
             }
url = 'https://api.github.com/repos/{owner}/{repo}'.format(
            owner="Iroski", repo="SE-Group-90")
r=requests.get(url,headers=pr_header,proxies=proxies)

# req = Request(url, headers=pr_header)
# req.set_proxy('127.0.0.1:7890', 'http')
# req.set_proxy('127.0.0.1:7890', 'https')
# response = urlopen(req).read()
# result = json.loads(response.decode())
# print(result)
