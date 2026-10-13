---
title: 首页
---

# NJU CS · Serving Notes

南京大学计算机硕士阶段的个人学习与研究笔记，围绕 LLM 与多模态模型的推理、服务系统和实验方法持续更新。

这是个人学习仓库，与学校及文中开源项目的官方文档无隶属关系。正文以中文记录，文件和目录使用英文命名。

<div class="grid cards" markdown>

-   **学习路线**

    从推理瓶颈开始，连接调度、KV 管理和多模态 Serving。

    [查看阅读路线 →](../../index.md)

-   **论文精读**

    A–F 分组，分别记录原始笔记、答疑、研读队列。

    [进入论文目录 →](../../papers/index.md)

-   **系统实践**

    从源码结构到实验条件，把理解落到可测量的问题上。

    [查看 vLLM 笔记 →](../vllm-architecture.md)

-   **研究问题**

    记录候选假设、已有证据和下一步验证，持续修正判断。

    [查看问题清单 →](../research-questions.md)

</div>

## 当前进度

| 日期 | 已有产出 | 下一步 |
|---|---|---|
| 2026-10-13 | A1 高效推理综述笔记、22 条答疑、补充研读清单 | A2 Roofline；Orca → PagedAttention → Sarathi-Serve |

## 今天的阅读入口

- [A1 原始笔记](../../papers/a-inference-foundations/efficient-inference-survey/notes.md)
- [A1 逐问答疑与方向判断](../../papers/a-inference-foundations/efficient-inference-survey/answers.md)
- [A1 待研读论文与 Zotero 归档](../../papers/a-inference-foundations/efficient-inference-survey/reading-list.md)

## 如何使用

顶部导航切换主题，左侧选择文章，右侧目录跳转到具体问题。搜索支持中文和英文术语；深浅色模式可在页头切换。论文 PDF 与批注保存在 Zotero，站点保留学习笔记和官方来源链接。

后续新增课程、实验或项目时，遵循 [维护指南](../../../repository-guide.md)，不把运行日志、数据集和模型权重混入文档目录。
