# 仓库维护

## 目录约定

```text
docs/
  roadmap/       学习路线
  foundations/   概念和系统地图
  papers/        A–F 论文分组及逐篇笔记
  practice/      框架源码与实践笔记
  research/      候选问题、假设与历史构想
  references/    文献索引及归档信息
  templates/     论文、实验模板
  assets/        图片与站点样式
experiments/     实验代码与配置
scripts/         文档检查等维护脚本
```

新文件使用小写英文与连字符，例如 `kv-cache-management.md`。正文可以继续用中文。每篇论文独立建目录：自己的记录写在 `notes.md`，答疑写在 `answers.md`，后续论文写在 `reading-list.md`。

## 本地编辑与预览

使用 Python 3.12，首次运行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

浏览器访问命令输出的本地地址。修改 Markdown 后，页面自动刷新。

新增页面后，在 `mkdocs.yml` 的 `nav` 中加入导航。图片使用相对 Markdown 链接，例如 `![示意图](../../assets/images/example.png)`；这样 GitHub、Obsidian 和站点都能读取。

## 发布与检查

```bash
python scripts/check_docs.py
python -m mkdocs build --strict
```

推送到 `main` 后，GitHub Actions 构建文档并发布 GitHub Pages。首次发布需在仓库 `Settings → Pages → Source` 中选 `GitHub Actions`。拉取请求仅构建检查，不执行公开部署。

## 文献与实验材料

Zotero 的 `Research/Serving` 保存文献与 PDF，A–F 分类和 B 组的主题子分类供检索。一个 Zotero 条目可以属于多个分类，无需复制 PDF。

原始实验数据、模型权重、运行日志和本地编辑器配置不纳入 Git。实验说明和可复现配置放入 `experiments/`，公开结果解释放在 `docs/practice/`。个人访问密钥不得写入文档或提交历史。

## 内容状态

原始笔记、答疑和研究假设分别标注。历史稿保留当时的表达，不能因为归档到网页就自动视为已核实的结论。引用第三方图片和论文时注明来源；本站不重新打包分发论文全文。
