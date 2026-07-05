# Tokenization and Embeddings

Tokenization and embeddings turn raw text into the discrete IDs and dense vectors that a Transformer can process.

## Why It Matters

- Tokenization chooses the model's basic text units; modern LLMs usually use subword or byte-pair schemes rather than pure word-level tokenization.
- Tokenizer design affects multilingual efficiency, context-window consumption, special-token behavior, and embedding-table size.
- One-hot vectors are sparse and semantically uninformative; embeddings learn dense vectors where usage similarity can become geometric proximity.
- The embedding matrix has shape `vocab_size x d_model`, so vocabulary growth directly increases parameters and memory.
- Embeddings provide token identity and coarse semantic priors, while positional encoding provides order and attention layers produce contextualized meaning.
- Weight tying can share the input embedding matrix with the LM head, saving one large vocabulary-by-hidden-dimension matrix.
- Tokenizer normalization, pre-tokenization, special-token insertion, padding, and truncation must be treated as part of the model input contract because they affect masks and valid sequence lengths.

## Related Pages

- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- [Positional Encoding](positional-encoding.md)

## Sources

- [3.9 Tokenization与词嵌入](../sources/tokenization-and-word-embedding.md)
- [Transformer and Attention, Explained Plainly](../sources/transformer-and-attention-a-layman-guide.md)
- [Transformer Architecture Quick Start](../sources/transformer-architecture-quick-start.md)
- [探秘Transformer系列之（6）--- token](../sources/cnblogs-transformer-series-06-token.md)
- [探秘Transformer系列之（7）--- embedding](../sources/cnblogs-transformer-series-07-embedding.md)
