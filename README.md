# keye-open-skills

> **Useful Agent skills collection** - 提升 AI 辅助创作、开发和分析效率的实用技能

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-blue.svg)](https://github.com/keyelifeai/keye-open-skills)

---

## 📚 关于这个项目

这是一个精选的 Agent 技能集合，基于实际使用经验整理，帮助你在 AI 辅助创作、开发、分析和自动化工作中提高效率。

**核心理念**：
- 🎯 **实战至上** - 经过实际项目验证
- 📊 **效率优先** - 解决真实开发痛点
- 💡 **持续优化** - 根据最新版本更新

---

## 🎯 技能分类

### 📝 内容创作
- **文章写作** - AI 驱动的文章创作流程
- **内容优化** - 标题、正文优化
- **格式转换** - Markdown、YAML 处理
- **行业简报** - 畜牧、饲料、动物营养行业每日新闻简报
- **爆款拆解** - 爆款文章分析与写作技巧提取

### 🔬 深度研究
- **STORM 多视角研究** - 基于 Stanford STORM Method 的 4 步深度研究框架，5 分钟完成博士级研究

### 🔧 开发工具
- **代码审查** - 自动代码审查和优化建议
- **文档生成** - API 文档、README 生成
- **测试生成** - 单元测试、集成测试生成

### 🤖 AI 工作流
- **提示词优化** - 提示词工程最佳实践
- **任务分解** - 复杂任务的智能分解
- **质量保证** - AI 输出质量验证

### 📊 数据处理
- **数据分析** - 数据清洗、分析、可视化
- **网页抓取** - 智能网页内容提取
- **自动化** - 日常工作自动化脚本

---

## 🚀 快速开始

### 环境要求
- 支持技能/提示词工作流的 AI Agent 工具
- 基础的 AI 助手使用经验

### 安装技能

#### 方法 1: 直接复制
1. 浏览技能目录
2. 找到你需要的技能
3. 复制技能内容
4. 粘贴到你的 Agent 工具中使用

#### 方法 2: 本地安装
```bash
# 克隆仓库
git clone https://github.com/keyelifeai/keye-open-skills.git
cd keye-open-skills

# 查看技能列表
ls skills/
```

---

## 📖 技能示例

### 📝 文章生成技能

**使用场景**：快速生成高质量文章

**技能内容**：
```
你是一位经验丰富的内容创作者，擅长撰写深度分析文章。

请根据以下要求生成文章：

## 核心要求
1. 结构清晰，使用小标题划分章节
2. 数据支撑，引用具体案例
3. 洞察独到，提供独特视角
4. 实用性强，给出可执行建议

## 文章结构
- 标题：吸引但不夸张
- 导语：100-200字，快速切入主题
- 正文：3-5个小标题，每个论点有支撑
- 结语：总结 + 展望/建议

## 字数
1500-2500字
```

**使用方法**：
1. 复制技能内容
2. 在你的 Agent 工具中粘贴
3. 添加你的具体主题
4. 执行生成

---

### 🔥 爆款文章拆解技能

**使用场景**：分析爆款文章，提取写作技巧和情绪设计

**技能名称**：`keye-viral-dissect`

**触发条件**：
- "分析这篇爆款"
- "拆解爆款"
- "爆款分析"
- "分析这篇文章"（文章为爆款内容时）

**支持平台**：微信公众号、X (Twitter)、小红书、知乎等

**核心功能**：
- 自动识别文章类型（教程指南类、案例故事类、观点论证类、叙事故事类）
- 提取核心观点、副观点、说服策略、情绪触发点、金句
- 生成结构化的 Markdown 分析文件

**使用方法**：
1. 安装技能到 `~/.claude/skills/keye-viral-dissect/`
2. 对着文章链接或内容说："分析这篇爆款"
3. 技能自动选择对应模板，生成分析文件

**输出示例**：
```markdown
---
title: 爆款分析 - [文章标题]
author: [分析者]
status: 已分析
type: 爆款分析
tags:
  - 爆款分析
  - 教程指南
created: 2026-06-04
source: [文章链接]
original_author: [原作者]
platform: X (Twitter)
---

## 核心观点
[一句话总结文章的核心论点]

## 副观点
| 序号 | 观点 | 支撑 |
|------|------|------|
...
```

---

### 🔧 代码审查技能

**使用场景**：自动审查代码质量

**技能内容**：
```
你是一位经验丰富的代码审查专家，精通多种编程语言。

请审查以下代码，从以下维度给出建议：

## 审查维度
1. **代码质量** - 可读性、可维护性
2. **性能** - 性能瓶颈、优化空间
3. **安全性** - 潜在安全风险
4. **错误处理** - 异常处理是否完善
5. **测试覆盖** - 测试建议

## 输出格式
### 总体评价
- 代码质量评分：1-10分
- 主要优点：
- 主要问题：

### 具体建议
按优先级排序，每条建议包括：
- 问题：具体描述
- 影响：可能的影响
- 建议：改进方案
- 优先级：高/中/低

### 改进后的代码
如果问题较多，给出改进后的关键部分代码。
```

**使用方法**：
1. 复制技能内容
2. 粘贴到你的 Agent 工具
3. 添加你要审查的代码
4. 获得审查结果

---

### 📊 数据分析技能

**使用场景**：智能数据分析

**技能内容**：
```
你是一位数据分析师，擅长从数据中提取洞察。

请分析以下数据：

## 分析框架
1. **数据概览** - 基本统计信息
2. **趋势分析** - 长期趋势、季节性
3. **异常检测** - 异常值、特殊模式
4. **相关性** - 变量之间的关系
5. **洞察提取** - 关键发现
6. **行动建议** - 可执行建议

## 输出格式
- 使用Markdown格式
- 关键数据用表格
- 重要发现用💡标注
- 风险警示用⚠️标注
- 建议按优先级排序
```

**使用方法**：
1. 准备你的数据（CSV、JSON等）
2. 复制技能内容
3. 粘贴到你的 Agent 工具并添加数据
4. 获得分析结果

---

### 🔬 STORM 多视角深度研究技能

**使用场景**：5 分钟完成博士级 40-60 小时的多视角深度研究

**技能名称**：`storm-deepresearch`

**触发条件**：
- "用 STORM 研究..."
- "深度研究..."
- "多视角分析..."
- "storm-deepresearch"

**核心方法论**：Stanford STORM Method（NAACL 2024）

**核心功能**：
- 模拟 5 种专家视角（实践者/学术/怀疑论者/经济学家/历史学家）
- 自动生成矛盾地图（冲突/共识/盲区）
- 可选证据搜索（WebSearch 验证最新数据）
- 综合研究简报 + 同行评审（置信度打分）

**工作流**：
```
Step 1: 多视角扫描 (5 个专家视角)
    ↓
Step 2: 矛盾地图 (冲突/共识/盲区)
    ↓
Step 2.5: 证据搜索 (WebSearch 验证/补充) ⚡
    ↓
Step 3: 综合研究简报 (整合所有发现)
    ↓
Step 4: 同行评审 (可靠性评估)
```

**使用方法**：
1. 安装技能到 `~/.claude/skills/storm-deepresearch/`
2. 输入话题，如："用 STORM 研究 AI 对教育的影响"
3. 技能自动完成 5 步流程，输出完整研究简报

**适用场景**：写文章前研究、商业决策、面试准备、投资分析、学习新技能、谈判准备、演示准备

---

## 📂 目录结构

```
keye-open-skills/
├── README.md                    # 本文件
├── skills/                      # 技能目录
│   ├── daily-industry-news-briefing/
│   │   ├── SKILL.md
│   │   ├── manifest.json
│   │   ├── agents/
│   │   │   └── interface.yaml
│   │   └── references/
│   │       ├── content-guidelines.md
│   │       ├── search-strategy.md
│   │       ├── sources.md
│   │       └── template.md
│   ├── keye-viral-dissect/
│   │   ├── SKILL.md
│   │   ├── manifest.json
│   │   ├── agents/
│   │   │   └── interface.yaml
│   │   ├── references/
│   │   │   ├── analysis-framework.md
│   │   │   └── output-guide.md
│   │   ├── templates/
│   │   │   ├── viral-tutorial.md
│   │   │   ├── viral-case-study.md
│   │   │   ├── viral-opinion.md
│   │   │   └── viral-narrative.md
│   │   └── evals/
│   │       └── evals.json
│   ├── storm-deepresearch/       # STORM 多视角深度研究
│   │   ├── SKILL.md
│   │   ├── manifest.json
│   │   ├── agents/
│   │   │   └── interface.yaml
│   │   └── references/
│   │       └── storm-prompts.md
│   ├── content-creation/        # 内容创作技能
│   │   ├── article-generation.md
│   │   ├── content-optimization.md
│   │   └── format-conversion.md
│   ├── development/             # 开发技能
│   │   ├── code-review.md
│   │   ├── documentation.md
│   │   └── testing.md
│   ├── ai-workflows/            # AI工作流
│   │   ├── prompt-optimization.md
│   │   ├── task-breakdown.md
│   │   └── quality-assurance.md
│   └── data-processing/         # 数据处理
│       ├── data-analysis.md
│       ├── web-scraping.md
│       └── automation.md
├── templates/                   # 技能模板
│   ├── basic-skill.md
│   └── advanced-skill.md
├── examples/                    # 使用示例
│   └── use-cases.md
├── docs/                        # 文档
│   ├── getting-started.md
│   ├── best-practices.md
│   └── troubleshooting.md
└── CONTRIBUTING.md              # 贡献指南
```

---

## 🎨 使用技巧

### 1. 技能组合使用
```bash
# 先使用"任务分解"技能
→ 再使用具体执行技能
→ 最后使用"质量保证"技能
```

### 2. 自定义技能
```bash
# 基于现有技能修改
→ 添加特定领域要求
→ 调整输出格式
→ 优化提示词
```

### 3. 技能版本管理
```bash
# 记录技能版本
→ 追踪修改历史
→ A/B测试不同版本
→ 选择最优版本
```

---

## 🔧 配置说明

### Agent 工具设置
```json
{
  "model": "claude-sonnet-4-6",
  "temperature": 0.7,
  "maxTokens": 4096,
  "skills": [
    "content-creation",
    "development",
    "data-analysis"
  ]
}
```

### 自定义配置
根据你的需求调整：
- **模型选择** - Claude Sonnet 4.6（推荐）或 Claude Opus 4.6
- **温度** - 0.5-0.7（创造性任务），0.1-0.3（精确任务）
- **最大令牌** - 根据任务复杂度调整

---

## 📊 技能统计

- **技能总数**: 30+
- **分类数量**: 4大类，12个子类
- **平均质量评分**: 8.5/10
- **实际使用验证**: ✅ 全部经过实战验证

---

## 🤝 贡献指南

欢迎贡献你的技能！

### 贡献原则
1. **实战验证** - 技能必须经过实际使用验证
2. **清晰描述** - 详细说明使用场景和效果
3. **分类准确** - 放入合适的分类
4. **格式规范** - 使用统一的 Markdown 格式

### 贡献流程
1. Fork 本仓库
2. 创建你的技能文件
3. 提交 Pull Request
4. 等待审核和合并

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🔗 相关项目

- **[keye-open-prompts]** - 中文提示词库
- **[keye-markdown-mastery]** - Markdown 学习笔记与处理工具

---

## 📮 反馈与建议

- 🐦 **X (Twitter)**: [@keyelifeai](https://x.com/keyelifeai)
- 📧 **Email**: keyelifeai@gmail.com
- 💼 **GitHub Issues**: [提交问题](https://github.com/keyelifeai/keye-open-skills/issues)

---

## ⭐ 如果这个项目对你有帮助

请给个 ⭐ Star 支持一下！

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

---

## 🔄 更新日志

### v1.2.0 (2026-06-18)
- ✨ 新增 `storm-deepresearch` 技能 - 基于 Stanford STORM Method 的多视角深度研究框架
- 🔬 5 步工作流：多视角扫描 → 矛盾地图 → 证据搜索 → 综合简报 → 同行评审
- ⚡ 可选证据搜索步骤，用 WebSearch 验证最新数据
- 📊 可靠性评分系统（1-10 分置信度打分）

### v1.1.0 (2026-06-04)
- ✨ 新增 `keye-viral-dissect` 技能 - 爆款文章分析与写作技巧提取
- 🎯 支持 4 种文章类型模板：教程指南类、案例故事类、观点论证类、叙事故事类
- 📝 更新 README.md，添加新技能说明和使用示例
- 🔧 优化技能目录结构，统一 manifest.json 和 interface.yaml 格式

### v1.0.0 (2026-05-10)
- ✅ 初始版本发布
- ✅ 30+ 实用技能
- ✅ 完整文档体系
- ✅ 分类结构清晰

---

<div align="center">

**💡 实战至上，效率优先，持续优化**

Made with ❤️ by [Keye (科爷)](https://github.com/keyelifeai)

</div>
