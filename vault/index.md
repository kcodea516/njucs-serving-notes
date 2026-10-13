---
aliases:
- 学习总路线
---

# Serving 论文阅读路线

原有 A–F 分组与学习安排。新增研读材料见 [A1 研读清单](papers/a-inference-foundations/efficient-inference-survey/reading-list.md)，按实际瓶颈选择候选方向。

链接都是 arXiv 的 PDF。2025 年以后的论文我联网核实过，较早的经典论文是凭记忆给的编号。打不开的话，用标题搜一下就能找到。

### A. 推理基础：先搞清楚瓶颈在哪

|#|论文|链接|重点看什么|
|---|---|---|---|
|1|A Survey on Efficient Inference for LLMs|[2404.14294](https://arxiv.org/pdf/2404.14294)|当地图用，建立分类框架|
|2|LLM Inference Unveiled: Survey and Roofline Model Insights|[2402.16363](https://arxiv.org/pdf/2402.16363)|**Roofline 分析**，搞懂为什么 prefill 受算力限制、decode 受访存限制|
|3|FlashAttention|[2205.14135](https://arxiv.org/pdf/2205.14135)|IO-aware 的思路，理解访存才是瓶颈|
|4|FlashAttention-2|[2307.08691](https://arxiv.org/pdf/2307.08691)|并行划分|

### B. Serving 系统主线：调度、内存、PD 分离

|#|论文|链接|
|---|---|---|
|5|Orca（continuous batching 的起源）|[OSDI'22 PDF](https://www.usenix.org/system/files/osdi22-yu.pdf)|
|6|vLLM / PagedAttention|[2309.06180](https://arxiv.org/pdf/2309.06180)|
|7|SGLang / RadixAttention|[2312.07104](https://arxiv.org/pdf/2312.07104)|
|8|Sarathi-Serve（chunked prefill）|[2403.02310](https://arxiv.org/pdf/2403.02310)|
|9|DistServe（PD 分离、goodput 的概念）|[2401.09670](https://arxiv.org/pdf/2401.09670)|
|10|Splitwise|[2311.18677](https://arxiv.org/pdf/2311.18677)|
|11|Mooncake（Kimi 的 KV 中心架构）|[2407.00079](https://arxiv.org/pdf/2407.00079)|
|12|Llumnix（请求迁移、负载均衡）|[2406.03243](https://arxiv.org/pdf/2406.03243)|

### C. 算法层加速：KV cache、量化、投机解码

|#|论文|链接|
|---|---|---|
|13|H2O（KV eviction）|[2306.14048](https://arxiv.org/pdf/2306.14048)|
|14|StreamingLLM（attention sink）|[2309.17453](https://arxiv.org/pdf/2309.17453)|
|15|SnapKV|[2404.14469](https://arxiv.org/pdf/2404.14469)|
|16|KIVI（KV 量化）|[2402.02750](https://arxiv.org/pdf/2402.02750)|
|17|AWQ（权重量化）|[2306.00978](https://arxiv.org/pdf/2306.00978)|
|18|Speculative Decoding（Leviathan et al.）|[2211.17192](https://arxiv.org/pdf/2211.17192)|
|19|EAGLE|[2401.15077](https://arxiv.org/pdf/2401.15077)|
|20|MInference（长上下文稀疏 prefill）|[2407.02490](https://arxiv.org/pdf/2407.02490)|

### D. 多模态模型本身：知道 token 是怎么来的

|#|论文|链接|
|---|---|---|
|21|Qwen2-VL（动态分辨率、M-RoPE）|[2409.12191](https://arxiv.org/pdf/2409.12191)|
|22|InternVL 1.5（动态切 tile）|[2404.16821](https://arxiv.org/pdf/2404.16821)|

### E. 视觉 token 压缩（算法层，和你最对口）

|#|论文|链接|
|---|---|---|
|23|FastV（"一张图值半个 token"）|[2403.06764](https://arxiv.org/pdf/2403.06764)|
|24|SparseVLM|[2410.04417](https://arxiv.org/pdf/2410.04417)|
|25|VisionZip|[2412.04467](https://arxiv.org/pdf/2412.04467)|
|26|TopV（兼容 FlashAttention 的剪枝）|[2503.18278](https://arxiv.org/pdf/2503.18278)|
|27|VLM 高效推理综述|[2603.27960](https://arxiv.org/pdf/2603.27960)|

### F. 多模态 serving 系统（你的主战场）

|#|论文|链接|
|---|---|---|
|28|EPD Disaggregation（ICML'25，Encode/Prefill/Decode 三段分离）|[2501.05460](https://arxiv.org/pdf/2501.05460)|
|29|ModServe（模态感知、按阶段分离）|[2502.00937](https://arxiv.org/pdf/2502.00937)|
|30|HydraInfer（混合 EPD，按负载动态选择拓扑）|[2505.12658](https://arxiv.org/pdf/2505.12658)|
|+|ElasticMM|[2507.10069](https://arxiv.org/pdf/2507.10069)|
|+|TCM-Serve（模态感知调度）|[2603.26498](https://arxiv.org/pdf/2603.26498)|
|+|vLLM-Omni（any-to-any 模型的分离式 serving）|[2602.02204](https://arxiv.org/pdf/2602.02204)|

**关于你之前的 idea：** HydraInfer 和 ElasticMM 做的正是"根据负载动态调整"，只不过它们调整的是资源和拓扑，不是回答质量。你那个"高负载时降成本回答"的想法，可以理解为把 **E 组（token 压缩）和 F 组（负载感知调度）结合**：负载高的时候，对部分请求自适应地加大视觉 token 压缩率，用一点点精度换 SLO。先查有没有人做过，再测数据，看 trade-off 曲线是否成立。这个想法比之前具体多了。

---

# 二、怎么读：每篇写一页笔记

**每篇论文都回答这 8 个问题：**

1. **问题**：一句话说清楚它解决什么瓶颈。
2. **动机数据**：Motivation 部分的那张图是什么？这个问题是用什么数据证明存在的？**这一点最重要，你以后写论文也要从这里起步。**
3. **关键洞察**：方案背后的那个观察是什么（比如"视觉 token 在第 2 层之后的注意力很稀疏"）？
4. **核心假设**：方案在什么前提下才成立？
5. **实验设置**：用了哪些模型、数据集、负载 trace、baseline、指标（TTFT/TPOT/goodput/SLO attainment）？
6. **收益从哪来**：Ablation 里哪个组件贡献最大？
7. **局限**：作者承认了什么？没承认的又是什么？（比如只测了单图、只测了 7B 模型、负载是合成的）
8. **迁移**：这个假设在多模态 / 视频 / 多图 / 高负载下还成立吗？

**读的时候要特别留意：**

- **Baseline 是否公平**：是不是拿旧版 vLLM 当对手，有没有开 chunked prefill 和 prefix caching？很多论文的收益就藏在这里。
- **负载是否真实**：合成的泊松到达，还是真实 trace？
- **指标是否挑过**：只报吞吐不报尾延迟，只报延迟不报精度，都要打问号。
- **论文之间的矛盾**：比如 EPD 自己承认"只看吞吐不看 SLO 时，不分离反而更好"。这种矛盾的地方，往往就是新论文的切入点。

**读的方法：**

- A、B 组精读，要配合 vLLM 源码一起看（`vllm/core/scheduler.py`、`vllm/v1/` 下的调度和 KV 管理部分）。
- E、F 组精读，并且**每组至少复现一篇**。
- 维护一张对比表：每行一篇论文，列是"问题 / 假设 / 场景 / 指标 / 局限"。读到第 20 篇左右，表里的空白格子就是你的候选 idea。

---

# 三、怎么实践：前 8 周的计划

|周|做什么|产出|
|---|---|---|
|1–2|读 A、B 组；在 A800 上跑通 vLLM 和 SGLang，部署 Qwen2.5-VL-7B 和 InternVL|能用 `benchmark_serving` 测 TTFT、TPOT、吞吐|
|3–4|**做 profiling**：改变图片数、分辨率、视频帧数、请求率、图文混合比例，测各阶段耗时（ViT encode / prefill / decode），以及 KV 占用和排队时间。工具用 `torch.profiler` 和 Nsight Systems|一份带图的 profiling 报告，**拿去给宦老师和师兄看**|
|5–6|读 E、F 组，复现 FastV（或 VisionZip）以及 EPD（[代码在这里](https://github.com/vbdi/epdserve)）|复现数据，并和论文报告的数字对比|
|7–8|拿 profiling 报告对照论文对比表，挑 2–3 个"数据显示有问题、现有工作没覆盖"的点，每个做一个最小验证实验|1 个立得住的 idea，带 motivation 图|

**和 GPT 的正确分工：** 让它帮你读源码、写 profiling 脚本、查相关工作有没有撞车、挑你的论证漏洞。**问题本身要由你的数据来定**，不要让它来想 idea。

**开源贡献：** 在 profiling 过程中，你大概率会碰到 vLLM 多模态部分的 bug 或性能问题。顺手去提 issue 或 PR，这是最自然的开源入口。
