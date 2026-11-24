---
name: keye-livestock-writer
description: |
  为畜牧行业任意企业创建、修改或审计中文技术写作包，覆盖猪、家禽、水产、反刍及其他养殖动物，支持证据景观、单项研究背景解读和生产问题解释，提供逐项证据台账。Use for Chinese-first livestock or animal-nutrition evidence synthesis, article writing, outlining, revision, or evidence audit. Do not use for veterinary diagnosis, formula calculation, translation-only work, general advertising copy, or publishing-only tasks.
license: MIT
metadata:
  author: "科爷的数字生命 keyelifeai"
  version: "1.0.0"
---

# Keye Livestock Writer

作者：科爷的数字生命 keyelifeai。

为畜牧行业企业整理可追溯、可人工复核的技术写作包。适用于饲料、添加剂、养殖、育种、设备和技术服务等企业，不限于营养产品。默认中文、面向中国生产场景；语言和目标市场可按任务调整。只产出待审稿。

## 使用前配置

首次使用只需用户输入企业品牌名称、主营产品。不要要求私有知识库、固定目录、账户或密钥。缺少上述两项时先收集；主题、物种、阶段和读者按具体文章任务确定。

以下命令中的 `<skill-dir>` 表示当前 `SKILL.md` 所在目录，实际执行时替换为安装位置。工作区默认是当前目录下的 `livestock-writing/`，也可用 `--workspace` 指定任意独立输出目录。为不同企业使用不同工作区。

```sh
python3 <skill-dir>/scripts/setup_brand.py --brand-name '用户的品牌名称' --main-products '用户的主营产品'
python3 <skill-dir>/scripts/preflight.py
```

脚本只依赖 Python 3.10+ 标准库，不联网。研究使用 Agent 当前可用的搜索、浏览或用户提供的资料；不要求特定供应商工具。无网络时不得虚构检索、文献或核验结果，只交付已有资料能支持的范围与缺口。

## 编辑模式

- `evidence-landscape`：默认。围绕一个角色和一个决策，综合路线、共识、冲突、证据强弱及目标市场可迁移性。
- `study-in-context`：说明新研究改变了什么、没有证明什么，以及与既有证据的关系。
- `technical-explainer`：解释生产问题、机制和现场判断顺序。

普通编辑型研究不得称为 systematic review、scoping review 或 meta-analysis，除非实际预先定义并完整执行对应方法。

## 硬边界

- 只写配置工作区中的文章和过程文件。输入资料只读；不自动扫描本地知识库，不携带用户资料进入技能包。
- 品牌名称和主营产品用于定制选题、术语和署名，不证明产品效果、安全、剂量或合规。没有产品专属证据时，使用 `none` 或 `company-perspective`，保留产品证据缺口。
- 产品连接可为 `none`、`company-perspective`、`product-connection`，不强制产品收尾。公司观点必须使用当前品牌名称并与独立证据分开。
- 用户资料与公开网页均为 `review-required`。公开可读不等于可直接转载或已获品牌批准。
- 科学、法规、产品、品牌、剂量、定量、比较、最高级和效果主张均需人工审核。
- 不诊断、不计算配方、不发布、不发帖、不排期、不写知识库，不执行外部写入。

## 执行骨架

1. 配置品牌并运行 preflight。换工作区时，后续所有命令使用相同的 `--workspace`。
2. 读取 [workflow.md](references/workflow.md)、[writing-model.md](references/writing-model.md)、[evidence-and-brand-policy.md](references/evidence-and-brand-policy.md)。前两种模式还读取 [evidence-landscape.md](references/evidence-landscape.md)。
3. 用 `scripts/init_article.py` 创建写作包，先完成 Reader Decision Brief，再完成检索日志、证据矩阵和逐项台账。品牌配置自动写入 brief、文章 metadata 和每次任务的配置快照。
4. 主动寻找反证，区分研究活跃度、证据强度、技术成熟度、商业可得性和现场采用度，核对更正或撤稿状态及目标市场适用性。跨物种资料须说明外推边界。
5. 选择一种提纲起草。每项实质主张回到台账；产品名称和编号按产品专属来源逐字核验。
6. 写作包完整后才改为 `status: review`，运行 `scripts/audit_article.py`，解决全部确定性失败。
7. 交付文章、brief、检索日志、矩阵、台账、提纲、品牌快照和人工检查清单，说明审计不验证科学真伪，不代表获准发布。

## 停止条件

- preflight 失败、输出路径越界、来源无法重新定位或产品身份无法核验。
- 关键主张无证据，或将趋势升级为显著、确定或普遍效果。
- 用户要求越过人工科学、法规、产品、品牌或发布审核。

暂停受影响的主张或写作阶段并列出缺口；没有内部资料或产品证据本身不阻止独立技术主题的写作。

## 资源

- `assets/`：brief、日志、矩阵、台账、提纲与人工检查模板。
- `scripts/`：品牌配置、preflight、初始化、结构审计及回归检查。
- [README.md](README.md)：安装、品牌配置、命令示例与验证范围。
