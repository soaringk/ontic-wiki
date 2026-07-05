# Low-Rank Adaptation (LoRA)

LoRA is a parameter-efficient fine-tuning method that freezes a base model and trains low-rank update matrices attached to selected linear layers.

## Why It Matters

- LoRA represents a weight update as a low-rank product, usually written as `Delta W = B A`, so the trainable parameter count is much smaller than full fine-tuning.
- Freezing the base model reduces optimizer state, gradient memory, checkpoint size, and the operational cost of keeping multiple task-specific variants.
- At inference time, LoRA adapters can be merged into base weights or loaded dynamically as separate adapter state.
- Rank, alpha scaling, dropout, target modules, and calibration data determine the quality/cost trade-off.
- QLoRA combines low-bit base-model quantization with LoRA adapters, making low-memory fine-tuning practical but increasing sensitivity to quantization and adapter settings.

## Related Pages

- [LLM Quantization](llm-quantization.md)
- [Transformer Feed-Forward Network](transformer-feed-forward-network.md)
- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

## Sources

- [探秘Transformer系列之（22）--- LoRA](../sources/cnblogs-transformer-series-22-lora.md)
- [探秘Transformer系列之（36）--- 大模型量化方案](../sources/cnblogs-transformer-series-36-llm-quantization-methods.md)
