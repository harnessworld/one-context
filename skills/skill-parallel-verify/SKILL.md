---
name: skill-parallel-verify
type: quality-assurance
description: 并行验证测试 Skill。用于 Skill 交付前的自动化一致性验证——3 个独立测试专家在干净上下文中执行被测 Skill，测试主管判定输出是否语义等价，不一致时自动驱动修复循环。与 skill-creator（开发阶段迭代+人工评审）互补，本 Skill 侧重交付前的自动化质量关卡。触发关键词：验证skill一致性、并行测试skill、skill交付验证。
triggers:
  - 验证skill
  - 测试skill
  - skill一致性
  - 并行验证
  - parallel verify
  - skill交付验证
author: 水猿
version: 1.1.0
tags:
  - skill
  - testing
  - quality
openclaw:
  requires:
    bins: []
  install: []
---

# Skill Parallel Verify

通过多角色并行测试机制，验证 Skill 的产出质量和一致性。核心思路：让 3 个独立的测试专家分别在干净上下文中执行同一个 Skill，然后由测试主管判定结果是否语义等价且符合验收标准。不一致时自动驱动修复循环。

---

## 触发条件

当用户提到以下场景时使用：
- "验证一下这个 skill" / "测试一下 skill 质量"
- "做一下 skill 的一致性测试"
- "并行验证 skill"
- "我想确保这个 skill 每次运行结果都差不多"
- 用户提供 test-case 文件要求测试

---

## 使用方法

1. 准备 test-case YAML 文件（格式见下方）
2. 调用：告诉 Claude "用 skill-parallel-verify 验证 `path/to/test-case.yaml`"
3. 等待验证完成，查看最终报告

---

## Test Case 文件格式

详细格式参考 `references/test-case-format.md`，模板见 `assets/test-case-template.yaml`。

简要格式：

```yaml
skill_path: "skills/xxx/skill-name/SKILL.md"  # 被测 Skill 路径（必填）
test_name: "测试名称"                                    # 测试名称（必填）
acceptance_criteria: "验收标准描述"                       # 验收标准（可选）

test_cases:
  - id: tc-1
    prompt: "用户输入的提示词"
    description: "测试目的描述"  # 可选
```

---

## 执行流程

### Step 1: 解析与校验

**操作**：读取并校验 test-case YAML 文件
- 验证 skill_path 指向的 SKILL.md 存在
- 验证 test_cases 非空
- 验证必填字段完整

**门控条件**：校验通过，否则报错退出

### Step 2: 备份原始 Skill

**操作**：将被测 Skill 文件备份到同目录的 `backups/` 下
- 备份路径：`{skill所在目录}/backups/SKILL.md.bak`
- 只备份一次，已有备份则跳过
- 备份位置仅存放原始版本
- 每轮修复前，将当前 SKILL.md 复制到 `.skill-parallel-verify/round-{N}/SKILL.md.snapshot` 作为工作快照

**门控条件**：备份完成

### Step 3: 创建工作目录（或断点恢复）

**操作**：检查是否已有 `.skill-parallel-verify/verification.json`（工作目录位于**项目根目录**下，已在 `.gitignore` 中排除）

**如果是新启动**：
- 创建项目根目录下的 `.skill-parallel-verify/` 目录和 `verification.json` 状态文件
- 初始化 verification.json（含 test_case_content 快照）

> ⚠️ 工作目录说明：`.skill-parallel-verify/` 是运行时产物目录，位于项目根目录，已在 `.gitignore` 中排除，不会被提交到 Git。

**如果是断点恢复**（verification.json 存在且 status = "running"）：
- 读取 verification.json，根据 last_checkpoint 判断断点位置
- 从断点继续：跳过已完成的测试专家，继续未完成的部分
- 向用户确认："检测到未完成的验证任务（{test_name}，第{N}轮），是否从断点恢复？"

### Step 4: 启动测试专家（伪并行）

**操作**：顺序启动 3 个 skill-tester subagent，每个在独立的干净上下文中：
1. 读取被测 SKILL.md 的完整内容
2. 按照用户提供的 prompt 执行被测 Skill
3. 如实记录完整输出

每个测试专家的 prompt 模板：

```
你是 skill 测试专家 {N}，你的任务是在干净的环境中独立测试一个 Skill。

## 被测 Skill
请先读取被测 Skill 文件：{skill_path}

## 测试提示词
{prompt}

## 验收标准
{acceptance_criteria}

## 你的任务
1. 读取被测 Skill 的完整内容
2. 严格按照 Skill 的指令执行用户的测试提示词
3. 记录你的完整输出结果

## 重要约束
- 你必须在独立上下文中执行，不要假设任何外部信息
- 严格按照 Skill 的流程执行，不要自行添加或跳过步骤
- 如实记录输出，不要根据"预期结果"调整你的输出
- 输出你的完整执行结果
```

将每个测试专家的输出保存到 `.skill-parallel-verify/round-{N}/tester-{i}/output.md`

### Step 5: 测试主管判定

**操作**：使用 subagent 执行测试主管判定，评估 3 个测试专家的输出是否语义等价

测试主管判定 prompt 模板：

```
你是测试主管，负责判定 3 个测试专家的输出是否语义等价。

## 被测 Skill 路径
{skill_path}

## 验收标准
{acceptance_criteria}

## 3 个测试专家的输出
{tester_results}

## 判定规则（4 维度结构化判定）

按以下 4 个维度逐一判定，每个维度给出 pass/fail：

1. **功能完整性**：是否所有输出都完成了需求的核心功能？有任何输出缺少核心功能则 fail
2. **输出类型一致**：输出的类型/格式是否相同（如都是 PPT、都是 markdown）？类型不同则 fail
3. **关键属性匹配**：输出的关键属性是否一致（如风格、主题、约束条件）？关键属性不匹配则 fail
4. **质量水平相当**：输出的质量水平是否在同一层级（如详细程度、专业度）？差异显著则 fail

判定逻辑：
- **verdict = "pass" 的充要条件**：semantic_equivalent = true 且 matches_acceptance = true（即四个维度全部 pass 且所有输出均符合验收标准）
- 前三个维度（功能完整性、输出类型、关键属性）任一 fail → semantic_equivalent = false → verdict = "fail"
- 前三个维度都 pass，但质量水平差异显著 → semantic_equivalent = false（标记为"轻微不一致"）→ verdict = "fail"
- 四个维度全部 pass 但不符合验收标准 → matches_acceptance = false → verdict = "fail"

判定示例：
- 需求"商务风格PPT"：3 个都是商务风格 + 都有3页以上 → pass
- 需求"商务风格PPT"：2 个商务风格 + 1 个科技风格 → fail（关键属性不匹配）
- 需求"生成 API 文档"：3 个都生成了 API 文档，但 1 个缺少错误码 → fail（功能完整性缺失）

## 验收标准检查
每个输出是否都满足验收标准（独立于语义等价判定）

## 输出格式（必须严格遵守）
```json
{
  "semantic_equivalent": true/false,
  "matches_acceptance": true/false,
  "equivalence_dimensions": {
    "functional_completeness": "pass/fail",
    "output_type_consistency": "pass/fail",
    "key_attribute_matching": "pass/fail",
    "quality_level": "pass/fail"
  },
  "inconsistencies": "如果不一致，描述具体的差异",
  "verdict": "pass/fail",
  "failed_testers": ["tester-3"],
  "failure_details": "每个失败测试专家的具体问题"
}
```
```

**门控条件**：
- verdict = "pass" → 跳到 Step 7（生成通过报告）
- verdict = "fail" → 继续 Step 6

### Step 6: Skill 专家修复

**操作**：启动 skill-expert subagent，分析不一致原因并修复被测 Skill

Skill 专家修复 prompt 模板：

```
你是 Skill 专家，负责修复被测 Skill 存在的问题。

## 被测 Skill 文件
{skill_path}
（请先 Read 该文件了解当前内容）

## 测试主管的判定
- 语义等价: {semantic_equivalent}
- 符合验收标准: {matches_acceptance}
- 不一致详情: {inconsistencies}
- 失败的测试专家: {failed_testers}
- 失败详情: {failure_details}

## 失败测试专家的输出
{failed_tester_outputs}

## 成功测试专家的输出（作为参照）
{succeeded_tester_outputs}

## 你的任务
1. 分析失败的测试专家与成功的测试专家的差异
2. 定位 Skill 中导致不一致的根因
3. 修改 Skill 文件，使所有测试专家都能产生一致且符合验收标准的输出
4. 修改应最小化，只修改导致问题的部分

## 重要约束
- 原始 Skill 备份已保存在 backups/ 目录，你可以放心修改
- 修改范围应最小化，不要大范围重写
- 请直接修改 Skill 文件并说明修改了什么
```

修复完成后，更新 verification.json，回到 **Step 4** 重新测试。

**轮次上限**：最多 10 轮，超过后跳到 Step 7 生成失败报告。

### Step 7: 生成 HTML 报告

**操作**：生成一份自包含的 HTML 报告文件，用户可在浏览器中打开，3 个测试专家的输出直接内联渲染在页面中，HTML 用 iframe 预览，文本用代码块展示，可选 2 面板对比视图，差异一目了然。

**报告保存路径**：`.skill-parallel-verify/report.html`

**设计原则**：
- **对比优先**：3 个测试专家输出直接内联渲染在页面中，支持双面板对比，差异高亮
- **一眼判定**：暗色主题 + 渐变 + 动画，核心状态无需阅读文字即可感知
- **零依赖**：所有 CSS/JS 内联，单文件可直接在浏览器打开
- **完整展示**：测试专家输出不截断，方便人工逐条确认

**HTML 报告模板**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Skill 并行验证测试报告 - {test_name}</title>
<style>
/* ===== 设计令牌 ===== */
:root {
  --bg-primary: #0f172a; --bg-secondary: #1e293b; --bg-card: #1e293b;
  --bg-card-hover: #334155; --bg-output: #0f172a; --bg-overlay: rgba(15,23,42,0.95);
  --text-primary: #f1f5f9; --text-secondary: #94a3b8; --text-muted: #64748b;
  --border: #334155; --border-focus: #475569;
  --pass: #22c55e; --pass-bg: rgba(34,197,94,0.12); --pass-glow: rgba(34,197,94,0.3);
  --fail: #ef4444; --fail-bg: rgba(239,68,68,0.12); --fail-glow: rgba(239,68,68,0.3);
  --warn: #f59e0b; --warn-bg: rgba(245,158,11,0.12);
  --accent: #6366f1; --accent-bg: rgba(99,102,241,0.12); --accent-glow: rgba(99,102,241,0.25);
  --gradient-hero: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
  --gradient-pass: linear-gradient(135deg, #22c55e 0%, #10b981 100%);
  --gradient-fail: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
  --radius: 10px; --radius-lg: 16px;
  --shadow: 0 4px 24px rgba(0,0,0,0.3); --shadow-glow: 0 0 30px var(--accent-glow);
  --transition: 0.25s cubic-bezier(0.4,0,0.2,1);
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  --font-mono: "SF Mono", "Fira Code", "JetBrains Mono", "Cascadia Code", monospace;
}
/* ===== 重置 & 基础 ===== */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font-sans);background:var(--bg-primary);color:var(--text-primary);line-height:1.6;overflow-x:hidden}
a{color:var(--accent);text-decoration:none}
code{font-family:var(--font-mono);background:var(--bg-primary);padding:2px 6px;border-radius:4px;font-size:0.85em}
pre{font-family:var(--font-mono);white-space:pre-wrap;word-wrap:break-word}

/* ===== Hero 区域 ===== */
.hero{background:var(--gradient-hero);padding:48px 32px 40px;position:relative;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")}
.hero-content{position:relative;max-width:1400px;margin:0 auto}
.hero h1{font-size:2rem;font-weight:800;letter-spacing:-0.02em;color:#fff;margin-bottom:4px}
.hero .subtitle{color:rgba(255,255,255,0.7);font-size:1rem;margin-bottom:24px}

/* 状态指示器 */
.status-indicator{display:inline-flex;align-items:center;gap:12px;padding:10px 24px;border-radius:999px;font-weight:700;font-size:1.25rem;letter-spacing:0.05em;backdrop-filter:blur(12px)}
.status-indicator.passed{background:rgba(34,197,94,0.2);border:1.5px solid rgba(34,197,94,0.5);color:#86efac;box-shadow:0 0 40px rgba(34,197,94,0.2)}
.status-indicator.failed{background:rgba(239,68,68,0.2);border:1.5px solid rgba(239,68,68,0.5);color:#fca5a5;box-shadow:0 0 40px rgba(239,68,68,0.2)}
.status-dot{width:12px;height:12px;border-radius:50%;animation:pulse 2s ease-in-out infinite}
.status-indicator.passed .status-dot{background:var(--pass);box-shadow:0 0 12px var(--pass)}
.status-indicator.failed .status-dot{background:var(--fail);box-shadow:0 0 12px var(--fail)}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.6;transform:scale(0.85)}}

/* ===== 指标卡片 ===== */
.metrics{max-width:1400px;margin:-28px auto 0;padding:0 32px;position:relative;z-index:1}
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.metric-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:16px;text-align:center;transition:transform var(--transition),box-shadow var(--transition)}
.metric-card:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.metric-label{font-size:0.75rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-muted);margin-bottom:4px}
.metric-value{font-size:1.4rem;font-weight:800;color:var(--text-primary)}

/* ===== 容器 ===== */
.container{max-width:1400px;margin:0 auto;padding:0 32px}

/* ===== 轮次导航标签 ===== */
.round-tabs{display:flex;gap:8px;margin:24px 0 16px;flex-wrap:wrap}
.round-tab{padding:8px 20px;border-radius:999px;font-size:0.85rem;font-weight:600;cursor:pointer;border:1.5px solid var(--border);background:var(--bg-secondary);color:var(--text-secondary);transition:all var(--transition);user-select:none}
.round-tab:hover{border-color:var(--accent);color:var(--text-primary)}
.round-tab.active{background:var(--accent);border-color:var(--accent);color:#fff;box-shadow:0 0 16px var(--accent-glow)}
.round-tab .tab-verdict{margin-left:8px;font-size:0.75rem;padding:2px 8px;border-radius:999px}
.round-tab .tab-verdict.pass{background:var(--pass-bg);color:var(--pass)}
.round-tab .tab-verdict.fail{background:var(--fail-bg);color:var(--fail)}

/* ===== 轮次面板 ===== */
.round-panel{display:none;animation:fadeIn 0.3s ease}
.round-panel.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

/* ===== 4 维度判定区域 ===== */
.verdict-section{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:24px;margin-bottom:20px}
.verdict-section h3{font-size:1rem;margin-bottom:16px;color:var(--text-primary);display:flex;align-items:center;gap:8px}
.verdict-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}
@media(max-width:900px){.verdict-grid{grid-template-columns:1fr}}

/* 维度进度条 */
.dim-bars{display:flex;flex-direction:column;gap:14px}
.dim-bar-item{display:flex;flex-direction:column;gap:4px}
.dim-bar-label{display:flex;justify-content:space-between;align-items:center;font-size:0.85rem}
.dim-bar-label span:first-child{color:var(--text-secondary)}
.dim-bar-label .dim-status{font-weight:700;font-size:0.8rem;padding:2px 8px;border-radius:4px}
.dim-bar-label .dim-status.pass{background:var(--pass-bg);color:var(--pass)}
.dim-bar-label .dim-status.fail{background:var(--fail-bg);color:var(--fail)}
.dim-bar-track{height:8px;background:var(--bg-primary);border-radius:4px;overflow:hidden}
.dim-bar-fill{height:100%;border-radius:4px;transition:width 0.8s cubic-bezier(0.25,0.46,0.45,0.94)}
.dim-bar-fill.pass{background:var(--gradient-pass)}
.dim-bar-fill.fail{background:var(--gradient-fail)}

/* 不一致 & 修复信息 */
.verdict-details{display:flex;flex-direction:column;gap:16px}
.verdict-info-card{background:var(--bg-primary);border:1px solid var(--border);border-radius:var(--radius);padding:16px}
.verdict-info-card h4{font-size:0.8rem;text-transform:uppercase;letter-spacing:0.06em;color:var(--text-muted);margin-bottom:8px}
.verdict-info-card p{font-size:0.9rem;color:var(--text-secondary);line-height:1.7;white-space:pre-wrap}

/* ===== 输出区域（垂直堆叠） ===== */
.output-header-section{display:flex;align-items:center;justify-content:space-between;margin:24px 0 16px;flex-wrap:wrap;gap:12px}
.output-header-section h3{font-size:1rem;color:var(--text-primary)}
.gallery-btn{padding:6px 14px;border-radius:6px;font-size:0.8rem;font-weight:600;border:1px solid var(--border);background:var(--bg-secondary);color:var(--text-secondary);cursor:pointer;transition:all var(--transition)}
.gallery-btn:hover{border-color:var(--accent);color:var(--text-primary);background:var(--accent-bg)}

.output-section{border:1.5px solid var(--border);border-radius:var(--radius);overflow:hidden;margin-bottom:16px;transition:all var(--transition)}
.output-section.fail{border-color:rgba(239,68,68,0.5)}
.output-section.pass{border-color:rgba(34,197,94,0.3)}

.output-header{padding:14px 16px;display:flex;align-items:center;justify-content:space-between;background:var(--bg-secondary);border-bottom:1px solid var(--border)}
.output-title{font-weight:700;font-size:0.95rem;color:var(--text-primary)}
.output-title .tester-id{color:var(--accent);margin-right:4px;background:var(--accent-bg);padding:2px 8px;border-radius:4px;font-size:0.85rem}
.output-status{font-size:0.7rem;font-weight:700;padding:3px 12px;border-radius:999px;text-transform:uppercase;letter-spacing:0.05em}
.output-status.pass{background:var(--pass-bg);color:var(--pass)}
.output-status.fail{background:var(--fail-bg);color:var(--fail)}

.output-content{min-height:200px;max-height:600px;overflow:auto;background:var(--bg-primary)}
.output-content pre{margin:0;padding:16px;background:var(--bg-output);color:var(--text-secondary);font-family:var(--font-mono);font-size:0.85rem;line-height:1.7;word-wrap:break-word;white-space:pre-wrap}
.output-content iframe{width:100%;min-height:500px;border:none;background:#fff;display:block}

/* ===== 对比模式 Overlay ===== */
.compare-overlay{display:none;position:fixed;inset:0;background:var(--bg-overlay);z-index:1000;backdrop-filter:blur(8px)}
.compare-overlay.active{display:flex;flex-direction:column}

.compare-overlay-toolbar{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;border-bottom:1px solid var(--border);background:var(--bg-primary)}
.compare-overlay-title{font-weight:700;font-size:1rem;color:var(--text-primary)}
.compare-overlay-actions{display:flex;gap:8px}
.preview-btn{padding:8px 16px;border-radius:6px;font-size:0.85rem;font-weight:600;border:1px solid var(--border);background:var(--bg-secondary);color:var(--text-secondary);cursor:pointer;transition:all var(--transition)}
.preview-btn:hover{border-color:var(--accent);color:var(--text-primary);background:var(--accent-bg)}
.preview-btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.preview-btn.primary:hover{opacity:0.9}

.compare-overlay-content{flex:1;display:flex;overflow:hidden}

/* ===== 双面板对比视图 ===== */
.compare-view{display:none;flex-direction:column;height:calc(100vh - 73px)}
.compare-view.active{display:flex}
.compare-toolbar{display:flex;align-items:center;justify-content:space-between;padding:12px 24px;border-bottom:1px solid var(--border);background:var(--bg-primary)}
.compare-panels{display:flex;flex:1;overflow:hidden}
.compare-panel{flex:1;display:flex;flex-direction:column;border-right:1px solid var(--border)}
.compare-panel:last-child{border-right:none}

.compare-panel-header{padding:12px 16px;border-bottom:1px solid var(--border);background:var(--bg-secondary);display:flex;align-items:center;gap:8px}
.compare-panel-selector{flex:1;padding:6px 12px;border-radius:6px;border:1px solid var(--border);background:var(--bg-primary);color:var(--text-primary);font-size:0.85rem;cursor:pointer}
.compare-panel-status{font-size:0.7rem;font-weight:700;padding:2px 8px;border-radius:999px}
.compare-panel-status.pass{background:var(--pass-bg);color:var(--pass)}
.compare-panel-status.fail{background:var(--fail-bg);color:var(--fail)}

.compare-panel-content{flex:1;overflow:auto;padding:16px;background:var(--bg-primary)}
.compare-panel-content pre{margin:0;padding:16px;background:var(--bg-output);color:var(--text-secondary);font-family:var(--font-mono);font-size:0.85rem;line-height:1.7;border-radius:var(--radius);white-space:pre-wrap;word-wrap:break-word}
.compare-panel-content iframe{width:100%;min-height:100%;border:none;background:#fff;border-radius:var(--radius)}

/* 同步滚动开关 */
.sync-scroll-toggle{display:flex;align-items:center;gap:8px;font-size:0.8rem;color:var(--text-secondary);cursor:pointer;user-select:none}
.sync-scroll-toggle input{accent-color:var(--accent);width:14px;height:14px}

/* ===== 时间线 ===== */
.timeline-section{margin-top:32px}
.timeline-section h3{font-size:1rem;margin-bottom:16px;color:var(--text-primary)}
.timeline{position:relative;padding-left:28px}
.timeline::before{content:"";position:absolute;left:9px;top:4px;bottom:4px;width:2px;background:var(--border);border-radius:1px}
.tl-item{position:relative;margin-bottom:20px}
.tl-item::before{content:"";position:absolute;left:-23px;top:6px;width:12px;height:12px;border-radius:50%;border:2.5px solid var(--pass);background:var(--bg-primary);z-index:1}
.tl-item.fail::before{border-color:var(--fail)}
.tl-item .tl-time{font-size:0.75rem;color:var(--text-muted);margin-bottom:2px}
.tl-item .tl-title{font-weight:700;font-size:0.95rem;margin-bottom:4px}
.tl-item .tl-tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
.tl-dim{font-size:0.7rem;padding:2px 8px;border-radius:4px;font-weight:600}
.tl-dim.pass{background:var(--pass-bg);color:var(--pass)}
.tl-dim.fail{background:var(--fail-bg);color:var(--fail)}
.tl-fix{margin-top:8px;font-size:0.85rem;color:var(--text-secondary);padding:8px 12px;background:var(--accent-bg);border-radius:6px;border-left:3px solid var(--accent)}

/* ===== 页脚 ===== */
.footer{margin-top:48px;padding:20px 0;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;font-size:0.8rem;color:var(--text-muted)}
.footer a{color:var(--accent)}
</style>
</head>
<body>

<!-- ===== Hero ===== -->
<section class="hero">
  <div class="hero-content">
    <h1>Skill 并行验证测试报告</h1>
    <p class="subtitle">{test_name}</p>
    <div class="status-indicator {passed/failed}">
      <span class="status-dot"></span>
      {PASSED/FAILED}
    </div>
  </div>
</section>

<!-- ===== 指标卡片 ===== -->
<section class="metrics">
  <div class="metrics-grid">
    <div class="metric-card"><div class="metric-label">被测 Skill</div><div class="metric-value" style="font-size:0.85rem;word-break:break-all">{skill_path}</div></div>
    <div class="metric-card"><div class="metric-label">验证结果</div><div class="metric-value" style="color:{var(--pass)/var(--fail)}">{PASSED/FAILED}</div></div>
    <div class="metric-card"><div class="metric-label">通过轮次</div><div class="metric-value">{pass_round}</div></div>
    <div class="metric-card"><div class="metric-label">总轮次</div><div class="metric-value">{total_rounds}</div></div>
    <div class="metric-card"><div class="metric-label">备份位置</div><div class="metric-value" style="font-size:0.75rem;word-break:break-all">{backup_path}</div></div>
  </div>
</section>

<div class="container">

<!-- ===== 轮次导航 ===== -->
<h2 style="font-size:1rem;margin:28px 0 0;color:var(--text-primary)">轮次详情</h2>
<div class="round-tabs">
  <!-- 每轮一个标签 -->
  <div class="round-tab {active}" onclick="switchRound({N})" data-round="{N}">
    第 {N} 轮
    <span class="tab-verdict {pass/fail}">{pass/fail}</span>
  </div>
</div>

<!-- ===== 各轮面板 ===== -->
<!-- 每轮一个 round-panel -->
<div class="round-panel {active}" id="round-{N}">

  <!-- 4 维度判定 -->
  <div class="verdict-section">
    <h3>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 22 12 18.56 5.82 22 7 14.14l-5-4.87 6.91-1.01L12 2z"/></svg>
      测试主管判定
    </h3>
    <div class="verdict-grid">
      <!-- 左：维度进度条 -->
      <div class="dim-bars">
        <div class="dim-bar-item">
          <div class="dim-bar-label"><span>功能完整性</span><span class="dim-status {pass/fail}">{PASS/FAIL}</span></div>
          <div class="dim-bar-track"><div class="dim-bar-fill {pass/fail}" style="width:{100/0}%"></div></div>
        </div>
        <div class="dim-bar-item">
          <div class="dim-bar-label"><span>输出类型一致</span><span class="dim-status {pass/fail}">{PASS/FAIL}</span></div>
          <div class="dim-bar-track"><div class="dim-bar-fill {pass/fail}" style="width:{100/0}%"></div></div>
        </div>
        <div class="dim-bar-item">
          <div class="dim-bar-label"><span>关键属性匹配</span><span class="dim-status {pass/fail}">{PASS/FAIL}</span></div>
          <div class="dim-bar-track"><div class="dim-bar-fill {pass/fail}" style="width:{100/0}%"></div></div>
        </div>
        <div class="dim-bar-item">
          <div class="dim-bar-label"><span>质量水平相当</span><span class="dim-status {pass/fail}">{PASS/FAIL}</span></div>
          <div class="dim-bar-track"><div class="dim-bar-fill {pass/fail}" style="width:{100/0}%"></div></div>
        </div>
      </div>
      <!-- 右：不一致详情 + 修复说明 -->
      <div class="verdict-details">
        <div class="verdict-info-card">
          <h4>不一致详情</h4>
          <p>{inconsistencies}</p>
        </div>
        <!-- 若有修复 -->
        <div class="verdict-info-card">
          <h4>修复说明</h4>
          <p>{fix_description}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- 测试专家输出区域（垂直堆叠） -->
  <div class="output-header-section">
    <h3>测试专家输出</h3>
    <button class="gallery-btn" onclick="enterCompareMode({N})">对比模式</button>
  </div>

  <!-- 测试专家 1 -->
  <div class="output-section {pass/fail}">
    <div class="output-header">
      <span class="output-title"><span class="tester-id">T1</span> 测试专家 1</span>
      <span class="output-status {pass/fail}">{status}</span>
    </div>
    <div class="output-content" id="output-t1-{N}">
      <!-- HTML 类型：<iframe srcdoc="{content}" onload="autoResizeIframe(this)"></iframe> -->
      <!-- TEXT 类型：<pre>{content}</pre> -->
    </div>
  </div>

  <!-- 测试专家 2 -->
  <div class="output-section {pass/fail}">
    <div class="output-header">
      <span class="output-title"><span class="tester-id">T2</span> 测试专家 2</span>
      <span class="output-status {pass/fail}">{status}</span>
    </div>
    <div class="output-content" id="output-t2-{N}">
      <!-- 输出内容 -->
    </div>
  </div>

  <!-- 测试专家 3 -->
  <div class="output-section {pass/fail}">
    <div class="output-header">
      <span class="output-title"><span class="tester-id">T3</span> 测试专家 3</span>
      <span class="output-status {pass/fail}">{status}</span>
    </div>
    <div class="output-content" id="output-t3-{N}">
      <!-- 输出内容 -->
    </div>
  </div>

</div>

<!-- ===== 对比模式 Overlay ===== -->
<div class="compare-overlay" id="compare-overlay">
  <div class="compare-overlay-toolbar">
    <span class="compare-overlay-title">对比视图</span>
    <div class="compare-overlay-actions">
      <label class="sync-scroll-toggle">
        <input type="checkbox" id="sync-scroll-checkbox" checked>
        同步滚动
      </label>
      <button class="preview-btn" onclick="closeCompare()">关闭</button>
    </div>
  </div>

  <!-- 对比视图 -->
  <div class="compare-view" id="compare-view">
    <div class="compare-toolbar">
      <span style="font-size:0.85rem;color:var(--text-muted)">对比两台测试专家的输出</span>
    </div>
    <div class="compare-panels">
      <div class="compare-panel">
        <div class="compare-panel-header">
          <select class="compare-panel-selector" id="compare-left-selector" onchange="updateComparePanel('left', this.value)">
            <option value="1">测试专家 1</option>
            <option value="2">测试专家 2</option>
            <option value="3">测试专家 3</option>
          </select>
          <span class="compare-panel-status" id="compare-left-status">{status}</span>
        </div>
        <div class="compare-panel-content" id="compare-left-content" data-sync-scroll="compare">
          <!-- 内容动态填充 -->
        </div>
      </div>
      <div class="compare-panel">
        <div class="compare-panel-header">
          <select class="compare-panel-selector" id="compare-right-selector" onchange="updateComparePanel('right', this.value)">
            <option value="1">测试专家 1</option>
            <option value="2" selected>测试专家 2</option>
            <option value="3">测试专家 3</option>
          </select>
          <span class="compare-panel-status" id="compare-right-status">{status}</span>
        </div>
        <div class="compare-panel-content" id="compare-right-content" data-sync-scroll="compare">
          <!-- 内容动态填充 -->
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ===== 测试过程时间线 ===== -->
<div class="timeline-section">
  <h3>测试过程</h3>
  <div class="timeline">
    <!-- 每轮一个时间线节点 -->
    <div class="tl-item {pass/fail}">
      <div class="tl-time">{started_at} - {completed_at}</div>
      <div class="tl-title">第 {N} 轮</div>
      <div class="tl-tags">
        <span class="tl-dim {pass/fail}">功能完整性:{pass/fail}</span>
        <span class="tl-dim {pass/fail}">输出类型:{pass/fail}</span>
        <span class="tl-dim {pass/fail}">关键属性:{pass/fail}</span>
        <span class="tl-dim {pass/fail}">质量水平:{pass/fail}</span>
      </div>
      <!-- 若 fail -->
      <div class="tl-fix">修复：{修复说明}</div>
    </div>
  </div>
</div>

<!-- ===== 页脚 ===== -->
<div class="footer">
  <span>报告生成时间：{generated_at} | skill-parallel-verify v1.1.0</span>
  <span>备份：<code>{backup_path}</code></span>
</div>

</div><!-- /.container -->

<!-- ===== 交互脚本 ===== -->
<script>
// 轮次切换
function switchRound(n) {
  document.querySelectorAll('.round-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.round-panel').forEach(p => p.classList.remove('active'));
  const tab = document.querySelector('.round-tab[data-round="'+n+'"]');
  if (tab) tab.classList.add('active');
  const panel = document.getElementById('round-'+n);
  if (panel) panel.classList.add('active');
}

// 测试数据（生成时填充）
const testerData = {
  {N}: {
    1: { type: '{tester_1_output_type}', content: '{tester_1_output_content}', status: '{status}' },
    2: { type: '{tester_2_output_type}', content: '{tester_2_output_content}', status: '{status}' },
    3: { type: '{tester_3_output_type}', content: '{tester_3_output_content}', status: '{status}' }
  }
};

let currentRound = 1;
let isCompareMode = false;

// 渲染内联输出
function renderInlineOutput(round) {
  for (let i = 1; i <= 3; i++) {
    const data = testerData[round][i];
    const container = document.getElementById('output-t' + i + '-' + round);
    if (container && data) {
      if (data.type === 'html') {
        container.innerHTML = '<iframe srcdoc="' + escapeHtml(data.content) + '" onload="autoResizeIframe(this)"></iframe>';
      } else {
        container.innerHTML = '<pre>' + escapeHtml(data.content) + '</pre>';
      }
    }
  }
}

// iframe 自动调整高度
function autoResizeIframe(iframe) {
  try {
    iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 'px';
  } catch (e) {
    // 跨域限制时保持默认高度
    iframe.style.height = '500px';
  }
}

// 渲染对比面板
function renderComparePanel(panelId, data) {
  const panel = document.getElementById(panelId);
  if (data.type === 'html') {
    panel.innerHTML = '<iframe srcdoc="' + escapeHtml(data.content) + '" onload="autoResizeIframe(this)"></iframe>';
  } else {
    panel.innerHTML = '<pre>' + escapeHtml(data.content) + '</pre>';
  }
}

// 进入对比模式
function enterCompareMode(round) {
  currentRound = round;
  isCompareMode = true;

  const overlay = document.getElementById('compare-overlay');

  // 默认左边选T1，右边选T2
  document.getElementById('compare-left-selector').value = '1';
  document.getElementById('compare-right-selector').value = '2';
  updateComparePanel('left', '1');
  updateComparePanel('right', '2');

  overlay.classList.add('active');
  document.body.style.overflow = 'hidden';
}

// 关闭对比模式
function closeCompare() {
  isCompareMode = false;
  const overlay = document.getElementById('compare-overlay');
  overlay.classList.remove('active');
  document.body.style.overflow = '';
}

// 更新对比面板
function updateComparePanel(side, testerId) {
  const data = testerData[currentRound][testerId];
  const panelId = 'compare-' + side + '-content';
  const statusId = 'compare-' + side + '-status';

  renderComparePanel(panelId, data);

  const statusEl = document.getElementById(statusId);
  statusEl.textContent = data.status.toUpperCase();
  statusEl.className = 'compare-panel-status ' + data.status;
}

// 转义 HTML
function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML.replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

// 对比视图同步滚动
let syncScrollEnabled = true;
document.getElementById('sync-scroll-checkbox')?.addEventListener('change', function(e) {
  syncScrollEnabled = e.target.checked;
});

document.addEventListener('scroll', function(e) {
  if (!syncScrollEnabled || !isCompareMode) return;
  const el = e.target;
  if (!el.hasAttribute('data-sync-scroll')) return;
  const group = el.getAttribute('data-sync-scroll');
  if (group !== 'compare') return;

  const siblings = document.querySelectorAll('[data-sync-scroll="compare"]');
  if (el.tagName === 'PRE') {
    const ratio = el.scrollTop / (el.scrollHeight - el.clientHeight || 1);
    siblings.forEach(s => {
      if (s !== el && s.tagName === 'PRE') {
        s.scrollTop = ratio * (s.scrollHeight - s.clientHeight);
      }
    });
  }
}, true);

// ESC 关闭对比
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && isCompareMode) closeCompare();
});

// 页面加载时渲染所有内联输出
window.addEventListener('load', function() {
  // 获取所有轮次并渲染
  const rounds = Object.keys(testerData);
  rounds.forEach(round => renderInlineOutput(round));
});
</script>

</body>
</html>
```

**HTML 生成规则**：
1. 所有 CSS/JS 内联，零外部依赖，单文件可在浏览器打开
2. **直接内联渲染**：3 个测试专家输出直接在页面中渲染，HTML 用 iframe srcdoc，文本用 pre 代码块
3. **2 面板对比**：点击"对比"按钮进入全屏对比视图，选择两个测试专家并排对比
4. **4 维度进度条**：可视化展示判定结果，pass 全绿 / fail 红色渐变
5. 每轮测试专家输出**完整展示**，不截断摘要
6. 最后一轮默认激活（tab active），其余轮次通过标签切换
7. 失败测试专家的输出区域边框高亮为红色
8. 暗色主题，渐变 + 动画，核心状态无需阅读文字即可感知
9. 替换所有 `{占位符}` 为实际数据，移除注释占位行
10. `round-tab` 的 `onclick` 参数和 `data-round` 属性需用实际轮次数字替换

**同时生成 markdown 报告**：在 `verification.json` 同目录下生成 `final-report.md`（简版），供 Git 提交和 Dima 同步使用。

---

## Quick Reference

| 步骤 | 操作 | 门控条件 |
|------|------|---------|
| 1 | 解析与校验 test-case YAML | 校验通过 |
| 2 | 备份原始 Skill 到 backups/ | 备份完成 |
| 3 | 创建工作目录（或断点恢复） | 就绪 |
| 4 | 顺序启动 3 个测试专家 | 3 份输出收集完成（成功数 >= 2） |
| 5 | 测试主管判定（4 维度框架） | 判定结果为 pass/fail |
| 6 | Skill 专家修复（fail 时） | 修复完成，回到步骤 4 |
| 7 | 生成 HTML 报告 + markdown 简报 | 报告输出完毕 |

---

## 错误处理

| 错误 | 处理策略 |
|------|---------|
| test-case 文件不存在 | 报错退出，提示用户检查文件路径 |
| skill_path 指向的 SKILL.md 不存在 | 报错退出，提示用户检查被测 Skill 路径 |
| test-case YAML 格式错误 | 报错退出，提示具体格式错误 |
| 测试专家 subagent 超时/崩溃 | 标记为 timeout/crash，使用已有成功结果继续判定；成功数 < 2 则本轮 fail |
| 测试专家输出为空 | 标记为 empty_output，视为不一致，进入修复循环 |
| 测试主管 subagent 失败 | 重试一次，仍失败则在主会话中内联判定 |
| Skill 专家 subagent 失败 | 重试一次，仍失败则标记 fix_failed，进入下轮测试 |
| 连续 3 轮 fix_failed | 提前中止，生成失败报告（备注：Skill 专家持续失败） |
| 修复超过 10 轮 | 生成失败报告，提示用户可从 backups/ 恢复 |
| 中断后恢复 | 检测 verification.json 断点，从断点继续（见 Step 3） |