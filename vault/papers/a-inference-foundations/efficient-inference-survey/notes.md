---
aliases:
- 1.A Survey on Efficient Inference for Large  Language Models
---

# A1 · 高效 LLM 推理综述：原始笔记

阅读日期：2026-10-13 · [论文](https://arxiv.org/abs/2404.14294) · [逐问答疑](answers.md) · [研读清单](reading-list.md)

!!! note "原始阅读记录"
    保留阅读时的问题与判断。以下猜想尚未经过实验验证；概念修正与后续资料见逐问答疑。原文仅调整图片链接、制表符和网页排版。

1. **问题**：首先这是一篇综述，主要叙述了LLM的瓶颈
    
    ![inference-survey-20261013152050](../../../images/inference-survey-20261013152050.png)
    大模型推理的计算量大幅提高，导致了三种常见因素(**计算成本，内存访问成本和内存使用量**)同时在资源受限的情况下，可能会降低效率指标(**延迟，吞吐量，存储需要，功耗等**)
    问题所在：
    1. model size: **即模型参数过多**
    2. attention operation: 输入prompt过长，prefill阶段计算太大
    3. decoding approach: decode阶段，每次自回归的时候都要加载KV Cache，这个造成的是内存访问成本的增加
    什么是**roofline model**？
2. **目前的方法**：
    分为三类
    1. data-level: 输入压缩，输出组织方面入手
    2. model-level: 压缩模型，包括compression，量化等
    3. system-level:
3. System-level optimazation
    什么是LLM 的计算图？
    使用**不同模型，不同长度**对run time进行分析，发现**linear attention两部分加起来超过了75%** (何为linear operators attention operators，linear就是线性变换的算子GEMM？attention就是注意力计算的算子？) 因此一大重要的研究方向就是**优化算子** (算子如何优化，这是我应该去看的吗？针对多模态场景，还需要优化算子？)
    ![inference-survey-20261013170339](../../../images/inference-survey-20261013170339.png)
    ![inference-survey-20261013170658](../../../images/inference-survey-20261013170658.png)
    线性算子优化(GEMM优化)现在应该已经比较成熟了吧？针对多模态场景的话，计算应该仍用GEMM。主流框架(vLLM,DeepSpeed调用的是GEMM接口) 什么是cuBLAS，CURLASS？算子优化这部分我了解的很少，应该去了解吗？(我觉得这不是我的重点)
    
    Online Serving system: 核心是处理不同的异步请求
    **online serving面临的问题有: `memory, batching, and scheduling arising from asynchronous requests.`**
    1. memory-managemnet:  大多针对KV Cache。**带来了注意力算子访问内存随机性的问题，这个问题目前是否被解决？**
        >For the attention operator using the paged KV cache, this necessitates the consideration of the mapping relationship between the virtual address space of the KV cache and its corresponding physical address space. To enhance the efficiency of the attention operator, the loading pattern of the KV cache must be tailored to facilitate contiguous memory access.
        
        **The optimization of the attention operator in conjunction with paged KV cache storage remains a forefront challenge in the advancement of serving systems.**
        这个问题现在研究的人是否多？或许这是一个好的研究方向？ 何为注意力算子与paged KV Cache的联合？如何解释？
    2.  continuous batching: 不同长度的请求，导致了GPU的低利用率的问题
        异步性质的存在，长短请求不一致，导致着利用率低
        orca提出continuous batching，随后vLLM扩展到**注意力计算？** 如何理解？具体是哪一部分？
        拆解融合，对于多模态来讲，**continuous batching是否足够用？**
        **split and fuse 策略？** 具体是哪一篇文章？是把prefill和decode解码了吗？对与多模态来说应该如何呢？前提是prefill阶段请求可以分为块，为什么？
        chunked prefill是一种前沿的方法，如果往下去多模态扩展，是否还是一个难题？continuous batching的研究潜力目前看来或许不如memory management
    3. scheduling strategy
        执行的请求顺序会影响吞吐量
        orca vllm ligthllm采用的调度策略都是FCFS
        FastServe  用了**多级优先队列**
        总的看来，调度算法其实大部分是迁移OS调度的，现在是否能针对多模态场景提出一种新的调度算法？我觉得这或许是一个潜力
        现有文献大多用预测机制设计调度算法，但是预测的方法还未能达到令人满意的效果，**因此这是一个potential的研究方向**
    4. 多模态框架仍然是一个promising的研究领域(multimodal serving system)

研读计划：
online system serving:
1. memory management : 
    1. S3，核心思想，存在什么不足？为什么这样设计？
    2. pagedattention: 核心思想？还存在什么不足
    3. LightLLM: 基于vLLM做出了什么改变？不足之处？
    4. flashInfer: 提供了多样的内存访问方式？
2. continous batching:
    1. orca:
    2. Sarathi DeepSpeed-FastGen  and SarathiServe 
3. scheduing stratey
    1. DeepSpeed-FastGen
    2. FastServe
    3. VTC

服务框架
- DeepSpeed
- vLLM
- LightLLM
- TensorRT-LLM
