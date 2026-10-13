# 文档维护

## 同一份文档，两个入口

```text
Research/
  vault/             Obsidian 打开的目录
    index.md         学习路线
    papers/          论文原始笔记、答疑和研读清单
    notes/           原有学习笔记，不生成网页
    images/          配图
    .obsidian/       本地设置，不提交 Git
  docs -> vault      MkDocs 的文档入口
  mkdocs.yml         网站配置
  scripts/           文档检查脚本
  bibliography/      书目数据
```

在 Obsidian 中选择“打开本地仓库”，打开 `vault`。不要把整个 `Research` 当作文档库。文件只保存一份，软链接无需同步或复制。

网站导航包括学习路线和论文精读；模板和暂缓的实践计划放在论文精读栏目。只在有实际笔记时把对应分组加入 `mkdocs.yml` 的 `nav`。`notes/` 通过 `exclude_docs` 排除，网页和搜索均不包含它；该目录仍在公开 Git 仓库中。

## 写笔记和插图

每篇论文使用一个文件：`papers/<分组>/<序号>-<简称>.md`。A1 的原始笔记和答疑沿用现有路径。可复制 [精读模板](vault/papers/template.md)。文件名用小写英文和连字符，正文继续用中文。

Obsidian 新附件写入 `images/`。图片采用标准 Markdown 相对链接，Obsidian 和 MkDocs 都可读取。已有图片链接已随迁移更新。

## 构建

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
python scripts/check_docs.py
mkdocs build --strict
mkdocs serve
```

检查脚本会验证软链接、正文链接，以及文档库中是否混入脚本或配置。GitHub Actions 在 Linux 上检出同一个相对软链接并构建。

推送到 `main` 自动发布；拉取请求只检查构建。在线网页不会因为本地编辑而直接更新。

## 原笔记位置

| 旧笔记 | 现在的位置 |
| --- | --- |
| 学习总路线 | [学习路线](vault/index.md) |
| vllm | [vLLM 架构笔记](vault/notes/vllm-architecture.md) |
| LLM Serving System | [Serving 系统地图](vault/notes/serving-system-map.md) |
| A 组第一篇综述 | [原始精读笔记](vault/papers/a-inference-foundations/efficient-inference-survey/notes.md) |

## 分组与阅读状态

| 分组 | 新笔记目录 |
| --- | --- |
| A - Inference Foundations | `papers/a-inference-foundations/` |
| B - Batching and Serving Basics | `papers/b-batching-and-serving-basics/` |
| C - Text LLM Scheduling | `papers/c-text-llm-scheduling/` |
| D - Multimodal Models | `papers/d-multimodal-models/` |
| E - Visual Token Adaptation | `papers/e-visual-token-adaptation/` |
| F - Multimodal Serving | `papers/f-multimodal-serving/` |

例如 `papers/c-text-llm-scheduling/09-learning-to-rank.md`。尚未写笔记时，首页的笔记栏显示“暂无”，导航不显示空分组。状态使用“未读”“在读”“已读”。

Zotero 中 A1 使用 `order:00`、`status:done`；01 至 19 使用对应 `order:*` 和 `status:todo`，主线标 `read:deep`。G 为 `read:skim`；Inbox 存放待归类的新论文。

A1 研读清单与框架资料是隐藏参考页：通过 `not_in_nav` 和 `search.exclude` 隐藏，保留旧链接。不要修改 A1 原始笔记和逐问答疑来迁就目录调整。
