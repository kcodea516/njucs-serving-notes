# 实践计划（暂缓，待更新）

以下保留原 8 周计划，待结合当前调度主线更新。

|周|做什么|产出|
|---|---|---|
|1–2|读 A、B 组；在 A800 上跑通 vLLM 和 SGLang，部署 Qwen2.5-VL-7B 和 InternVL|能用 `benchmark_serving` 测 TTFT、TPOT、吞吐|
|3–4|**做 profiling**：改变图片数、分辨率、视频帧数、请求率、图文混合比例，测各阶段耗时（ViT encode / prefill / decode），以及 KV 占用和排队时间。工具用 `torch.profiler` 和 Nsight Systems|一份带图的 profiling 报告，**拿去给宦老师和师兄看**|
|5–6|读 E、F 组，复现 FastV（或 VisionZip）以及 EPD（[代码在这里](https://github.com/vbdi/epdserve)）|复现数据，并和论文报告的数字对比|
|7–8|拿 profiling 报告对照论文对比表，挑 2–3 个"数据显示有问题、现有工作没覆盖"的点，每个做一个最小验证实验|1 个立得住的 idea，带 motivation 图|

**和 GPT 的正确分工：** 让它帮你读源码、写 profiling 脚本、查相关工作有没有撞车、挑你的论证漏洞。**问题本身要由你的数据来定**，不要让它来想 idea。

**开源贡献：** 在 profiling 过程中，你大概率会碰到 vLLM 多模态部分的 bug 或性能问题。顺手去提 issue 或 PR，这是最自然的开源入口。
