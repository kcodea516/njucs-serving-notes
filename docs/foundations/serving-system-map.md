# LLM Serving 系统地图

原始学习记录。图中 prefill/decode 的瓶颈标签是常见情况，具体负载需通过 profiling 确认。

```
                         LLM Serving
                              │
             ┌────────────────┼────────────────┐
             │                │                │
          Request          Scheduling       Execution
             │                │                │
       prompt/output      batching          GPU kernels
       arrival rate       admission         CUDA
       SLO                priority          parallelism
             │                │                │
             └────────────────┼────────────────┘
                              │
                          Memory
                              │
                          KV Cache
                              │
                      memory allocation
                              │
                       PagedAttention
                              │
             ┌────────────────┴───────────────┐
             │                                │
          Prefill                          Decode
      compute-heavy                    memory-heavy
             │                                │
             └────────────────┬───────────────┘
                              │
                         Performance
                              │
                   TTFT / TPOT / Throughput
```
