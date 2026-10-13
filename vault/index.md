---
aliases:
- 学习总路线
---

# 学习路线

## 研究方向

研究主线是多模态 serving 的调度，包含 batching 策略。当前关注视觉编码器不能直接照搬因果 prefill 分块机制带来的调度约束、多模态请求的成本模型、混合负载下的 SLO 冲突，以及负载自适应的视觉 token 预算。通过 profiling 和相关工作对照确认瓶颈，再选择可验证的调度问题。

## 主线论文（20 篇）

按序号阅读；A1 已完成，其余目前为未读。笔记完成后更新状态和链接。简称旁的 Zotero 链接用于打开本地条目。

### A · 推理基础

| 序号 | 简称 | 标题 | PDF 链接 | 状态 | 笔记链接 |
| --- | --- | --- | --- | --- | --- |
| A1 | Efficient Inference Survey · [Zotero](zotero://select/library/items/BXYPLGW7) | A Survey on Efficient Inference for Large Language Models | [PDF](https://arxiv.org/pdf/2404.14294) | 已读 | [原始笔记](papers/a-inference-foundations/efficient-inference-survey/notes.md) · [逐问答疑](papers/a-inference-foundations/efficient-inference-survey/answers.md) |
| 01 | Roofline · [Zotero](zotero://select/library/items/39NN3CGB) | LLM Inference Unveiled: Survey and Roofline Model Insights | [PDF](https://arxiv.org/pdf/2402.16363) | 未读 | 暂无 |

### B · 批处理与服务系统基础

| 序号 | 简称 | 标题 | PDF 链接 | 状态 | 笔记链接 |
| --- | --- | --- | --- | --- | --- |
| 02 | Orca · [Zotero](zotero://select/library/items/G29SWJ7U) | Orca: A Distributed Serving System for Transformer-Based Generative Models | [PDF](https://www.usenix.org/system/files/osdi22-yu.pdf) | 未读 | 暂无 |
| 03 | vLLM · [Zotero](zotero://select/library/items/ITLI9Q8Q) | Efficient Memory Management for Large Language Model Serving with PagedAttention | [PDF](https://arxiv.org/pdf/2309.06180) | 未读 | 暂无 |
| 04 | Sarathi-Serve · [Zotero](zotero://select/library/items/9XGS64FF) | Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve | [PDF](https://arxiv.org/pdf/2403.02310) | 未读 | 暂无 |
| 05 | DeepSpeed-FastGen · [Zotero](zotero://select/library/items/KFA5F4GP) | DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference | [PDF](https://arxiv.org/pdf/2401.08671) | 未读 | 暂无 |
| 06 | DistServe · [Zotero](zotero://select/library/items/9UQJ79PH) | DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving | [PDF](https://arxiv.org/pdf/2401.09670) | 未读 | 暂无 |

### C · 文本 LLM 调度

| 序号 | 简称 | 标题 | PDF 链接 | 状态 | 笔记链接 |
| --- | --- | --- | --- | --- | --- |
| 07 | FastServe · [Zotero](zotero://select/library/items/ZJQFDKQ3) | Fast Distributed Inference Serving for Large Language Models | [PDF](https://arxiv.org/pdf/2305.05920) | 未读 | 暂无 |
| 08 | VTC · [Zotero](zotero://select/library/items/GHLLL739) | Fairness in Serving Large Language Models | [PDF](https://arxiv.org/pdf/2401.00588) | 未读 | 暂无 |
| 09 | Learning to Rank · [Zotero](zotero://select/library/items/9ADQLTAS) | Efficient LLM Scheduling by Learning to Rank | [PDF](https://arxiv.org/pdf/2408.15792) | 未读 | 暂无 |
| 10 | Llumnix · [Zotero](zotero://select/library/items/HNRQCHYG) | Llumnix: Dynamic Scheduling for Large Language Model Serving | [PDF](https://arxiv.org/pdf/2406.03243) | 未读 | 暂无 |

### D · 多模态模型

| 序号 | 简称 | 标题 | PDF 链接 | 状态 | 笔记链接 |
| --- | --- | --- | --- | --- | --- |
| 11 | Qwen2-VL · [Zotero](zotero://select/library/items/HHW8ELR3) | Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution | [PDF](https://arxiv.org/pdf/2409.12191) | 未读 | 暂无 |

### E · 视觉 Token 自适应

| 序号 | 简称 | 标题 | PDF 链接 | 状态 | 笔记链接 |
| --- | --- | --- | --- | --- | --- |
| 12 | FastV · [Zotero](zotero://select/library/items/9NRLNFI3) | An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models | [PDF](https://arxiv.org/pdf/2403.06764) | 未读 | 暂无 |
| 13 | TopV · [Zotero](zotero://select/library/items/SYPZFF3X) | TopV: Compatible Token Pruning with Inference Time Optimization for Fast and Low-Memory Multimodal Vision Language Model | [PDF](https://arxiv.org/pdf/2503.18278) | 未读 | 暂无 |
| 19 | SmartVL · [Zotero](zotero://select/library/items/DK3VFCBT) | Look Less, Think Faster: Joint Token-Compute Adaptation for Multimodal LLMs | [PDF](https://arxiv.org/pdf/2607.20357) | 未读 | 暂无 |

### F · 多模态 Serving

| 序号 | 简称 | 标题 | PDF 链接 | 状态 | 笔记链接 |
| --- | --- | --- | --- | --- | --- |
| 14 | EPD · [Zotero](zotero://select/library/items/YR2VE82F) | Efficiently Serving Large Multimodal Models Using EPD Disaggregation | [PDF](https://arxiv.org/pdf/2501.05460) | 未读 | 暂无 |
| 15 | ModServe · [Zotero](zotero://select/library/items/BTGL8M3S) | ModServe: Modality- and Stage-Aware Resource Disaggregation for Scalable Multimodal Model Serving | [PDF](https://arxiv.org/pdf/2502.00937) | 未读 | 暂无 |
| 16 | HydraInfer · [Zotero](zotero://select/library/items/PJAAKAZB) | HydraInfer: Hybrid Disaggregated Scheduling for Multimodal Large Language Model Serving | [PDF](https://arxiv.org/pdf/2505.12658) | 未读 | 暂无 |
| 17 | ElasticMM · [Zotero](zotero://select/library/items/QSL4JZ98) | ElasticMM: Efficient Multimodal LLMs Serving with Elastic Multimodal Parallelism | [PDF](https://arxiv.org/pdf/2507.10069) | 未读 | 暂无 |
| 18 | TCM-Serve · [Zotero](zotero://select/library/items/KB5332M5) | TCM-Serve: Modality-aware Scheduling for Multimodal Large Language Model Inference | [PDF](https://arxiv.org/pdf/2603.26498) | 未读 | 暂无 |

## 泛读清单

??? note "G · Background (Skim)：27 篇背景论文"

    - [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](https://arxiv.org/pdf/2306.00978) · [Zotero](zotero://select/library/items/TPNVNU3A)
    - [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/pdf/2401.15077) · [Zotero](zotero://select/library/items/AQPLRUYK)
    - [Efficient Inference for Large Vision-Language Models: Bottlenecks, Techniques, and Prospects](https://aclanthology.org/2026.findings-acl.1057.pdf) · [Zotero](zotero://select/library/items/ML7AA4K9)
    - [Efficient Streaming Language Models with Attention Sinks](https://arxiv.org/pdf/2309.17453) · [Zotero](zotero://select/library/items/D45FHZUQ)
    - [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/pdf/2211.17192) · [Zotero](zotero://select/library/items/CMKEYMBD)
    - [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/pdf/2307.08691) · [Zotero](zotero://select/library/items/GREKPM4M)
    - [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/pdf/2205.14135) · [Zotero](zotero://select/library/items/65P68IAK)
    - [FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving](https://arxiv.org/pdf/2501.01005) · [Zotero](zotero://select/library/items/6QXMYG3Z)
    - [How Far Are We to GPT-4V? Closing the Gap to Commercial Multimodal Models with Open-Source Suites](https://arxiv.org/pdf/2404.16821) · [Zotero](zotero://select/library/items/5A2B2M3V)
    - [H₂O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models](https://arxiv.org/pdf/2306.14048) · [Zotero](zotero://select/library/items/DXR9LJ7F)
    - [Improved Baselines with Visual Instruction Tuning](https://arxiv.org/pdf/2310.03744) · [Zotero](zotero://select/library/items/ZVQ9TJZW)
    - [KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache](https://arxiv.org/pdf/2402.02750) · [Zotero](zotero://select/library/items/ZHENBECS)
    - [MagicPIG: LSH Sampling for Efficient LLM Generation](https://arxiv.org/pdf/2410.16179) · [Zotero](zotero://select/library/items/6UWGIPBJ)
    - [MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention](https://arxiv.org/pdf/2407.02490) · [Zotero](zotero://select/library/items/XCG29I76)
    - [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](https://arxiv.org/pdf/2407.00079) · [Zotero](zotero://select/library/items/EAXBRKSY)
    - [RUTA: Principled Visual Token Allocation via Rate-Utility Optimization](https://arxiv.org/pdf/2608.04132) · [Zotero](zotero://select/library/items/A9D95M97)
    - [SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills](https://arxiv.org/pdf/2308.16369) · [Zotero](zotero://select/library/items/9K5FVMFW)
    - [Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time](https://arxiv.org/pdf/2305.17118) · [Zotero](zotero://select/library/items/MPNZ4NDZ)
    - [SGLang: Efficient Execution of Structured Language Model Programs](https://arxiv.org/pdf/2312.07104) · [Zotero](zotero://select/library/items/8CTX7RIP)
    - [SnapKV: LLM Knows What You are Looking for Before Generation](https://arxiv.org/pdf/2404.14469) · [Zotero](zotero://select/library/items/DY9YRQKR)
    - [SparseVLM: Visual Token Sparsification for Efficient Vision-Language Model Inference](https://arxiv.org/pdf/2410.04417) · [Zotero](zotero://select/library/items/82S3BWLQ)
    - [Splitwise: Efficient generative LLM inference using phase splitting](https://arxiv.org/pdf/2311.18677) · [Zotero](zotero://select/library/items/A28QRUDP)
    - [S³: Increasing GPU Utilization during Generative Inference for Higher Throughput](https://arxiv.org/pdf/2306.06000) · [Zotero](zotero://select/library/items/NP7EGC8I)
    - [Towards Efficient Large Vision-Language Models: A Comprehensive Survey on Inference Strategies](https://arxiv.org/pdf/2603.27960) · [Zotero](zotero://select/library/items/MTG3B7YX)
    - [VisionZip: Longer is Better but Not Necessary in Vision Language Models](https://arxiv.org/pdf/2412.04467) · [Zotero](zotero://select/library/items/W5RUXH3Z)
    - [vLLM-Omni: Fully Disaggregated Serving for Any-to-Any Multimodal Models](https://arxiv.org/pdf/2602.02204) · [Zotero](zotero://select/library/items/SCVN75B3)
    - [xLLM Technical Report](https://arxiv.org/pdf/2510.14686) · [Zotero](zotero://select/library/items/BKCQMQ6S)

??? note "配套项目与官方资料"

    - [FlashInfer Documentation](https://docs.flashinfer.ai/) · [Zotero](zotero://select/library/items/46REJTA4)
    - [LightLLM](https://github.com/ModelTC/lightllm) · [Zotero](zotero://select/library/items/DMBZLK2J)
    - [DeepSpeed](https://github.com/deepspeedai/DeepSpeed) · [Zotero](zotero://select/library/items/EA2TUMDM)
    - [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) · [Zotero](zotero://select/library/items/3J3VFAYB)
    - [InternVL2](https://internvl.github.io/blog/2024-07-02-InternVL-2.0/) · [Zotero](zotero://select/library/items/3KANFLNE)
