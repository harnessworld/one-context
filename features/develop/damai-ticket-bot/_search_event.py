# -*- coding: utf-8 -*-
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Referer': 'https://www.damai.cn/',
}

# 试大麦移动API
keyword = '京剧'
r = requests.get('https://mapi.damai.cn/project/list', params={'keyword': keyword, 'page': 1, 'size': 20, 'type': 1}, headers=headers, timeout=10)
print('mapi status:', r.status_code)
print('url:', r.url)
print('content[:500]:', r.text[:500])
print()

# 尝试官方搜索接口
r2 = requests.get('https://search.damai.cn/api/sys/search', params={'keyword': '京剧', 'pageIndex': 1, 'pageSize': 10}, headers=headers, timeout=10)
print('search api status:', r2.status_code)
print('search url:', r2.url)
print('search content[:500]:', r2.text[:500])
