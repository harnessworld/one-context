# -*- coding: utf-8 -*-
"""
测试：直接用 requests 访问大麦 API，检查 cookie 是否有效
"""
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.7727.55 Safari/537.36',
    'Referer': 'https://www.damai.cn/',
    'Accept': 'application/json, text/plain, */*',
}

# 读取 cookies 文件（如果有）
cookie_file = 'cookies_damai.json'
try:
    with open(cookie_file, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    print(f'已加载 {len(cookies)} 个 cookie')
    
    # 用 cookie 请求大麦接口
    session = requests.Session()
    session.headers.update(headers)
    for name, value in cookies.items():
        session.cookies.set(name, value)
    
    # 测试：获取用户信息
    r = session.get('https://www.damai.cn/', timeout=10)
    print('大麦首页:', r.status_code, len(r.text), '字节')
    
    # 测试：访问项目详情
    test_item_id = '610820299671'
    r2 = session.get(f'https://detail.damai.cn/item.htm?id={test_item_id}', timeout=10)
    print(f'项目 {test_item_id}:', r2.status_code)
    
except FileNotFoundError:
    print(f'没有找到 {cookie_file}，请先扫码登录')
    print('要生成这个文件，请在浏览器登录大麦后，把 cookies 导出为 JSON 格式')
    print('格式: { "cookie_name": "cookie_value", ... }')
