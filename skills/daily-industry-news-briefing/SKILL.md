---
name: daily-industry-news-briefing
description: >-
  Generate professional daily industry news briefings for the livestock, feed,
  and animal nutrition sector. This skill searches, aggregates, and synthesizes
  news from the past 24-48 hours across 7 core sections: (1) Policy and industry
  data from official sources like MARA, (2) Enterprise and industry chain
  dynamics, (3) Market trends and structural changes in farming, (4) Pet
  industry insights, (5) Domestic macroeconomic and business context, (6) Global
  agriculture and supply chain perspectives, and (7) Industry reference
  websites. Use this skill when users request daily news briefings, industry
  report generation, or ask for updates on livestock/feed/animal nutrition
  industry trends. The briefing maintains a professional, rational, and steady
  tone suitable for corporate management, sales teams, and R&D personnel.
---

# Daily Industry News Briefing

Generate professional daily news briefings for the livestock, feed, and animal nutrition industry.

## Quick Start

To create a briefing, execute the following steps in order:

1. **Search for latest information** - Use WebSearch to find news from the past 24-48 hours for each section
2. **Synthesize findings** - Organize information into the 7-section structure
3. **Generate briefing** - Create formatted Markdown output following the template

## Core Principles

- **Steady & Professional**: Avoid sensational language, exclamation marks, or exaggerated claims
- **Data-Driven**: Base analysis on facts and verifiable data
- **Multi-Angle Analysis**: Consider policy, market, technology, and operational perspectives
- **Long-Term Value**: Focus on structural trends, not short-term fluctuations

## Section Structure

Each briefing consists of 7 sections:

1. **Policy & Industry Data** - Official announcements from MARA, statistics, regulatory updates
2. **Enterprise & Chain Dynamics** - Corporate strategies, M&A, product launches, capacity changes
3. **Farming Market Trends** - Cost pressures, demand shifts, efficiency improvements
4. **Pet Industry Insights** - Cross-species nutrition trends, functional pet food developments
5. **Macroeconomic Context** - Commodity prices, economic policies affecting the industry
6. **Global Perspectives** - International trade, supply chain resilience, global trends
7. **Reference Sources** - Industry websites for fact-checking and deep research

## Search Strategy

For each section, execute 2-3 targeted searches using different keyword combinations. Prioritize:
- Official sources (government agencies, industry associations)
- Professional industry media over general news
- Recent publications (past 24-48 hours)
- Verifiable data and facts

See [search-strategy.md](references/search-strategy.md) for detailed keyword combinations and search workflows.

## Content Guidelines

Each news item must include:

**Factual Summary (2-3 sentences)**
- Objective description only
- Include time, entity, and key data/actions
- No subjective commentary

**Industry Significance (3 bullet points)**
- Logical analysis based on facts
- Multiple dimensions (policy, market, technology, operations)
- Forward-looking, medium to long-term perspective

For detailed writing standards, style guidelines, and quality checklists, see [content-guidelines.md](references/content-guidelines.md).

## Recommended Sources

Prioritize information from:
- **Official**: Ministry of Agriculture and Rural Affairs (MARA), National Bureau of Statistics
- **Industry Media**: 中畜网, 中国饲料行业信息网, 养猪信息网
- **Financial Media**: Caixin, Yicai, 21st Century Business Herald
- **International**: FeedStrategy, FeedNavigator, WattAgNet
- **Data Platforms**: Boyar, China Grain Information Network

For complete source list with usage recommendations, see [sources.md](references/sources.md).

## Template

Use the standardized template structure in [template.md](references/template.md) which includes:
- Header with date, coverage period, positioning
- 7 formatted sections with standard placeholders
- Management quick summary section
- Footer with generation timestamp

## Execution Workflow

```
1. Initialize briefing
   ├── Get current date
   └── Load template structure

2. For each section (1-6):
   ├── Execute searches using keywords from search-strategy.md
   ├── Filter and verify information (past 24-48h, authoritative sources)
   ├── Select 1-2 most relevant items
   └── Draft factual summary + industry significance

3. Section 7 (Reference Sources):
   └── List recommended websites from sources.md

4. Generate quick summary:
   ├── Synthesize 3-5 key takeaways across all sections
   └── Format for management rapid review

5. Final output:
   ├── Populate template with all sections
   ├── Add generation timestamp
   └── Review against quality checklist
```

## Quality Assurance

Before finalizing, verify:

- **Content Quality**: Each section has meaningful information with sources
- **Structure**: Follows template format exactly
- **Tone**: Professional, steady, rational (no sensational language)
- **Completeness**: Date, timestamp, and all sections present
- **Value**: Quick summary provides actionable insights for management

See [content-guidelines.md](references/content-guidelines.md) for complete self-checklist.

## When to Use This Skill

Trigger this skill when users ask for:
- "生成今日行业简报" (Generate today's industry briefing)
- "创建 Daily Industry News Briefing"
- "帮我整理畜牧/饲料行业新闻"
- "最新的行业动态"
- "养殖业政策更新"
- Any request for livestock/feed/animal nutrition industry news aggregation

## Key References by Context

- **Planning searches**: search-strategy.md
- **Writing content**: content-guidelines.md
- **Choosing sources**: sources.md
- **Formatting output**: template.md
