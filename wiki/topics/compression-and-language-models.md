# Compression and Language Models

The equivalence of prediction and lossless compression — Shannon's source coding theorem links maximizing log-likelihood to minimizing compressed bit-length. Large language models, as powerful predictors, are also powerful compressors. This topic covers the theoretical connection, the empirical capabilities of LLMs as cross-modal compressors, and the practical insights that the compression viewpoint provides for scaling laws, tokenization, and in-context learning.

## Core Ideas

- Arithmetic coding transforms any probabilistic model into a lossless compressor with near-optimal coding length. Maximizing log-likelihood is equivalent to minimizing compression rate.
- Conversely, any compressor defines a predictive distribution via coding-length differences, enabling compression-based generation (though quality is usually poor).
- **Adjusted compression rate** = (model size + compressed data size) / raw data size. When model parameters are counted, each dataset has an optimal model size; scaling beyond this point worsens compression because parameter overhead dominates. This gives a compression-grounded perspective on scaling laws.
- **LLMs as general-purpose compressors.** Chinchilla 70B, trained on text, compresses ImageNet patches to 43.4% and LibriSpeech to 16.4% — beating domain-specific codecs. This is achieved through in-context learning, not cross-modal training.
- **In-context compression.** Foundation models adapt within a short context window via in-context learning; classical compressors (gzip, LZMA2) rely on long context windows and small programs. These represent two fundamentally different compression strategies.
- **Tokenization as pre-compression.** Tokenizers are lossless pre-compressors; larger vocabularies increase information density per token but make prediction harder. For raw compression, simpler tokenizers (ASCII, BPE-1K) often outperform larger ones.

## Related Concepts

- [Prediction-Compression Equivalence](../concepts/prediction-compression-equivalence.md)
- Information theory, Shannon entropy, cross-entropy
- Arithmetic coding, Huffman coding
- Kolmogorov complexity, Solomonoff induction

## Sources

- [Language Modeling Is Compression](../sources/language-modeling-is-compression.md)
