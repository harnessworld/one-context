---
id: skill-merge-to-main
title: 选择性合并到主干（Agent Skill）
status: done
primary_repo_id: one-context
---

# 选择性合并到主干

## 目标

在 one-context 伞仓中，将功能分支改动 **按路径** 合入 `main`：**文档、框架元数据、CLI/包、skills** 可合；**业务交付物与个人 Agent 根配置** 默认不合。执行前须向用户展示分类并获 **明确确认**。

## 实现位置

- 技能说明与流程：`skills/merge-to-main/SKILL.md`（权威操作步骤）

## 验收

- 代理能根据 `AGENTS.md` / `features/README.md` 与 `SKILL.md` 中的表格完成分类与咨询。
- 未经用户明确确认，不执行 `git commit` / `git push` 到 `main`。
