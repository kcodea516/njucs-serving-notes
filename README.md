# NJU CS Serving Notes

个人硕士阶段学习与研究笔记，关注 LLM 和多模态模型的高效推理与 Serving 系统。使用英文路径、中文正文，并通过 MkDocs Material 生成可搜索的文档站。

- 文档站：<https://kcodea516.github.io/njucs-serving-notes/>
- [学习路线](docs/roadmap/reading-roadmap.md)
- [论文精读](docs/papers/index.md)
- [第一篇综述的逐问答疑](docs/papers/a-inference-foundations/efficient-inference-survey/answers.md)
- [研究问题](docs/research/questions.md)

本仓库为个人学习记录，不代表南京大学或所引用项目的官方立场。已读笔记、历史构想和未验证假设分别标注；目前尚未报告实验结果。

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-docs.txt
python scripts/check_docs.py
python -m mkdocs serve
```

## Structure

| Path | Content |
|---|---|
| `docs/roadmap/` | Reading roadmap |
| `docs/foundations/` | Concepts and system maps |
| `docs/papers/` | Paper notes organized into groups A–F |
| `docs/practice/` | Framework and implementation notes |
| `docs/research/` | Questions, hypotheses, and historical drafts |
| `docs/references/` | Bibliography and Zotero inventory |
| `docs/templates/` | Paper and experiment templates |
| `experiments/` | Reproducible code and configuration |
| `scripts/` | Documentation maintenance |

Pushes to `main` run a strict build and publish GitHub Pages. Pull requests run the same checks without deploying. See [维护指南](docs/maintenance.md) for adding notes and configuring the first deployment.

PDFs and annotations are managed in Zotero. Private editor state, datasets, model weights, and generated files are excluded from Git. Third-party diagrams remain attributed to their original sources; no blanket license is assigned to them by this repository.
