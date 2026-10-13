---
search:
  exclude: true
---

!!! warning "历史研究构想，尚未验证"
    这是原有规划的归档稿，保留当时的设想。文中对文献、会议和研究空白的判断尚未全部重新核查，不代表本站已确认的结论；原稿标注日期与部分后续文献时间也需复核。当前判断见 [研究问题清单](questions.md)。

# 语义感知计算分配 × 硬件感知执行：MLLM 推理系统研究路线

> 更新时间：2026-09-15
>
> 当前定位：**多模态大模型推理系统（MLLM inference/serving systems）**

---
```
GPU architecture
      ↓
CUDA execution model
      ↓
PyTorch GPU execution
      ↓
Profiling
      ↓
Attention / GEMM 性能
      ↓
MLLM serving runtime
      ↓
必要时再学 Triton / CUDA kernel optimization
```

## 0. 先把方向说清楚

### 我们不是在做什么

- 不是单独设计一个新的 visual token pruning 算法。
- 不是单独做一个 GPU scheduler。
- 不是把数据库 query optimizer 搬到多模态模型上。
- 也不是简单把“少 token”与“GPU batching”两个模块拼起来。

### 我们想研究什么

暂时把方向定义为：

**Semantic- and Hardware-Aware Adaptive MLLM Serving**

或者更强调方法论：

**Cross-Layer Co-Design for Adaptive Multimodal Inference**

核心思想：

> 对每个 image/video + query 请求，系统不再把模型执行配置视为固定不变，而是同时考虑请求的语义计算需求与实时 GPU serving 状态，联合决定“算多少”和“怎么跑”，在满足回答质量与 SLO 的条件下优化端到端延迟、吞吐和 GPU 成本。

最简结构：

```text
image/video + query
        |
        v
Semantic-aware Compute Controller
这个请求需要多少视觉/模型计算？
        |
        |  execution configuration
        v
Hardware-aware Runtime / Scheduler
当前 queue / batch / GPU 状态下怎么执行最划算？
        |
        v
       GPU
        |
        v
      answer
```

真正的 **co-design** 在于两层不是独立的：

```text
semantic requirement  <---->  serving / GPU state
                    |
                    v
          joint execution decision
```

即：前端预算决策可以感知当前系统状态；后端 scheduler 也知道不同 fidelity / compute configuration 的语义质量与成本。

---

## 1. 从 idea 反推：我们真正要解决的问题是什么？

### 1.1 当前领域存在两种“异质性”

#### A. Semantic / content heterogeneity

不同 request 对视觉信息和推理计算的需求不同。

例如：

- “图里有没有汽车？”可能低 visual fidelity 就足够。
- “挡风玻璃左下角是否有细小裂痕？”可能需要更多视觉细节。

因此，一个固定的 visual token / resolution / compute budget 对所有请求都未必合理。

#### B. System / hardware heterogeneity

即使每个请求的计算需求已经确定，GPU serving 仍然受到：

- 不同视觉 token 长度
- 不同 input resolution
- encoder / prefill / decode 的资源特征差异
- batch composition
- queueing
- SM / HBM 利用率
- 并发请求
- SLO

等因素影响。

### 1.2 现有研究的核心断层

目前大部分工作分别优化两边：

```text
模型 / 算法侧
“这个 request 应该算多少？”

        和

系统 / serving 侧
“这些固定 workload 应该怎么放到 GPU 上跑？”
```

我们真正想研究的是两者之间的 **cross-layer coupling**：

> 单请求层面最省计算的 execution configuration，不一定是并发 serving 环境下端到端性能最优的 execution configuration。

例如：

```text
Request A
144 tokens 已经足够保证质量

但是：
当前 GPU queue 中有大量 288-token 请求，
而 144-token bucket 只有 A 一个请求。
```

如果只看单请求，应该选 144；
如果考虑 queue / batching / waiting time，288 反而可能更快完成。

这就是我们需要验证的核心系统现象。

---

## 2. 当前核心 Research Question

### 主问题

> **How can an MLLM serving runtime jointly adapt per-request computation to semantic demand and schedule heterogeneous requests according to live hardware state, so as to minimize end-to-end serving cost/latency under quality and SLO constraints?**

中文：

> **在多模态 serving 中，根据每个 query 的语义需求以及实时系统负载，联合决定 visual fidelity 和 request scheduling，从而在满足质量与 latency SLO 的条件下最小化 GPU 计算和显存成本。

```
                  Multimodal Request
                Image + Query
                       │
                       ▼
            ┌────────────────────┐
            │ Semantic Controller │
            └────────────────────┘
                       │
            这个 query 需要多精细？
                       │
             ┌─────────┼──────────┐
             ▼         ▼          ▼
          Low        Medium      High
        fidelity     fidelity   fidelity
             │
             │
       visual token budget
       image resolution
       frame sampling
       pruning ratio
       encoder compute
             │
             ▼
        Cost Predictor
             │
       预测计算资源：
       encoder FLOPs
       prefill tokens
       KV bytes
       latency
             │
             ▼
      ┌────────────────┐
      │ Runtime Scheduler│
      └────────────────┘
             │
     当前 GPU load
     KV cache occupancy
     waiting requests
     TTFT / TPOT SLO
             │
             ▼
           GPU
```
### 第一篇工作先收窄

不要一开始同时控制 resolution、frames、visual tokens、encoder depth、LLM depth、precision。

第一阶段只选择一个主要 semantic compute knob。

候选：

1. **visual token budget**：最直接，文献多，容易建立 baseline。
2. **input resolution / pre-encoder visual budget**：能进一步影响 vision encoder，本身可能带来更完整的端到端收益。

最终选哪个，不靠直觉决定；先 profiling。

### 最简优化形式

对请求 `r_i = (visual_i, query_i)`，实时系统状态为 `s_t`：

```text
choose:
    semantic compute budget b_i
    execution / scheduling action a_t

minimize:
    end-to-end latency / GPU cost

subject to:
    answer quality >= target
    P95/P99 latency <= SLO   （如果研究 online serving）
```

关键点：

```text
b_i = f(request semantics, system state)
a_t = g(queue, GPU state, b_i, quality constraint)
```

而不是先独立决定 `b_i`，再让 scheduler 被动接受。

---

## 3. 最需要验证的三个假设

### H1：Semantic heterogeneity 确实存在

> 不同 query-input pair 的最小充分计算预算差异明显。

定义：

```text
b*(x, q) = 在满足质量阈值时所需的最小 visual/computation budget
```

如果绝大多数 request 的 `b*` 基本一样，这个方向失去重要前提。

### H2：局部最优 != 系统最优

> **Per-request optimal compute is not necessarily serving-optimal execution.**

需要证明 variable budget 会影响：

- batching efficiency
- padding / fragmentation
- queueing delay
- GPU utilization
- encoder / prefill interference
- tail latency

这是从“adaptive pruning 算法”走向“systems paper”的关键。

### H3：联合决策优于串联优化

比较：

```text
A. full compute
B. static pruning / fixed budget
C. semantic-only adaptive compute
D. hardware-only serving optimization
E. semantic + hardware co-design
```

目标是证明 E 的 quality-latency / quality-throughput Pareto frontier 更好。

---

## 4. 当前研究版图：到底有多少人在做？

不能简单说“没人做”。截至 2026 年，这个领域两边都很活跃：

### 4.1 方向 A：Adaptive multimodal compute / visual fidelity

这一类已经有大量工作，主要回答：

> 对单个输入，应该保留多少视觉信息 / 多少模型计算？

代表工作：

#### SmartVL — Look Less, Think Faster: Joint Token-Compute Adaptation for Multimodal LLMs (ECCV 2026)

https://arxiv.org/abs/2607.20357

它已经非常接近我们的“联合计算分配”思想：

- 动态控制 visual token 数
- 动态控制 LLM compute
- 根据输入内容与 compute budget 联合决策
- 使用 differentiable latency estimator

**它是目前必须重点防撞的工作。**

但它主要仍是模型/单请求 inference 层面的 joint adaptation；我们需要重点确认它是否建模：

- multi-request queue
- dynamic batching
- live GPU utilization
- resource contention
- tail latency / SLO

如果没有，这就是我们与它最重要的边界。

---

#### ResAdapt — Adaptive Resolution for Efficient Multimodal Reasoning (2026)

https://arxiv.org/abs/2603.28610

核心：

- 在 vision encoder **之前**分配视觉预算
- 动态改变 spatial resolution / frame budget
- lightweight allocator
- unchanged MLLM backbone
- 强调与 vLLM / FlashAttention 等 optimized engine 的兼容性

它回答了：

> 如何根据 input content 在进入 encoder 前决定“看多少”。

我们要问：

> 它的 allocator 是否会根据实时 serving state 改变决策？

---

#### Vista-LLM — Decoupled Query-Guided Visual Token Pruning (ACL 2026)

https://aclanthology.org/2026.acl-long.601/

核心：

- query-guided dynamic budgeting
- query-specific token selection
- pruning 与主推理网络解耦
- 强调真实 inference acceleration 与 FlashAttention compatibility

它回答：

> 如何让 visual budget 与 query 本身相关。

我们重点看：

> 它是否只优化每个 sample 的 quality-efficiency，而不处理并发 serving 下的 batch / queue / GPU state？

---

#### QuietPrune — Query-Guided Early Token Pruning for VLMs (CVPR 2026)

https://openaccess.thecvf.com/content/CVPR2026/html/Gao_QuietPrune_Query-Guided_Early_Token_Pruning_for_Vision-Language_Models_CVPR_2026_paper.html

核心：

- 在 Vision Transformer 内更早 pruning
- query-guided
- 同时尝试减少 vision-side 与 downstream prefill cost

它很重要，因为它帮助我们理解：

> **预算决策放在 MLLM pipeline 的什么位置，决定到底能省哪一段 latency。**

---

### 4.2 方向 B：MLLM serving / GPU execution

这一类主要回答：

> 给定一批 multimodal workloads，GPU 怎么高效执行？

#### ModServe — Modality- and Stage-Aware Resource Disaggregation for Scalable Multimodal Model Serving (SoCC 2025)

https://arxiv.org/abs/2502.00937

重点：

- encoder / prefill / decode 多阶段异质性
- production multimodal traces
- stage disaggregation
- modality-aware scheduling
- autoscaling
- tail-latency SLO

它是理解 **MLLM serving 问题本身** 的第一篇核心系统论文。

---

#### SpaceServe — Spatial Multiplexing of Complementary Encoders and Decoders for Multimodal LLMs (NeurIPS 2025)

https://proceedings.neurips.cc/paper_files/paper/2025/hash/720e7ebc49c84252abc0754dddf80976-Abstract-Conference.html

重点：

- encoder compute-intensive / memory-light
- decoder 资源特征不同
- encoder / decoder colocate
- fine-grained SM partitioning
- cost-model-guided scheduling

它回答：

> encoder 与 decoder 怎么利用 GPU 的资源互补性。

---

#### ElasticMM — Efficient Multimodal LLMs Serving with Elastic Multimodal Parallelism (NeurIPS 2025)

https://arxiv.org/abs/2507.10069

重点：

- modality-aware load balancing
- stage decoupling
- elastic parallelism
- dynamic resource allocation
- prefix caching

它说明 serving runtime 已经可以根据 workload 动态调资源，但主要把模型的 computation demand 当成外部给定条件。

---

#### Resonator — Symbiotic MLLM Serving: Dynamically Balancing Parallelism Across GPUs and Resources Within GPUs (ISCA 2026)

DOI: https://doi.org/10.1109/ISCA66397.2026.00173

这是当前 **hardware-aware runtime** 方向最重要的近邻之一。

重点：

- runtime SM / HBM sharing
- encoder / decoder interference
- 根据 input resolution、batch composition 动态选择 parallelism
- inter-GPU + intra-GPU runtime decisions

它已经很接近我们后半部分“怎么跑”。

我们必须问：

> resolution / compute amount 是 workload 给定的，还是系统可以基于 query semantics 主动改变？

如果仍是给定的，我们的前端 semantic compute allocation 就是新的 control dimension。

---

## 5. 目前看到的真正 Gap

针对目前检索到的代表性工作，可以把 gap 写成：

### Adaptive-compute 工作的不足

它们越来越会回答：

```text
“这个输入需要多少 token / resolution / LLM compute？”
```

但通常没有把在线 serving 的：

- queue state
- batch composition
- concurrent requests
- GPU utilization
- resource contention
- tail latency / SLO

作为 compute allocation 的一等输入。

即：**semantic adaptation 很强，但 serving awareness 不够。**

### MLLM-serving 工作的不足

它们越来越会回答：

```text
“encoder / prefill / decode 怎么调度？”
“GPU / SM / HBM / parallelism 怎么分？”
```

但通常把：

- input resolution
- visual token count
- request compute demand

当作已经给定的 workload 属性，而不是 runtime 可以根据语义需求改变的执行旋钮。

即：**hardware adaptation 很强，但 semantic elasticity 不够。**

### SmartVL 是最危险的交叉近邻

SmartVL 已经证明：

> visual token allocation 与 LLM compute 不应该独立优化。

因此我们不能把“联合控制多个 model compute knobs”本身当 novelty。

我们的潜在新问题必须进一步推进到：

> **Can semantic compute allocation and multi-request hardware serving be optimized in one online control loop?**

即：

```text
request semantics
      +
live serving state
      |
      v
joint execution plan
      |
      +--> compute / fidelity configuration
      +--> batching / scheduling / resource allocation
```

截至当前检索，没有发现一篇代表性工作完整覆盖这一闭环；但这只是当前文献检索结论，不应当视为“绝对没人做过”。后续 literature review 必须继续查重。

---

## 6. 为什么这个问题值得做

2026 年的 LVLM efficient-inference survey 已经把：

- visual information shaping
- encoding / prefill / decoding 的 end-to-end interaction
- stage-disaggregated serving
- hardware-algorithm co-design

明确列为重要趋势。

因此我们现在的方向不是凭空拼接两个概念，而是踩在两个正在快速发展的研究线交叉处。

真正的研究价值不在“我们也做 pruning”，而在：

> **把 model-side semantic elasticity 暴露给 serving runtime，并让 runtime 与 GPU execution 共同利用这种 elasticity。**
