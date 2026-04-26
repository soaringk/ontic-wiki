# Iteration-Level Scheduling

Iteration-level scheduling means the serving system reconsiders the active batch after each generation step instead of locking a request set for the full lifetime of a request.

## Why It Matters

- Finished requests can leave immediately instead of waiting for the slowest peer in the batch.
- New arrivals can start after one iteration rather than after an entire batch drains.
- It enables continuous batching and other fine-grained policies that fit autoregressive generation.
- It makes queueing behavior depend on token steps, not just request count.

## Limits

- Fine-grained scheduling still needs compatible memory management and batch composition rules.
- It reduces one kind of interference but does not itself solve cross-phase contention or decode-side resource hotspots.

## Related Pages

- [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- [PagedAttention](pagedattention.md)

## Sources

- [Orca: A Distributed Serving System for Transformer-Based Generative Models](../sources/orca-a-distributed-serving-system-for-transformer-based-generative-models.md)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
- [How to Generate Tokens Faster: A vLLM Performance Model](../sources/vllm-performance-model.md)
