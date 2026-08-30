# 贡献指南

本仓库只接收 Brand 5.0 Lab by Keye 已明确维护的 Agent Skill 源码，以及对现有 3 个 Skill 的修正。

## 修正现有 Skill

1. 从 `main` 创建 feature branch。
2. 保持 Skill 的目录名与 `SKILL.md` 中的 `name` 一致。
3. 只在 `SKILL.md` 维护便携字段：`name`、`description`、`license`、`compatibility`、`metadata` 和实验性的 `allowed-tools`。
4. 新增脚本时写清环境、输入、输出和系统影响，不得硬编码密钥或个人绝对路径。
5. 运行 `./script/validate`。
6. 通过 Pull Request 提交，并说明来源、权利、许可证、修改范围和风险变化。

## 提交新 Skill

外部 Skill 不能直接通过源码 PR 进入本仓库。请先创建 Adoption Request，说明：

- 原作者和权威上游；
- Keye 可以发布、修改并持续维护该 Skill 的权利证据；
- SPDX 许可证、完整许可证文本、归属、NOTICE 和修改记录；
- 网络、认证、浏览器自动化、外部写入和系统影响；
- 为什么由 Brand 5.0 Lab 接管维护，而不只是链接原始上游。

只有 Keye 明确接受维护责任后，源码 PR 才进入 Open-source Review。未接管的第三方 Skill 只可能由技能目录链接其原始上游，本仓库不会复制源码。

## 发布门禁

- Agent Skills 官方格式校验通过。
- Skill 名称和目录唯一。
- 引用文件、依赖路径和许可证证据存在。
- 无个人绝对路径、疑似 secret、虚构数量、评分或效果承诺。
- Python 等自带脚本通过静态语法检查和已有单元测试。
- 每个 Skill 有独立语义版本。
- Release Snapshot 固定到公开 commit 或 tag。

仓库验证不执行 Skill、第三方安装命令或 Agent 客户端冒烟测试。没有明确的客户端、版本、操作系统、安装方式和日期时，不得声称兼容性已验证。

## 许可证

Keye 原创贡献按仓库 [MIT License](LICENSE) 发布。接管或衍生内容必须保留适用的 License Exception，不得把 GPL 或许可证不明的内容自动改为 MIT。
