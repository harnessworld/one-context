---
name: diagram-tag
description: >-
  读取图片或分析文字描述，生成内容标签并匹配/生成画图提示词。支持批量处理多张图片，生成后自动验证。
  触发词："/diagram-tag" "标签图" "图片标签" "匹配提示词" "找提示词" "生成提示词" "tag diagram"
---

# Diagram Tag — 图片/文字 → 内容标签 → 提示词

读取用户提供的图片或文字描述，生成内容标签，在路由表中匹配推荐提示词。如果对应提示词尚未生成，则自动生成并验证。

## 何时触发

- 用户说 `/diagram-tag` 并提供一张图片
- 用户说 `/diagram-tag` 并描述想画什么图
- 用户提供多张图片要求批量处理
- 用户问"我该用哪个提示词"、"帮我匹配/生成画图模板"

## 工作流程

### 流程 A：单张图片输入

1. **读图**：分析用户提供的图片，识别其内容类型和结构特征
2. **提取标签**：从"内容标签词汇表"中选取 1-3 个最匹配的标签
3. **查路由表**：读取 `knowledge/prompts/diagram/ROUTING.md`，用标签匹配推荐 prompt-N
4. **检查 prompt 文件是否存在**：
   - 如果 `knowledge/prompts/diagram/prompt-N-xxx.md` 已存在 → 读取其 YAML frontmatter，从 `exemplar_image` 字段获取对应参考图路径；如果 `exemplar_image` 为 null 则说明无参考图
   - 如果不存在 → 进入"流程 C：生成提示词"
5. **返回结果**：输出标签、推荐提示词编号、对应参考图文件名（来自 frontmatter）

### 流程 B：文字输入

1. **分析描述**：从用户文字中提取关键词
2. **映射标签**：用 ROUTING.md 的"标签提取指南"将关键词映射到内容标签
3. **查路由表**：同上
4. **检查 prompt 文件是否存在**：同流程 A 步骤 4
5. **返回结果**：同上

### 流程 C：生成提示词（prompt 文件不存在时触发）

当输入的是图片，且知识库中还没有对应的 prompt 文件时：

1. **确定编号**：查 `knowledge/prompts/diagram/` 目录下最大的 prompt 编号 N，新文件编号为 N+1
2. **读图分析**：逐区域描述图片的视觉特征（布局结构、区域占比、配色 hex 值、组件、图标、箭头风格、字体层级）
3. **生成 prompt 文件**：写入 `knowledge/prompts/diagram/prompt-(N+1)-<简短主题名>.md`，格式遵循下方的"Prompt 文件格式规范"；**必须包含 YAML frontmatter**，其中 `prompt_id`、`slug`、`exemplar_image`、`tags` 由本步骤填入
4. **复制参考图**：将原始图片复制为 `knowledge/prompts/diagram/images/exemplar-<简短主题名>.<ext>`
5. **验证**：进入"流程 E：验证循环"
6. **验证通过后更新索引**：
   - 在 `knowledge/prompts/diagram/prompts.md` 的索引表追加一行
   - 在 `knowledge/prompts/diagram/README.md` 的"提示词与色系对照"表追加一行
   - 在 `knowledge/prompts/diagram/ROUTING.md` 的标签路由表追加对应标签行（如现有标签不够用，在词汇表里追加新标签）
7. **返回生成结果**

### 流程 D：批量处理多张图片

当用户提供多张图片时：

1. **逐张处理**：对每张图片，启动一个干净的 subagent（Task tool），subagent 内执行 `/diagram-tag` 的完整流程 A+C+E
2. **顺序执行**：必须逐张顺序处理，不要并发——并发会触发 API 限流
3. **汇总报告**：全部完成后，输出批量处理汇总表

批量执行的伪代码：

```
for each image in images:
    result = Task(subagent_type="general-purpose", prompt="""
        执行 diagram-tag skill：
        1. 读取 knowledge/prompts/diagram/ROUTING.md 获取路由表
        2. 读取图片 {image_path}，提取内容标签
        3. 查路由表匹配 prompt
        4. 如果 prompt 文件不存在，生成 prompt 文件、复制参考图
        5. 执行验证循环（流程 E）
        6. 验证通过后更新索引文件
        7. 返回结果
    """)
    collect result
output summary table
```

### 流程 E：验证循环

生成 prompt 后，必须经过验证才能入库。验证逻辑：

**前置步骤**：读取 prompt 文件的 YAML frontmatter，获取 `exemplar_image` 字段作为参考图路径。如果 `exemplar_image` 为 null（无参考图），跳过验证循环，直接标记为"无参考图，跳过验证"。

```
round = 0
max_rounds = 10
image_path = frontmatter.exemplar_image  # 相对于 knowledge/prompts/diagram/

while round < max_rounds:
    round += 1

    # 1. 启动 verify subagent（干净上下文，图优先）
    verify_result = Task(subagent_type="general-purpose", prompt="""
        你是提示词验证员。任务（严格按此顺序执行，不得调换）：

        第一步·看图（不看 prompt）：
        1. 读取参考图片 {image_path}
        2. 逐区域客观描述你看到的视觉内容：布局结构、颜色（尝试给出 hex）、文字内容、元素数量、箭头方向、位置关系
        3. 输出到"图片观察"列

        第二步·读 prompt：
        1. 读取 prompt 文件 {prompt_file_path}（跳过 frontmatter，只读提示词正文）
        2. 逐区域提取 prompt 中的具体声明：hex 色值、文字内容、元素数量、位置占比、箭头方向
        3. 输出到"prompt 声明"列

        第三步·逐项比对（逐条声明检查，不是模糊印象）：
        1. 将 prompt 的每条声明与图片观察逐项比对
        2. 对每条声明给出判定：
           - 精确匹配：声明与观察完全一致
           - 可接受偏差：声明与观察有小差异但语义一致（见"可接受偏差"规则）
           - 实质性差异：声明与观察不一致，或声明遗漏了图片中的显著特征
        3. 按"验证输出格式"输出结果

        重要：你必须先完成看图再读 prompt，避免用 prompt 内容"引导"你对图片的观察。
    """)

    # 2. 判断是否通过
    if verify_result.passed:
        break  # 验证通过，退出循环
    if verify_result.conditional_pass:
        记录差异项到 prompt 文件 frontmatter：在 adjacent 字段追加（如无此字段则新建）
        break  # 条件通过，接受但不修改

    # 3. 未通过，启动修改 subagent（携带 verify 反馈）
    modify_result = Task(subagent_type="general-purpose", prompt="""
        你是提示词修改员。任务：
        1. 读取当前 prompt 文件 {prompt_file_path}
        2. 读取参考图片 {image_path}
        3. 根据以下验证反馈，针对性修改 prompt：

        {verify_result.feedback}

        4. 修改原则：只改反馈中指出的差异点，不动已通过的部分
        5. 将修改后的 prompt 写回 {prompt_file_path}
    """)

    # 继续下一轮验证

# 循环结束
if round >= max_rounds:
    报告警告：验证循环已达上限 {max_rounds} 次，prompt 可能仍存在差异，请人工检查
```

**关键设计**：
- verify subagent 用**干净上下文**，避免先入为主
- **图优先验证**：必须先看图描述，再读 prompt 逐条比对，防止用 prompt 内容"引导"图片观察
- 逐条声明比对而非模糊区域匹配，每条 prompt 声明都需与图片观察单独比对
- 修改 subagent 携带 verify 的具体反馈，**针对性修改而非全盘重写**
- 每轮只改差异点，不改已通过的部分，防止振荡

#### 验证输出格式

verify subagent 必须按以下格式输出：

```markdown
## 验证结果：[通过/条件通过/未通过]

### 逐区域逐项比对

| 区域 | prompt 声明 | 图片观察 | 判定 | 差异说明 |
|------|-----------|---------|------|---------|
| GLOBAL STYLE | 背景色 #FFFFFF | 底色为纯白 #FFFFFF | 精确匹配 | — |
| GLOBAL STYLE | 主色 #E8913A | 橙色标题线，约 #E8913A | 精确匹配 | — |
| 区域1 (0%–18%) | 标题文字"Hermes Agent 对象拆解" | 标题文字"Hermes Agent 对象拆解" | 精确匹配 | — |
| 区域1 (0%–18%) | 3个菱形图标 | 仅2个菱形图标 | 实质性差异 | prompt 多声明了1个图标 |
| 区域2 (18%–55%) | 橙色竖线装饰4px宽 | 橙色竖线装饰约4px宽 | 可接受偏差 | 宽度目测接近 |
| ... | ... | ... | ... | ... |

### 统计
- 精确匹配：N 项
- 可接受偏差：N 项
- 实质性差异：N 项

### 实质性差异清单（必须逐条列出）
1. [区域名] prompt 声明 X，图片实际 Y → 应修改 prompt 中的 Z
2. ...

### 可接受偏差清单
1. [区域名] prompt 声明 X，图片实际 Y → 偏差原因（裁剪/渲染差异等）
2. ...
```

#### 判定规则

- **通过**：0 个实质性差异
- **条件通过**：1-2 个实质性差异，且均为非关键性声明（装饰元素数量、辅助图标等）；必须列出差异项
- **未通过**：3 个及以上实质性差异，或任何关键性声明存在实质性差异

**关键性声明**（以下类型的声明不一致直接判为未通过）：
- 文字内容（标题、标签、注释的文字与图片不一致）
- 主色调 hex 值（色差超过 30 ΔE，即肉眼可辨的明显色差）
- 布局结构（层级数量、区域方向、主要元素的上下左右关系）
- 流动方向（箭头方向、数据流方向）

**非关键性声明**（属于条件通过范围）：
- 装饰元素数量（图标数差 1 个、小菱形有无）
- 辅助色的色阶偏移（ΔE < 30，肉眼难以区分）
- 字号差异（同层级字号差 ≤ 2px）
- 间距差异（区域占比差 ≤ 3 个百分点）

**可接受偏差**（不算实质性差异）：
- 渲染引擎差异导致的手绘线条粗细微变
- 图片裁切导致的边缘元素部分缺失（需在偏差清单中注明"裁切所致"）

#### 循环终止条件

1. 验证通过 → 正常退出
2. 达到 10 轮上限 → 输出警告，标记 prompt 为"待人工检查"
3. 连续 2 轮反馈完全相同（说明修改无效）→ 提前终止，输出警告

## Prompt 文件格式规范

生成的 prompt 文件必须遵循以下结构：

```markdown
---
prompt_id: <编号>
slug: <简短主题名>
exemplar_image: images/exemplar-<简短主题名>.<ext>
tags: [<内容标签>]
---

# <主题名> — 图片还原提示词

> 来源: `<原始图片文件名>`
> 类型: <内容标签>
> 适用: 图像生成 AI (Claude / DALL-E / Midjourney / Flux / Ideogram)

## 提示词

\```
Create a <比例> <风格概述> infographic/diagram.

═══════════════════════════════════════
GLOBAL STYLE
═══════════════════════════════════════
- Background: <背景色及描述>
- Primary accent: <主色 hex>
- Secondary accent: <辅色 hex>
- Typography: <字体层级描述>
- Border style: <边框风格>
- Drop shadows: <阴影风格>

═══════════════════════════════════════
<区域1名称> (<起始%>–<结束%> from top)
═══════════════════════════════════════
<详细描述区域内的组件、文字、布局>

...（后续区域）

═══════════════════════════════════════
COLOR PALETTE SUMMARY
═══════════════════════════════════════
| Role | Hex |
|------|-----|
| ...  | ... |

═══════════════════════════════════════
DESIGN ATOMS APPLIED
═══════════════════════════════════════
色彩策略：<从 design-atoms 选>
布局骨架：<从 design-atoms 选>
信息层级：<从 design-atoms 选>
连接语言：<从 design-atoms 选>
元素词汇：<从 design-atoms 选>
情绪基调：<从 design-atoms 选>
\```
```

关键要素：
- **YAML frontmatter**：每个 prompt 文件**必须**包含 frontmatter，字段说明：
  - `prompt_id`：整数编号，与文件名中的 N 对应
  - `slug`：简短英文主题名，与文件名中 `-` 后的部分一致
  - `exemplar_image`：参考图相对于 `knowledge/prompts/diagram/` 的路径；无参考图时为 `null`
  - `tags`：YAML 数组，列出该 prompt 的内容标签（从"内容标签词汇表"中选取）
- **精确配色**：所有颜色必须提供 hex 值，不能只写"蓝色"
- **区域占比**：标注每个区域占画面的百分比（如 "0%–18% from top"）
- **字体层级**：定义 T1~Tn 的字号、粗细、颜色
- **DESIGN ATOMS APPLIED**：末尾必须用 design-atoms 词汇标注六个维度，供路由匹配

## 内容标签词汇表

只使用以下标签，不要自创（除非在生成新 prompt 时发现确实无法覆盖，可追加并同步更新 ROUTING.md）：

| 标签 | 含义 |
|------|------|
| 架构图 | 多层级组件/运行时/系统分层 |
| 流程图 | 转化/蒸馏/Pipeline/单向流动 |
| 概念蓝图 | 围绕核心概念的多维度展开 |
| 模块蓝图 | 能力模型/分岗组合/模块拼装 |
| 安全流程 | 门禁/审核链/逐层过滤 |
| 协作编排 | 多角色切换/Persona+Work 配合 |
| 系统全貌 | 目录结构/概览/一张图讲清全貌 |
| 多入口 | 网关/API聚合/殊途同归 |
| 知识沉淀 | 学习回路/Skill库/经验复用 |
| 技术解析(循环) | Agent Loop/实时流/SSE |
| 技术解析(对比) | 缓存/压缩/before vs after |
| 品牌图 | 暗色品牌风/营销/产品生态/B2B |
| 论文插图 | 学术论文 Figure/管道架构/扁平配色 |

## 路由表与索引文件位置

每次执行都要读取/更新以下文件：

| 文件 | 读取 | 写入(生成 prompt 时) |
|------|:----:|:----:|
| `knowledge/prompts/diagram/ROUTING.md` | ★ | ★（追加标签行） |
| `knowledge/prompts/diagram/prompts.md` | ★ | ★（追加索引行） |
| `knowledge/prompts/diagram/README.md` | ★ | ★（追加色系对照行） |
| `knowledge/prompts/diagram/prompt-N-*.md` | ★ | ★（生成时写入含 frontmatter 的完整文件） |

**Frontmatter 一致性校验**（流程 A/C 读取 prompt 文件时自动执行）：
- `exemplar_image` 字段指向的文件是否存在（null 除外）
- `tags` 字段与 ROUTING.md 中该 prompt 对应的标签是否一致
- 如不一致，输出警告但不阻断流程

## 示例

### 示例 1：图片输入（prompt 已存在）

用户提交一张 Agent 运行时架构图：

```
内容标签：[架构图]
推荐提示词：prompt-8（已存在）
参考图：images/exemplar-hermes-agent-runtime-architecture.jpg
下一步：打开 prompt-8，改内容不改视觉骨架
```

### 示例 2：图片输入（prompt 不存在，需生成+验证）

用户提交一张新的数据湖架构图：

```
内容标签：[架构图, 流程图]
匹配结果：prompt-8 风格接近，但无精确匹配
→ 生成新 prompt：prompt-14-data-lake-architecture.md
→ 复制参考图：images/exemplar-data-lake-architecture.jpg
→ 验证循环：
  [1/10] verify → 2 处「低」匹配（区域2配色、区域3布局）→ 修改
  [2/10] verify → 0 处「低」匹配 → 通过 ✓
→ 已更新：ROUTING.md / prompts.md / README.md
```

### 示例 3：文字输入

用户说："画一个 CI/CD 部署的安全审核流程"

```
内容标签：[安全流程]
推荐提示词：prompt-11（已存在）
参考图：images/exemplar-hermes-agent-security-runtime-gates.jpg
下一步：打开 prompt-11，改内容不改视觉骨架
```

### 示例 4：批量处理

用户提交 5 张图片：

```
正在批量处理 5 张图片（顺序执行）...

[1/5] image-1.png → 标签:[架构图] → prompt-8（已存在） ✓
[2/5] image-2.png → 标签:[流程图] → prompt-15-data-pipeline.md（新生成，验证 2 轮通过） ✓
[3/5] image-3.png → 标签:[品牌图] → prompt-12（已存在） ✓
[4/5] image-4.png → 标签:[概念蓝图] → prompt-16-ai-stack-blueprint.md（新生成，验证 1 轮通过） ✓
[5/5] image-5.png → 标签:[技术解析(对比)] → prompt-3（已存在） ✓

批量处理完成：
- 匹配已有 prompt：3 张
- 新生成 prompt：2 张（prompt-15 验证 2 轮, prompt-16 验证 1 轮）
- 索引文件已更新
```

### 示例 5：验证未通过达到上限

```
→ 生成新 prompt：prompt-17-xxx.md
→ 验证循环：
  [1/10] verify → 3 处「低」匹配 → 修改
  [2/10] verify → 2 处「低」匹配 → 修改
  [3/10] verify → 2 处「低」匹配（与上轮相同，修改无效）→ 提前终止
  ⚠ 验证循环 3 轮未收敛，prompt 标记为"待人工检查"
→ 已更新索引（带标记）
```