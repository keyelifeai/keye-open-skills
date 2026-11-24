# 写作工作流

所有命令中的 `<skill-dir>` 替换为当前技能安装目录。在当前目录执行命令时，默认工作区为 `livestock-writing/`。如需改址，给 setup、preflight、init 和 audit 一律添加相同的 `--workspace <output-dir>`。工作区不得放在技能安装目录内。

## 配置和创建

首次配置只需企业品牌名称和主营产品，不需要内部知识库或参考文件：

```sh
python3 <skill-dir>/scripts/setup_brand.py --brand-name '示例牧业' --main-products '饲料、养殖设备与技术服务'
python3 <skill-dir>/scripts/preflight.py
python3 <skill-dir>/scripts/init_article.py \
  --slug dairy-heat-stress \
  --title '奶牛热应激干预：哪些证据支持现场决策？' \
  --species 奶牛 --life-stage 泌乳期 --audience 牧场技术负责人 \
  --editorial-mode evidence-landscape
```

品牌名称和主营产品来自用户，不根据品牌名猜测公司资质或产品性能。默认产品连接为 none；有明确公司观点需求时可选择 company-perspective。产品专属主张另需产品说明或研究来源，不是初始化的前提。

setup 创建 `brand.json`、`work/`、`articles/`。它拒绝覆盖已有配置。已有企业继续用该工作区；更换企业使用新工作区。preflight 只读检查包文件、配置结构与输出边界，不核实品牌事实，不访问其他本地目录。

每次 init 创建：

```text
<workspace>/
├── brand.json
├── articles/YYYY-MM-DD-<slug>.md
└── work/YYYY-MM-DD-<slug>/
    ├── brand.json
    ├── brief.md
    ├── search-log.md
    ├── evidence-matrix.md
    ├── evidence.md
    ├── outline.md
    └── review.md
```

每次任务快照保留当时品牌配置。init 拒绝覆盖、路径穿越和软连接输出，写入失败时清理本次已创建文件。默认日期取执行环境的本地日期；需要特定业务日期时传 `--date YYYY-MM-DD`。

## 定义读者决策

先完成 brief 的 Primary reader、Decision、Why now、What could change their view、Target-market relevance，固定物种、阶段、范围、核心判断和产品连接状态。目标市场默认中国，可改为其他国家或地区，法规与适用条件随之调整。

## 检索和提取

1. 在日志中记录研究问题、日期范围、来源范围、查询式、纳排标准、每轮结果、无法访问的来源及限制。
2. 优先原始论文、正式综述、法规、标准和权威机构页面。只记录真实访问和核验过的内容。研究时使用当前可用工具，无需指定的 API、账号或私有目录。
3. 用户主动提供的文件可只读参考，不扫描用户目录。引用写成 `path/to/document.md#章节或页码`，相对路径按工作区解析；也可使用用户提供文件的实际绝对路径。路径只属于用户输出，不能回填到开源技能包中。
4. 矩阵逐项记录物种、阶段、日粮或生产背景、干预、对照、剂量、持续时间、实验单位、样本量、结局、不确定性、局限、利益冲突、更正或撤稿检查和目标市场适用性。设备、育种或服务主题使用相应性能与生产指标，不强套营养剂量；不适用字段写明原因。
5. 每个实质主张进入七列台账，关联矩阵 Evidence ID。区分直接证据与推断。用户风格范文不得作为事实来源。
6. 主动寻找反证，说明未找到的范围和限制。关键论文检查出版方页面；有 DOI 时可核对更新元数据。记录日期，不把未发现撤稿写成保证。

## 综合和起草

分别判断 Research activity、Evidence strength、Technology maturity、Commercial availability、Field adoption，五者不能互相替代。解释共识、冲突和可能原因，避免逐篇摘要。跨物种结果须记录来源物种、用途和外推边界。

前两种模式读取 `evidence-landscape.md`。常规编辑研究可在记录 editorial saturation 依据后停止，不声称检索穷尽。选一种提纲起草。公司观点使用当前品牌名称，产品段不是必选项。原料类别或技术路线证据不能直接证明具体产品性能。

## 审计和交付

文章使用 `workflow_version: "public-1"`，从 draft 开始。完成所有研究与写作文件、清除未解决占位符后改为 review。人工审核清单可以保留未完成项，并写明负责人或缺口；不得把尚未完成的人工审核勾成通过。final 仅供人工审核后的内部状态，不代表已发布。

```sh
python3 <skill-dir>/scripts/audit_article.py \
  <workspace>/articles/YYYY-MM-DD-<slug>.md \
  <workspace>/work/YYYY-MM-DD-<slug>/evidence.md
```

frontmatter 使用顶层单行标量；含特殊符号的字符串使用 JSON 双引号格式。表格单元格不要直接放管道符，可写成 HTML 实体。台账 `Source class` 为 user_document 或 external_url；所有来源保持 review-required，审计前删除 do-not-use 行和相应主张。

AUDIT PASS 只检查结构、路径绑定、品牌快照、未解决占位符、台账格式和部分来源边界，不联网验证引用，不检查全部主张是否遗漏，不确认科学真伪、版权或品牌批准，也不证明 brief、矩阵和日志的研究质量。

交付文章、七个过程文件与尚待人工审核的科学、法规、产品、品牌和发布事项。不得发布、排期或写入知识库。
