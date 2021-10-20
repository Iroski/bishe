import json
from urllib.request import urlopen
from urllib.request import Request
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token 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',
               'Content-Type': 'application/json',
               'Accept': 'application/vnd.github.VERSION.diff'
               }
url = 'https://api.github.com/repos/{owner}/{repo}'.format(
        owner='Iroski', repo='SE-group-90')
req = Request(url, headers=headers)
response = urlopen(req).read()
result = json.loads(response.decode())
pprint(result)
