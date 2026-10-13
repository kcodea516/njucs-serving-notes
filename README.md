# NJU CS Serving Notes

[文档网站](https://kcodea516.github.io/njucs-serving-notes/)只记录学习路线和论文精读。

## 在 Obsidian 中编辑

打开 `vault` 文件夹作为文档库。这里保存 Markdown 和图片；脚本、构建配置在库外。`docs` 是指向 `vault` 的相对软链接，两边读取同一份文件。

- [学习路线](vault/index.md)
- [论文笔记](vault/papers/index.md)
- [原有学习笔记](vault/notes/index.md)
- 图片目录：`vault/images/`

`vault/notes/` 保存原有 vLLM、系统地图和研究构想等学习记录，不生成网页，也不进入网站搜索。它仍随仓库保存，不是私密目录。

## 预览与发布

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
python scripts/check_docs.py
mkdocs serve
```

推送到 `main` 后自动构建并发布。修改文件会立即反映在 Obsidian 和本地预览中；公开网站在推送部署后更新。

详细维护方式见 [repository-guide.md](repository-guide.md)。
