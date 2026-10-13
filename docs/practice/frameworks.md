# 框架官方资料

这些条目是软件项目和文档，不统一当作学术论文。

| 项目 | 官方入口 | 当前阅读任务 |
|---|---|---|
| vLLM | [文档](https://docs.vllm.ai/en/latest/) · [仓库](https://github.com/vllm-project/vllm) | 主实践框架；请求、scheduler、KV manager、执行路径 |
| DeepSpeed | [仓库](https://github.com/deepspeedai/DeepSpeed) · [FastGen 论文](https://arxiv.org/abs/2401.08671) | 区分训练组件、推理组件与 Serving 方案 |
| LightLLM | [仓库](https://github.com/ModelTC/lightllm) | 对照内存管理及 batching 实现 |
| TensorRT-LLM | [仓库](https://github.com/NVIDIA/TensorRT-LLM) | 了解 NVIDIA 推理运行时与优化选项 |
| FlashInfer | [文档](https://docs.flashinfer.ai/) · [论文](https://arxiv.org/abs/2501.01005) | attention backend 与 KV 布局 |

读取源码或对比性能时，填写实际版本或 commit。上游 `main` 和 `latest` 的内容会变化，链接不代表实验固定版本。
