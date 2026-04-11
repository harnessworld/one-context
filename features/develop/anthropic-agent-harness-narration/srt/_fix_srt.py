# -*- coding: utf-8 -*-
import os, glob, shutil

# 找到 Downloads 里的 SRT
downloads = os.path.join(os.environ['USERPROFILE'], 'Downloads')
srt_files = glob.glob(os.path.join(downloads, 'Anthropic+*.srt'))
if not srt_files:
    print('No SRT found in Downloads')
    exit(1)

src_path = srt_files[0]
print('Source:', src_path)

src = open(src_path, 'r', encoding='utf-8').read()

replacements = [
    # 核心关键词纠正
    ('Agent是宠物还是生口?', 'Agent是宠物还是牲口？'),
    ('变成了可以随时替换的生口', '变成了可以随时替换的牲口'),
    ('宠物到胜口', '宠物到牲口'),
    ('宠物到生口', '宠物到牲口'),
    # 绘画 → 会话
    ('绘画状态', '会话状态'),
    ('绘画层', '会话层'),
    ('绘画', '会话'),
    # 沙箱统一
    ('杀箱', '沙箱'),
    # Asian → Agent
    ('在Asian的', '在Agent的'),
    # 成语
    ('千一发而动全身', '牵一发而动全身'),
    # 其他明显误识别
    ('出创公司', '初创公司'),
    ('评证', '凭证'),
    ('平谈化', '平台化'),
    ('管理门卡', '管理门槛'),
    ('就是Agent', '就是Agent'),
]

for old, new in replacements:
    if old in src:
        src = src.replace(old, new)
        print(f'  Fixed: {old!r} → {new!r}')

# 输出到项目目录
out_dir = r'D:\harnessworld\one-context\features\develop\anthropic-agent-harness-narration\srt'
os.makedirs(out_dir, exist_ok=True)
dst_path = os.path.join(out_dir, 'anthro_harness_v1.srt')
with open(dst_path, 'w', encoding='utf-8-sig') as f:
    f.write(src)

print(f'Written: {dst_path}')
print(f'Total chars: {len(src)}')
