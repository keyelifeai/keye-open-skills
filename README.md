# keye-open-skills

Brand 5.0 Lab by Keye 维护的 Agent Skills 公共源码仓库。当前公开 tree 只包含 3 个由 Keye 创建并维护的 Skill，不收录第三方 Skill 副本。

## 当前 Skill

| Skill | 版本 | 用途 | 主要要求 |
| --- | --- | --- | --- |
| `keye-network-optimizer` | `1.0.0` | 以可回滚方式诊断 macOS 网络、DNS、代理和 VPN/TUN 路径 | macOS、Python 3；系统变更前需用户批准 |
| `keye-viral-dissect` | `2.1.0` | 拆解文章结构、论证方式与情绪设计 | 文本输入；URL 输入另需网络访问与 `web-access` Skill |
| `storm-deepresearch` | `1.2.0` | 用多视角、矛盾图和证据复核组织研究简报 | 文本输入；证据搜索需要网络和搜索能力 |

各 Skill 的版本独立维护。仓库 Release 只用于记录一次可复现的 Release Snapshot，不替代单个 Skill 版本。

## 安装

优先使用 Agent 客户端提供的原生 Skill 添加入口。手工安装时，从固定 release 或 commit 下载目标 Skill 的完整目录，并按客户端文档放入其 Skill 目录。不要只复制 `SKILL.md`，因为脚本、参考资料和模板可能是 Skill 的一部分。

下面的快捷命令采用 `vercel-labs/skills` 当前公开的 `add` 与 `--skill` 语法。仓库校验不会执行安装命令，也不代表任何客户端已通过运行测试。

```bash
npx skills add keyelifeai/keye-open-skills --skill keye-network-optimizer
npx skills add keyelifeai/keye-open-skills --skill keye-viral-dissect
npx skills add keyelifeai/keye-open-skills --skill storm-deepresearch
```

根据来源生成，未安装验证。

## 许可证与来源

仓库中的 Keye 原创内容使用 [MIT License](LICENSE)。第三方方法、项目和许可证说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。方法归属不表示第三方组织维护或认可本仓库中的 Skill。

两个无法确认原始创作来源的旧式提示词已从当前 tree 撤下：

- `skills/content-creation/article-generation.md`
- `skills/development/code-review.md`

文件仍保留在 Git 历史中，但在来源证据解决前不会转换、发布或收录。

## 验证

本仓库用 Agent Skills 官方 `skills-ref` 校验标准 frontmatter，再运行仓库专用的唯一性、引用文件、许可证、个人路径、疑似 secret、Python 语法和失实声明检查。

```bash
./script/validate
```

验证只检查格式与静态内容，不执行 Skill、安装器、网络请求或客户端冒烟测试。

## 贡献

提交修正前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。外部 Skill 需要先通过 Adoption Request 由 Keye 明确接管维护，不能把普通 listing request 直接作为源码 PR。
