# 输出规范

## 文件命名

格式：`[YYYY-MM-DD]_[文章标题关键词]-爆款分析.md`

## 元数据（必需）

```yaml
---
title: [文章标题]
author: [分析者]
status: 已分析
type: 爆款分析
tags:
  - 爆款分析
  - [主题分类1]
  - [主题分类2]
  - [平台名称]
created: [分析日期 YYYY-MM-DD]
source: [文章链接]
original_author: [原作者]
platform: [平台名称]
---
```

## 输出路径

默认路径由用户首次使用时配置，保存在 memory 中。建议路径：

默认在对话中返回 Markdown。用户要求保存文件时，先确认目标目录和文件名；不得在 Skill 中写死个人目录。

**开源用户**：需询问用户自定义路径

## 质量标准

- 实用性：提炼的要素要可复用
- 可复用性：分析的结论要可模仿
- 结构完整：必需部分不可少
- 简洁性：Be succinct, but to the point
