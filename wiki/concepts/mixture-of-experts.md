# Mixture of Experts

Mixture of Experts (MoE) expands Transformer capacity by replacing some dense per-token FFN work with a router that sends each token to a small subset of expert networks.

## Why It Matters

- MoE increases total parameter count without activating all parameters for every token.
- The router/gate chooses top-k experts per token, so quality depends on both expert capacity and routing behavior.
- Sparse expert activation can reduce per-token FLOPs relative to an equally large dense model, but it introduces load balancing and communication problems.
- Expert parallelism is distinct from tensor parallelism: tokens must be dispatched to the devices that host selected experts, often creating all-to-all communication.
- Shared experts, fine-grained experts, auxiliary load-balancing losses, and capacity factors are common tools for reducing routing instability.
- In serving, MoE changes FFN compute and communication patterns, but attention, KV cache, and autoregressive scheduling remain active constraints.

## Related Pages

- [Transformer Feed-Forward Network](transformer-feed-forward-network.md)
- [Parallelism in LLM Serving](parallelism-in-llm-serving.md)
- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

## Sources

- [探秘Transformer系列之（21）--- MoE](../sources/cnblogs-transformer-series-21-moe.md)
- [探秘Transformer系列之（29）--- DeepSeek MoE](../sources/cnblogs-transformer-series-29-deepseek-moe.md)
- [3.4 Transformer前馈网络FFN深入理解](../sources/transformer-ffn-deep-dive.md)
