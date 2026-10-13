---
title: 逐问答疑与方向判断
---

# 第一篇综述：逐问答疑与方向判断

日期：2026-10-13 · 对应 [原始笔记](notes.md) · [下一步研读清单](reading-list.md)

这份答疑按笔记中的问题展开。基础概念给出解释；涉及选题的部分给出当前判断、已有工作的边界和需要做的验证。“值得验证”表示一个候选问题，不能当作创新性已经成立。软件能力依据文末链接的官方资料核对，实验必须另行记录具体版本。

## 1. 什么是 Roofline model？

**问题**：什么是 roofline model？为什么总说 prefill 受算力限制、decode 受访存限制？

**回答**：Roofline 用计算能力和内存带宽两个上限，估计一个算子最多能跑多快。定义算术强度 `I = FLOPs / 传输字节数`，则简化的性能上限为：

```text
可达算力 ≤ min(峰值算力, 内存带宽 × 算术强度)
```

例如一台假想 GPU 的算力是 100 TFLOP/s，带宽是 1 TB/s，算子每搬运 1 字节只做 10 次浮点运算，那么带宽只能支撑约 10 TFLOP/s。此时继续增加乘加单元不能直接补上差距。这是教学例子，不是 A800 的实测规格。

Prefill 一次处理较多 token，权重有机会被反复利用；小 batch decode 每个请求一次只生成一个 token，权重读取往往难以充分摊薄，attention 还要读历史 KV。于是前者常更偏计算受限，后者常更偏带宽受限。实际瓶颈会随 batch、上下文长度、精度和硬件变化，不能给整个阶段贴一个永远不变的标签。

Roofline 是分析起点，不涵盖所有排队、通信、CPU 调度和 kernel 启动开销。你下一篇 A2 可以重点练习：找一个实际算子，估 FLOPs 和 bytes，再与 profiler 结果对照。

参考：[NVIDIA 矩阵乘性能指南](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html)、[LLM Inference Unveiled](https://arxiv.org/abs/2402.16363)。

## 2. 什么是 LLM 的计算图？

**问题**：什么是 LLM 的计算图？

**回答**：把张量运算画成有依赖关系的图。节点表示计算，边表示张量从哪一步流向下一步。一个简化的 Transformer 层可以写成：

```text
输入 → Norm → Q/K/V 投影 → Attention → 输出投影 → 残差相加
     → Norm → FFN → 残差相加 → 下一层
```

图能告诉执行系统：哪些步骤必须等待前面的结果、哪些运算可以合并、哪些中间结果需要保存。图优化可能减少重复计算、合并小算子，或者减少不必要的中间张量读写。

要区分数学意义的计算图与 **CUDA Graph**。CUDA Graph 是把一组 GPU 操作及依赖捕获后重复执行的一种机制，主要用于降低重复提交工作时的 CPU 开销；它不等于改了 attention 的数学公式。动态形状、地址稳定性和可捕获操作会影响实际使用方式。

参考：[vLLM CUDA Graphs 设计文档](https://docs.vllm.ai/en/latest/design/cuda_graphs/)。

## 3. Linear operators 和 attention operators 分别是什么？

**问题**：linear 就是 GEMM 吗？attention 就是注意力计算吗？两者超过 75% 怎么理解？

**回答**：你理解的方向基本正确。这里的 **linear operators** 主要指带学习参数的线性投影，例如 `XW_Q`、`XW_K`、`XW_V`、attention 输出投影以及 FFN 中的线性层，常用 GEMM 实现；小形状下也可能采用其他实现。

**Attention operators** 主要指 Q、K、V 形成之后的注意力核心，例如 `softmax(QKᵀ / √d)V`。它里面也有矩阵乘。分类依据是模型里的功能，因此“底层用了矩阵乘”和“被统计为 linear operator”不是同一件事。

笔记里“linear attention 两部分”建议改成“**linear operators 与 attention operators 两部分**”，否则容易被理解为另一类模型方法 Linear Attention。

综述的 75% 来自其指定实现、模型和上下文长度下的 profiling。它说明那些测试条件下的大头在哪里，不能直接当成你多模态 vLLM 实验的耗时比例。[综述 §VI-A1](https://arxiv.org/html/2404.14294v3#S6.SS1.SSS1)。

## 4. 算子怎么优化？这是我必须深入的方向吗？

**问题**：算子如何优化？针对多模态还需要优化算子吗？我觉得这不是重点。

**回答**：常见方式包括分块复用数据、减少 HBM 读写、融合相邻操作、改善线程间的访存排列，以及选择适合形状和精度的 kernel。FlashAttention 是“重新组织计算以减少数据搬运”的典型例子。[FlashAttention](https://arxiv.org/abs/2205.14135)

多模态仍有这些运算，但新增问题还可能出在图像预处理、视觉编码、不同分辨率造成的形状变化和阶段间干扰。仅凭“多模态”不能推导出必须写一个新算子。

**对你当前路线的建议**：先学到能看懂 profiler、能辨认 GEMM/attention/数据复制、能解释 shape 对性能的影响。暂时不要求从零写高性能 CUDA GEMM。只有当数据证明现有 kernel 在你的目标负载上留下明显缺口，再决定补 Triton/CUDA 或寻求合作。这是学习优先级建议，不是对算子研究价值的否定。

## 5. GEMM 已经成熟了，还会有研究空间吗？

**问题**：GEMM 优化应该很成熟了吧？多模态计算仍然用 GEMM，是不是可以不管？

**回答**：通用 GEMM 库很成熟，但同一个库面对小矩阵、不同精度、不同形状和不同硬件，效率不会完全一样。优化还涉及融合、数据布局、低精度实现及资源分配。[NVIDIA CUTLASS](https://github.com/NVIDIA/cutlass)

对 Serving 研究更直接的问题是：你的调度和 token 预算会产生什么矩阵形状？减少 token 后，时间是否按比例减少？调度是否让 GPU 长时间只处理很小的 batch？这些问题即使不修改 GEMM kernel 也需要理解。

同时要检查旧规划里“144-token 请求单独一桶、288-token 请求一桶”的假设。**不能预设 vLLM 必须按相同长度分桶**：不同模块可能采用 padding、packing 或不同 batching 规则。只有先确认目标执行路径确实有这样的分桶或形状效应，这个例子才能成为实验假设。

## 6. cuBLAS、CUTLASS 分别是什么？

**问题**：什么是 cuBLAS、CURLASS？框架是不是都调用 GEMM 接口？

**回答**：正确拼写是 **CUTLASS**。

| 名称 | 作用 | 当前需要了解的程度 |
|---|---|---|
| cuBLAS / cuBLASLt | NVIDIA 提供的 GPU 线性代数库，可直接调用矩阵乘等操作 | 知道调用关系、dtype、shape 和性能选择 |
| CUTLASS | 用于构建和定制高性能线性代数 kernel 的模板及相关开发组件 | 知道它服务于 kernel 实现，暂不必全面精读 |
| GEMM | 矩阵乘运算类别，不是某一个软件包 | 能看懂 M、N、K 和 FLOPs |

框架可能通过 PyTorch、cuBLAS、CUTLASS、Triton 或专用 kernel 执行线性层，具体路径取决于版本、模型和量化配置，不能统一写成“所有地方都调用 cuBLAS”。

参考：[cuBLAS 官方文档](https://docs.nvidia.com/cuda/cublas/index.html)、[CUTLASS 官方仓库](https://github.com/NVIDIA/cutlass)。

## 7. 分页 KV cache 会导致随机访存吗？

**问题**：memory management 带来了 attention 访问内存随机性的问题，这个问题解决了吗？

**回答**：更准确的表述是“**逻辑连续的 token，可能落在不连续的物理块里**”。例如一个请求的逻辑块 `[0, 1, 2]` 对应显存块 `[7, 2, 11]`。kernel 先查块表，然后在每个块里按照布局读取 K/V。

这不意味着每个元素都无规则地跳转，也不意味着每次读取都从 CPU 把数据传到 GPU。块内可以安排连续、合并的访存；不同块之间通过索引找到位置。你笔记中的“加载 KV”通常首先要理解为 GPU 计算时从显存读取历史 KV。

PagedAttention 已经给出了实用的分页存储与 attention 实现；仍有索引、布局、负载均衡和硬件适配等开销可以优化。它把原来的空间浪费问题大幅改善了，却没有让所有 KV 访问在任意工作负载下都达到最优。

参考：[PagedAttention 论文](https://arxiv.org/abs/2309.06180)、[vLLM Paged Attention 设计说明](https://docs.vllm.ai/en/latest/design/paged_attention/)。

## 8. “Attention 算子与 paged KV cache 联合优化”具体指什么？

**问题**：何为两者联合？如何解释？

**回答**：存储方式决定数据怎么摆，attention kernel 决定线程怎么取这些数据，两者必须配合。例如页面大小、K/V 各维度的排列、线程负责的 head/token 范围、跨页读取方式，都会影响显存利用和执行效率。

一个教学性的权衡是：页面变小可能减少最后一页没填满的浪费，但也可能增加块表条目和索引工作；更大的页面可能便于成块处理，却让短请求浪费更多空间。这只是需要测量的方向，不是“页面越大/越小一定越快”的结论。

FlashInfer 的工作把可变序列、不同 KV 布局和 attention 执行调度放在一起考虑，适合用来理解这类接口。[FlashInfer 论文](https://arxiv.org/abs/2501.01005)

## 9. 这个方向现在研究的人多吗，值得我选吗？

**问题**：分页 KV 与算子联合优化是否还是好方向？

**回答**：这是已有较多实现和研究的方向。FlashInfer，以及通过 GPU 虚拟内存管理保留连续虚拟地址的 vAttention，已经提供不同路线。因此“分页导致不连续，所以我要优化一下”还不足以形成新问题。[vAttention](https://arxiv.org/abs/2405.04437)

**当前判断**：值得作为重点基础学习；是否成为你的主选题，要等目标负载的证据。可以先问：多图/视频的 KV 长度与复用模式是否让现有方法出现特别的开销？是否能在现代 backend 上稳定重现？改进需要碰 kernel 的程度有多深？如果只是在旧版框架上换个页面大小，研究贡献通常不足。

这次查到的代表工作可以排除“还是空白”的判断，不能据此断言已经穷尽所有最新相关工作。

## 10. Orca 的 batching 与 vLLM 的 attention batching 有什么区别？

**问题**：Orca 提出 continuous batching，随后 vLLM 扩展到 attention，具体是哪一部分？

**回答**：Orca 的 iteration-level scheduling 允许每轮迭代重新组成运行中的请求集合。它的 selective batching 会把适合一起执行的运算合并，而 attention 需要处理不同请求各自的历史长度，因此不能像共享权重的线性层一样简单拼接。[Orca 论文与报告](https://www.usenix.org/conference/osdi22/presentation/yu)

PagedAttention 允许一次 attention 执行处理具有不同上下文长度、不同物理 KV 块映射的请求。每个请求仍然只关注自己的上下文，不会把请求 A 的 token 和请求 B 的 token 混在一起计算语义。

需要区分两层：**调度器决定哪些请求进这一轮，kernel 决定这一轮怎么高效执行**。前者支持连续进出，并不自动保证后者能高效处理所有不规则形状。[PagedAttention](https://arxiv.org/abs/2309.06180)

## 11. Continuous batching 对多模态足够吗？

**问题**：多模态场景中 continuous batching 是否足够用？

**回答**：它能改善请求结束后空出来的计算机会，仍是有用基础。但多模态还有视觉编码、预处理、数据搬运，以及 encode/prefill/decode 之间的资源竞争。只在 LLM decode 端连续补请求，无法保证整条流水线都没有瓶颈。

ModServe 和 EPD 已经把多模态阶段差异作为系统设计的重要依据，所以“把连续批处理用于多模态”本身不能当作新贡献。[ModServe](https://arxiv.org/abs/2502.00937)、[EPD Disaggregation](https://arxiv.org/abs/2501.05460)

你可以先做一个对照：固定输出长度和请求率，改变图片数/分辨率，同时记录 encode 排队、prefill 排队、TTFT、ITL 和显存。如果瓶颈主要在 encoder 前面的等待，那么只改 decode batching 很可能解决不了主问题。这是建议做的实验，当前还没有实测结论。

## 12. Split-and-fuse 是哪篇？是不是 PD 分离？

**问题**：split and fuse 策略具体是哪篇文章？是把 prefill 和 decode 拆开了吗？

**回答**：**Dynamic SplitFuse** 是 DeepSpeed-FastGen 中的具体策略名。其核心是拆分较长 prompt 的 prefill 工作，再把这些工作与 decode token 组织成合适的批次。综述还把 Sarathi、Sarathi-Serve 中相关做法放在这一类讨论。[DeepSpeed-FastGen](https://arxiv.org/abs/2401.08671)

举一个不对应论文具体参数的例子：

```text
一轮有 512 个 token 的处理预算：
先容纳 32 个请求各自的 1 个 decode token，
再用剩余预算处理长 prompt 的一个 prefill chunk。
```

实际顺序和预算规则依系统而定。这里的“拆”发生在 **token 工作量/迭代** 层面。DistServe、Splitwise 的 PD disaggregation 则把 prefill 与 decode 放到不同的执行资源上；两者可以组合，不能当作同一个概念。

## 13. 为什么 prefill 可以切成 chunk？

**问题**：前提是 prefill 可以分块，为什么？

**回答**：对使用 causal attention 的 decoder-only Transformer，第 `i` 个位置只依赖它自己及之前的位置。假设 prompt 有 1,024 个 token，先计算前 512 个并保存各层 K/V，再计算后 512 个时读取前面已有的 KV，并在当前块内使用正确的 causal mask，就能保持相同的依赖关系。

这里的等价是数学依赖关系上的等价，不承诺不同 kernel 和浮点归约顺序产生逐 bit 相同的结果。实现还必须正确处理 position IDs、mask 和 KV 写入位置。

分块改变的是何时计算，不是让后半段忘记前半段。收益常来自给其他请求让出执行机会；代价可能是更多启动、调度或历史 KV 读取。chunk 过小未必更快。[Sarathi](https://arxiv.org/abs/2308.16369)、[Sarathi-Serve](https://arxiv.org/abs/2403.02310)

## 14. 多模态 chunked prefill 还是难题吗？

**问题**：把 chunked prefill 扩展到多模态，是否仍然很难？

**回答**：要分模型部件判断。对把视觉 embedding 插入 causal LLM 序列的模型，LLM 侧通常仍可利用上述因果性；但视觉 encoder 可能采用双向注意力，不能照搬“只保留过去 KV”来随意切图像 token。使用 cross-attention 或特殊 mask 的模型，还需要另外分析依赖关系。

当前 vLLM 的调度配置已经包含多模态输入与 chunk 的相关控制，说明基础支持已有工程实现。具体某种多模态片段能否被拆、encoder 预算如何处理，需要看对应模型和版本。[vLLM SchedulerConfig](https://docs.vllm.ai/en/latest/api/vllm/config/scheduler/)、[多模态数据处理](https://docs.vllm.ai/en/latest/design/mm_processing/)

**方向判断**：只实现“多模态能用 chunked prefill”通常不够。更值得验证的是不同图片数、分辨率和文本混合比例下，chunk 大小、encode 时机和 decode SLO 之间是否存在现有策略处理不好的权衡。

## 15. Batching 的潜力是不是不如 memory management？

**问题**：continuous batching 的研究潜力目前看来或许不如 memory management？

**回答**：现在还不能这样排序。二者互相约束：KV 空间不够，调度器放不进更多请求；batch 组成变化，又会改变 KV 占用和执行效率。即使显存很多，长 prefill 对 decode 的干扰也可能限制服务质量。

可以把兴趣转成一个可否定的问题：**在我的负载上，增加 KV 可用容量与改善 batch 组成，哪个更能提高满足 SLO 的吞吐？** 如果把 KV 容量人为放宽后问题仍然存在，就说明主因未必是容量；如果调整 batching 几乎不改变结果，也应降低这条线的优先级。

这是实验设计建议，不是已有结果。先测限制来自哪里，再评估哪类改进值得投入。

## 16. 现在的框架都是 FCFS 吗？执行顺序为什么会影响吞吐？

**问题**：Orca、vLLM、LightLLM 都采用 FCFS；排序改变吞吐，是不是只要优先短请求？

**回答**：综述对特定时期系统的描述不能直接替代当前源码。当前 vLLM 的调度配置可区分 FCFS 与 priority 等策略；请求排序之外还有 token budget、chunked prefill、KV 分配和抢占等规则。[vLLM SchedulerConfig](https://docs.vllm.ai/en/latest/api/vllm/config/scheduler/)

排序可能改变哪些请求占着 KV、哪些请求一起执行、何时释放资源，也会改变排队延迟。但降低平均完成时间、提高 tokens/s、提高满足 SLO 的 req/s、保证用户公平性，是不同目标。优先短请求可能改善平均等待，也可能让长请求长期等待。

FastServe 适合读抢占与完成时间，VTC 适合读多用户公平性。不要把某一个目标上的收益自动推广为所有指标都更好。[FastServe](https://arxiv.org/abs/2305.05920)、[VTC](https://arxiv.org/abs/2401.00588)

## 17. 从 OS 借鉴调度，还能做出多模态新算法吗？

**问题**：这些算法大多迁移 OS 调度，多模态是否还能提出新调度算法？

**回答**：可以借鉴 OS 思想，但需要证明多模态引入了现有策略没有处理好的约束。可关注的差异包括阶段资源需求不同、视觉 token 成本变化、可复用的编码结果，以及质量约束下允许调整的计算预算。

TCM-Serve 已直接研究模态感知调度；ModServe 也涉及模态与阶段资源管理。因此“按图片和文本区分优先级”这个宽泛描述已经不足以说明创新。[TCM-Serve](https://arxiv.org/abs/2603.26498)、[ModServe](https://arxiv.org/abs/2502.00937)

**给你的候选问题**：同样数量的视觉 token 是否有不同的阶段成本？只用 token 数的调度是否因此违反某类请求的 SLO？加入可测的阶段成本是否有效？如果还要调整视觉预算，必须同时证明回答质量符合约束，且收益超过决策与重组 batch 的成本。

在这些问题有数据前，“语义感知 + 系统状态感知”只能作为研究假设。

## 18. 输出长度预测不好，是否是一个潜在方向？

**问题**：现有预测机制效果不够好，所以提升预测是否有潜力？

**回答**：有可能，但预测误差下降不等于服务性能提高。调度可能只需要辨别长短、估计区间或判断是否将超出预算，不一定需要精确预测输出长度。S³ 使用预测辅助资源分配；FastServe 的 skip-join MLFQ 则利用已知输入信息和逐步反馈，不能简单概括为“先准确预测完整输出长度”。[S³](https://arxiv.org/abs/2306.06000)、[FastServe](https://arxiv.org/abs/2305.05920)

建议先做一个上限实验：在离线重放中提供真实输出长度作为 oracle，比较它与无需预测的强基线。如果知道答案后收益仍很小，训练更复杂的预测器就缺少必要性。若上限明显，再加入真实预测开销、误差和分布变化，检查 goodput 是否仍然提升。

记录 MAE/排序误差之外，还要记录错误的后果：低估是否导致抢占或重算，高估是否占住资源，以及哪一类用户/请求受到更多影响。

## 19. 多模态 Serving 仍然值得研究吗？

**问题**：multimodal serving system 仍然是 promising 的研究领域吗？

**回答**：有明确系统问题可研究，但已不是“支持多模态”就足够新颖的阶段。EPD、ModServe、HydraInfer、ElasticMM 等工作已经研究阶段分离、资源分配和负载适应。你要在它们的假设、负载和实现能力之间找具体缺口。[EPD](https://arxiv.org/abs/2501.05460)、[HydraInfer](https://arxiv.org/abs/2505.12658)、[ElasticMM](https://arxiv.org/abs/2507.10069)

**当前优先级建议**：先完成 A 组基础与 B 组核心机制，再用一个代表性多模态模型测出 encode、prefill、decode 的耗时和排队分布。对你而言，阶段干扰、异构请求调度和质量约束下的预算决策，比立即挑战通用 GEMM kernel 更接近现有积累。

这不是创新性保证。最终选题应有可复现的反例负载，能说明强基线为什么失败，并能解释方案在什么条件下不会获益。

## 20. S³、PagedAttention、LightLLM、FlashInfer 应分别读什么？

**问题**：这些方法的核心思想、不足以及彼此区别是什么？

**回答**：先给它们不同的阅读任务，避免把几篇都记成“优化 KV”。

| 材料 | 主要阅读任务 | 需要追问的边界 |
|---|---|---|
| S³ | 预测长度如何影响内存预留与调度 | 误预测如何处理；相对现代动态分配基线是否还有收益 |
| PagedAttention | 逻辑块到物理块的映射、按需增长、共享 | 最后一块浪费、块表管理、kernel 访问代价 |
| LightLLM | 官方实现中的 token 级内存管理及请求执行路径 | 元数据和索引成本；不同版本是否改变设计 |
| FlashInfer | 不同 KV 布局下的 attention 接口和执行策略 | 对目标模型、head 结构、精度、硬件和 batch 的适配范围 |

这些“追问”是读论文和源码时要验证的内容，不能直接写成作者已经承认的缺陷。LightLLM 是独立项目，综述中的“在 vLLM 基础上”应理解为方案比较，不能据此断言其仓库是 vLLM fork。

参考：[S³](https://arxiv.org/abs/2306.06000)、[PagedAttention](https://arxiv.org/abs/2309.06180)、[LightLLM](https://github.com/ModelTC/lightllm)、[FlashInfer 文档](https://docs.flashinfer.ai/)。

## 21. Sarathi、Sarathi-Serve、FastGen 是不是重复？

**问题**：研读计划里的 Sarathi、DeepSpeed-FastGen、Sarathi-Serve 都要读吗？

**回答**：它们相关，但不是同一篇。Sarathi 是 2023 年的早期工作；Sarathi-Serve 是 2024 年进一步面向 Serving 的工作；DeepSpeed-FastGen 是另一套系统中的 Dynamic SplitFuse 方案。

建议先精读 Sarathi-Serve，画出每轮 token budget 如何分给 decode 和 prefill；再用 Sarathi 理解最初的思路；最后对照 FastGen 的批次构造与目标。不要只比较论文摘要中的加速倍数，因为模型、硬件、负载和基线版本不同。

参考：[Sarathi](https://arxiv.org/abs/2308.16369)、[Sarathi-Serve](https://arxiv.org/abs/2403.02310)、[DeepSpeed-FastGen](https://arxiv.org/abs/2401.08671)。

## 22. DeepSpeed、vLLM、LightLLM、TensorRT-LLM 要全部学透吗？

**问题**：服务框架列了四个，接下来应该怎么安排？

**回答**：先选 **vLLM 作为主实践框架**，沿请求入口、scheduler、KV manager、model runner 这条路径读源码并做实验。其他框架作为针对具体问题的对照：读 FastGen 时查 DeepSpeed-MII/Inference，读 token 级 KV 管理时查 LightLLM，需要 NVIDIA 生态的部署对照时查 TensorRT-LLM。

先跑通一个可复现实验，比同时记四套架构更有帮助。框架功能持续变化，所以笔记里应记录版本或 commit、模型 revision、硬件、输入输出长度、并发与请求率，以及启用的缓存和 batching 配置。

官方入口见 [框架资料](../../../practice/frameworks.md)。

## 对今天笔记的整体评价

你已经开始把“作者说了什么”转成“这个问题现在还有没有空间”，这份笔记适合作为研究问题清单。下一步要补的是证据状态：把每条判断标成“论文已有结论”“我还没理解的机制”“待检索的判断”“待实验的假设”，不要把它们混在同一层。

这篇综述不必强行填满研究论文模板中的 ablation 和核心假设。对综述更合适的产出是分类地图、机制之间的区别、需要精读的原论文，以及不能直接沿用到今天的判断。你已经有了这些材料，接下来按 [研读清单](reading-list.md) 逐篇验证即可。
