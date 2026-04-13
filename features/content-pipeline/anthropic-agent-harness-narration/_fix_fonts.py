with open(r'D:\harnessworld\one-context\features\develop\anthropic-agent-harness-narration\_gen_anthro_ppt.py','r',encoding='utf-8') as f:
    c = f.read()
c = c.replace("'Roboto Mono', monospace", "'Consolas', 'Courier New', monospace")
c = c.replace("'Roboto Mono'", "'Consolas', 'Courier New', monospace")
with open(r'D:\harnessworld\one-context\features\develop\anthropic-agent-harness-narration\_gen_anthro_ppt.py','w',encoding='utf-8') as f:
    f.write(c)
print('Done')
