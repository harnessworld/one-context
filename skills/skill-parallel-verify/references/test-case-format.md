# Test Case 文件格式说明

## 概述

Test Case 文件是 YAML 格式，用于定义 skill-parallel-verify 的测试参数。

## 字段定义

### 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_path` | string | 被测 Skill 的 SKILL.md 文件路径（相对项目根目录） |
| `test_name` | string | 测试名称，用于报告标题 |
| `test_cases` | array | 测试用例列表，至少包含 1 个用例 |

### 可选字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `acceptance_criteria` | string | 使用 prompt 本身 | 验收标准描述，测试主管据此判定输出是否合格 |
| `description` | string | 空 | 测试目的的整体描述 |

### test_cases 数组元素字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 测试用例唯一标识（如 tc-1） |
| `prompt` | string | 是 | 模拟用户调用被测 Skill 的输入提示词 |
| `description` | string | 否 | 测试用例的目的描述 |

## 当前限制

- 当前版本仅使用 `test_cases[0]`（第一个测试用例）执行并行验证
- 多测试用例支持将在后续版本实现

## 格式规范

```yaml
# skill-parallel-verify test-case format v1

# ===== 必填字段 =====
skill_path: "skills/xxx/skill-name/SKILL.md"
test_name: "测试名称"

# ===== 可选字段 =====
acceptance_criteria: "验收标准描述"
description: "测试目的的整体描述"

# ===== 测试用例 =====
test_cases:
  - id: tc-1
    prompt: "用户输入的提示词"
    description: "测试目的描述"
```

## 示例

### 示例 1：html-ppt Skill 商务风格测试

```yaml
skill_path: "skills/html-slides/SKILL.md"
test_name: "html-ppt Skill 商务风格测试"
acceptance_criteria: "生成的 PPT 应为商务风格，包含标题页和至少 3 页内容"

test_cases:
  - id: tc-1
    prompt: "帮我做一个商务风格的PPT，主题是2026年Q1季度营收汇报"
    description: "测试商务风格PPT生成能力"
```

### 示例 2：知识库导入 Skill 测试

```yaml
skill_path: "skills/kb-lint/SKILL.md"
test_name: "kb-lint Skill 检查能力测试"
acceptance_criteria: "能正确识别知识库文档中的格式问题，输出结构化的检查报告"

test_cases:
  - id: tc-1
    prompt: "检查 knowledge/external/opencli/ 目录下的文档格式"
    description: "测试知识库文档格式检查能力"
```