# 发布素材

标题（主用，≤40 字内平台直贴）：
Claude Code 沙箱怎么隔离？并发冲突怎么处理？五层源码拆给你看

## 备选标题（按平台微调）

- B 站：读 Anthropic Claude Code 源码：沙箱、文件锁、任务 Claim、Bridge 一次讲清
- 抖音 / 竖屏：搭 Agent 平台必看：沙箱不是摆设，并发靠内核原子语义
- 小红书：10 分钟搞懂 Claude Code 五层安全：从黑名单到 Bridge 生命周期

简介：

你们公司是不是也在搭自己的 Agent 系统？执行代码怎么防乱删乱改？多实例抢同一份状态怎么不炸？锁文件残留卡死怎么办？

这期直接顺着源码讲 Claude Code 的安全与并发：Python REPL 黑名单与 gyoshu_bridge、不靠 flock 的 O_CREAT|O_EXCL 文件锁、Session 锁防 PID 复用、任务 Claim 三阶段、Bridge 四层校验和信号逐级退出。看完能对照设计自己的存储与调度层。

话题：
#ClaudeCode #Anthropic #AIAgent #沙箱 #并发控制 #源码解读 #Agent平台 #文件锁 #软件架构 #编程

## 置顶评论（可选粘贴）

五层速记：① REPL 黑名单 + 诚实写边界 ② 存在性文件锁 + 自愈 ③ Session 锁 + O_NOFOLLOW ④ 预检→原子锁→锁内重读 ⑤ Bridge 校验 + SIGINT→SIGTERM→SIGKILL。时间轴见简介上方章节。

## 章节轴（B 站 / 视频章节）

0:00 引入：自建 Agent 系统的典型痛点
1:23 第一层：Python REPL 沙箱与黑名单
2:40 第二层：O_CREAT|O_EXCL 文件锁，为何不 flock
4:13 第三层：Session 锁、PID+startTime、符号链接防御
6:14 第四层：任务级 Claim，乐观预检与竞态窗口
7:57 第五层：Bridge 四层验证与进程退出策略
9:28 总结：四条可落地的设计原则
10:26 收尾

## 发布检查清单

- [ ] 成片 `production/final.mp4` 已最终校对字幕与翻页
- [ ] 竖版封面 `production/videos/cover.png` 已替换各平台上一条
- [ ] 简介纯文本粘贴（无 Markdown 符号）
- [ ] 话题行单独一行，# 开头、空格分隔
- [ ] 口播中出现的专名（Claude Code、Anthropic、gyoshu_bridge 等）与简介一致
