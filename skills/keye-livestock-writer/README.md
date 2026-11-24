# keye-livestock-writer

作者：科爷的数字生命 keyelifeai。版本：1.0.0。许可证：[MIT](LICENSE)。

为畜牧行业企业准备中文技术文章、证据景观、单项研究解读、改稿与证据审计包。覆盖猪、家禽、水产、反刍和其他养殖动物，支持饲料、添加剂、养殖、育种、设备和技术服务品牌。默认仅交付待审稿。

## 安装与要求

把本目录完整复制到 Agent 客户端支持的技能目录，不要只复制 SKILL.md。ZIP 解压后顶层目录是 `keye-livestock-writer/`。按客户端官方方式加载 [SKILL.md](SKILL.md)，支持技能引用的客户端可用 `$keye-livestock-writer` 调用。

脚本需要 Python 3.10+，只用标准库，无第三方运行依赖，不需要本机私有目录、Wiki、范文、账号或 API 密钥。研究需要 Agent 可用的资料阅读能力；网络搜索使用客户端已有工具，无网络时只研究用户已提供资料并说明缺口。未执行具体 Agent 客户端安装验证。

## 最短使用方式

告诉 Agent：

```text
使用 $keye-livestock-writer。
企业品牌名称：示例牧业
主营产品：饲料、养殖设备与技术服务
主题：奶牛热应激干预
读者：牧场技术负责人
请创建 evidence-landscape 待审写作包。
```

品牌定制只需前两项。文章主题、物种、阶段、读者属于每篇任务信息。品牌名和主营产品不是效果证据；产品资料是需要写具体产品主张时的可选补充。其他示例：蛋鸡饲养设备的技术解释、仔猪饲料研究解读、水产技术服务文章审计。无需修改技能本身。

## 脚本示例

以下假设当前目录是解压后的技能目录，输出目录设在其外部：

```sh
python3 scripts/setup_brand.py --brand-name '示例牧业' --main-products '饲料、养殖设备与技术服务' --workspace ../my-writing
python3 scripts/preflight.py --workspace ../my-writing
python3 scripts/init_article.py --workspace ../my-writing \
  --slug dairy-heat-stress --date 2026-11-24 \
  --title '奶牛热应激干预：哪些证据支持现场决策？' \
  --species 奶牛 --life-stage 泌乳期 --audience 牧场技术负责人 \
  --editorial-mode evidence-landscape
python3 scripts/audit_article.py \
  ../my-writing/articles/2026-11-24-dairy-heat-stress.md \
  ../my-writing/work/2026-11-24-dairy-heat-stress/evidence.md \
  --workspace ../my-writing
```

刚生成的空模板应审计失败。完成 brief、检索日志、证据矩阵、台账、提纲、正文与审核项说明后，将文章状态从 draft 改为 review 再审计。更换企业选新工作区；脚本拒绝覆盖已有配置或同名写作包。默认工作区为运行命令所在目录下的 `livestock-writing/`。

setup 写品牌配置和两个输出目录；init 写文章、六份 Markdown 过程文件和一份品牌配置快照。preflight 与 audit 只读。所有脚本均不联网、不上传资料、不读取凭据、不改系统配置。完整流程见 [workflow.md](references/workflow.md)。

## 审核边界

AUDIT PASS 只表示确定性的结构与边界检查通过，不验证文献内容、全部主张覆盖、科学真伪、版权或品牌批准。科学、法规、产品、品牌与发布仍需人工审核。该技能不执行发布、发帖、排期或知识库写入。

## 验证与维护

```sh
python3 -B scripts/test_skill.py
python3 -B scripts/trigger_eval.py
```

回归测试在临时目录创建虚构品牌和来源，不读取私有知识库；覆盖独立安装、品牌切换、特殊字符、覆盖拒绝、路径与审计边界。trigger_eval 是规则代理，不是实际模型的触发率测量。脚本测试不代表任何 Agent 客户端兼容性或科学写作质量已获验证。

分发时只打包本目录中的源码、参考规则、模板、评估样例与许可证，不包含工作区、品牌配置、真实文章、缓存或用户资料。保留作者署名与许可证；维护更改同步检查脚本、模板与引用，更新 metadata.version。
