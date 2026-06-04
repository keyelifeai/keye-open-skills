---
name: keye-viral-dissect
description: 分析微信公众号、X、小红书等平台的爆款文章，提取写作技巧和情绪设计。当用户说"分析这篇爆款"、"拆解爆款"、"爆款分析"、"分析这篇文章"时触发。只做分析，不包括生成新文章。
# EXTENDED METADATA
version: 2.0.0
created_at: 2026-06-04T00:00:00Z
entry_point: SKILL.md
dependencies: [web-access]
---

# 爆款文章拆解 Skill

## 触发条件

- "分析这篇爆款"
- "拆解爆款"
- "爆款分析"
- "分析这篇文章"（文章为爆款内容时）
- 用户提供文章链接/内容/PDF并要求分析

## 适用平台

微信公众号、X (Twitter)、小红书、知乎及其他内容平台

## 核心流程

1. **获取内容**：链接调用/web-access，粘贴内容直接处理，PDF解析后处理
2. **识别类型**：教程指南类、案例故事类、观点论证类、叙事故事类
3. **选择模板**：根据文章类型选用对应模板（见 templates/）
4. **执行分析**：按照模板结构提取核心观点、副观点、说服策略、情绪触发点、金句等
5. **生成输出**：添加YAML元数据，保存到配置路径

## 输出配置

首次使用时询问保存路径，后续自动使用记忆中的路径。默认建议：
`/Users/kevinzheng/Library/Mobile Documents/iCloud~md~obsidian/Documents/SyncVault/Business_ContentCreator/01-灵感与素材库/爆款分析`

## 边界

- **包含**：文章结构分析、写作技巧提取、情绪设计拆解
- **不包含**：生成新文章、重写内容、创意延展

## 文件

- [分析框架](references/analysis-framework.md) - 必需/可选分析项说明
- [输出规范](references/output-guide.md) - 文件命名和元数据格式
- [模板目录](templates/) - 4种文章类型标准模板
