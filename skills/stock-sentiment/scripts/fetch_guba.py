#!/usr/bin/env python3
"""东方财富股吧评论抓取器 v2 - 抓取帖子标题"""
import json, re, sys, urllib.request
from datetime import datetime

BASE_URL = 'https://guba.eastmoney.com/list'

def clean_text(html):
    text = re.sub(r'<[^>]+>', ' ', html)
    return re.sub(r'\s+', ' ', text).strip()

def guba_code(stock_code):
    """将 9988.HK -> hk9988, 600536 -> 600536"""
    if stock_code.endswith('.HK') or stock_code.endswith('.hk'):
        num = stock_code.split('.')[0].lstrip('0') or '0'
        return 'hk' + num
    return stock_code

def fetch_guba_posts(stock_code, pages=3):
    results = []
    guba_code_str = guba_code(stock_code)
    for page in range(1, pages+1):
        url = f'{BASE_URL},{guba_code_str}.html' if page == 1 else f'{BASE_URL},{guba_code_str},f_{page}.html'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read()
                ct = resp.headers.get('Content-Type', '')
                encoding = 'gbk' if 'gbk' in ct or 'gb2312' in ct else 'utf-8'
                html = raw.decode(encoding, errors='ignore')
            # 通用正则：兼容 /news,600536,123.html 和 /news,hk9988,1695034698.html
            pid_map = {}
            for m in re.finditer(r'/news,([^,]+),(\d+)\.html', html):
                key = m.group(1)
                pid = m.group(2)
                if key != guba_code_str:
                    continue
                if pid in pid_map:
                    continue
                start = max(0, m.start()-500)
                ctx = html[start:m.end()+200]
                tm = re.search(r'>([一-龥\u4e00-\u9fff]{4,100})<', ctx)
                if tm:
                    t = clean_text(tm.group(1))
                    if len(t) > 3:
                        pid_map[pid] = t
            seen = set()
            for pid in sorted(pid_map.keys(), reverse=True):
                if pid in seen:
                    continue
                seen.add(pid)
                results.append({'post_id': pid, 'title': pid_map[pid],
                                'url': f'https://guba.eastmoney.com/news,{guba_code_str},{pid}.html'})
            print(f'  Page {page}: {len(results)} titles', file=sys.stderr)
        except Exception as e:
            print(f'  Page {page} error: {e}', file=sys.stderr)
    return results[:50]

titles_only = '--titles' in sys.argv
output_file = None
cleaned_args = []
for a in sys.argv[1:]:
    if a == '--titles' or a == '-t':
        titles_only = True
    elif a.startswith('--output='):
        output_file = a.split('=', 1)[1]
    else:
        cleaned_args.append(a)

if len(cleaned_args) < 1:
    print('Usage: fetch_guba.py <stock_code> [pages] [--titles] [--output=file.json]')
    sys.exit(1)

stock_code = cleaned_args[0]
pages = int(cleaned_args[1]) if len(cleaned_args) > 1 else 3
posts = fetch_guba_posts(stock_code, pages)

if titles_only:
    for p in posts:
        print(p['title'])
else:
    result = json.dumps({'stock_code': stock_code, 'total': len(posts),
                         'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                         'posts': posts}, ensure_ascii=False, indent=2)
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f'Saved {len(posts)} posts to {output_file}')
    else:
        print(result)
