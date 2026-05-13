# 话题大纲

<!-- 视频的话题拆分、每段核心要点、预计时长 -->

## 视频信息

- **时长**: 10-12 分钟
- **类型**: mid-video 中视频深度解析
- **受众**: 有技术基础的开发者/架构师
- **核心目标**: 看完能借鉴原理设计自己的 agent 平台沙箱和存储系统

## 章节结构

| 章节 | 时长 | 核心内容 | 源码素材 |
|------|------|---------|---------|
| **引入** | 1min | 以 "你们公司现在是不是也在搭自己的 agent 系统？" 直接切入痛点 | 无 |
| **第一层：Python REPL 沙箱** | 2min | 默认信任 vs 主动收紧，黑名单诚实声明能力边界 | `gyoshu_bridge.py:307-369` |
| **第二层：文件锁** | 2.5min | 不靠 flock、靠 `O_CREAT\|O_EXCL` 内核原子性的文件存在性锁，带死锁自愈 | `file-lock.ts:109-156` |
| **第三层：Session 锁** | 2.5min | PID+启动时间双重验证防 PID 复用，`O_NOFOLLOW` 防符号链接攻击 | `session-lock.ts:107-165` |
| **第四层：任务级并发 Claim** | 2.5min | 乐观预检 → 原子加锁 → 锁内重读验证 | `task-file-ops.ts:285-340` |
| **第五层：Bridge 生命周期** | 1.5min | 四层验证 + 信号逐级升级终止 + 父进程监控自杀 | `bridge-manager.ts:520-560` |
| **总结** | 1min | 4 个可落地的设计原则 | 无 |

## 关键源码文件索引

1. `oh-my-claudecode/src/lib/security-config.ts` — 安全配置模型（默认宽松/严格模式切换）
2. `oh-my-claudecode/bridge/gyoshu_bridge.py` — Python REPL 沙箱黑名单实现
3. `oh-my-claudecode/src/lib/file-lock.ts` — `O_CREAT\|O_EXCL` 原子文件锁
4. `oh-my-claudecode/src/tools/python-repl/session-lock.ts` — Session 锁 + PID reuse 检测
5. `oh-my-claudecode/src/team/task-file-ops.ts` — 任务级原子 claim 与并发控制
6. `oh-my-claudecode/src/tools/python-repl/bridge-manager.ts` — Bridge 生命周期四层验证
