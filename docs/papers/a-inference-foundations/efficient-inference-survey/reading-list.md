# A1 研读清单

这是从第一篇综述笔记中提取的后续阅读队列。加入队列不代表已经读完。

已核对并补齐 6 篇论文 PDF、4 个官方项目或文档条目；已有论文直接加入对应分类，没有重复下载。

| 笔记中的名称 | Zotero 分类 | 核对结果 |
| --- | --- | --- |
| [S³](https://arxiv.org/abs/2306.06000) · [打开 Zotero](zotero://select/library/items/NP7EGC8I) | B / Memory Management | 新增论文 + PDF |
| [PagedAttention / vLLM](http://arxiv.org/abs/2309.06180) · [打开 Zotero](zotero://select/library/items/ITLI9Q8Q) | B / Memory Management、Frameworks | 已有论文 + PDF |
| [LightLLM](https://github.com/ModelTC/lightllm) · [打开 Zotero](zotero://select/library/items/DMBZLK2J) | B / Memory Management、Batching、Frameworks | 新增官方项目 |
| [FlashInfer](https://arxiv.org/abs/2501.01005) · [打开 Zotero](zotero://select/library/items/6QXMYG3Z) | A；B / Memory Management | 新增论文 + PDF |
| [FlashInfer 文档](https://docs.flashinfer.ai/) · [打开 Zotero](zotero://select/library/items/46REJTA4) | B / Memory Management、Frameworks | 新增官方文档 |
| [Orca](https://www.usenix.org/conference/osdi22/presentation/yu) · [打开 Zotero](zotero://select/library/items/G29SWJ7U) | B / Batching | 已有论文 + PDF |
| [SARATHI](https://arxiv.org/abs/2308.16369) · [打开 Zotero](zotero://select/library/items/9K5FVMFW) | B / Batching | 新增论文 + PDF |
| [DeepSpeed-FastGen](https://arxiv.org/abs/2401.08671) · [打开 Zotero](zotero://select/library/items/KFA5F4GP) | B / Batching、Scheduling | 新增论文 + PDF |
| [Sarathi-Serve](https://arxiv.org/abs/2403.02310) · [打开 Zotero](zotero://select/library/items/9XGS64FF) | B / Batching | 已有论文 + PDF |
| [FastServe](https://arxiv.org/abs/2305.05920) · [打开 Zotero](zotero://select/library/items/ZJQFDKQ3) | B / Scheduling | 新增论文 + PDF |
| [VTC](https://arxiv.org/abs/2401.00588) · [打开 Zotero](zotero://select/library/items/GHLLL739) | B / Scheduling | 新增论文 + PDF |
| [DeepSpeed](https://github.com/deepspeedai/DeepSpeed) · [打开 Zotero](zotero://select/library/items/EA2TUMDM) | B / Frameworks | 新增官方项目 |
| [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) · [打开 Zotero](zotero://select/library/items/3J3VFAYB) | B / Frameworks | 新增官方项目 |

## 推荐阅读顺序

1. PagedAttention → Orca：先建立内存管理和迭代调度的基础。
2. SARATHI → Sarathi-Serve → DeepSpeed-FastGen：对照理解 chunked prefill、decode 优先和 Dynamic SplitFuse。
3. FastServe → VTC：分别看响应时间与多租户公平性目标。
4. S³ → FlashInfer：带着内存预测、分页布局和 kernel 执行问题阅读。
5. LightLLM、DeepSpeed、TensorRT-LLM：按论文对应机制查看源码，不必同时通读所有框架。

FastGen 和 FastServe 是不同工作；SARATHI 和 Sarathi-Serve 分别保留条目。LightLLM 等工程项目以官方仓库记录，避免误造“对应论文”。

[返回逐问答疑](answers.md) · [完整文献目录](../../../references/library.md)
