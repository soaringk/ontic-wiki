# Prediction-Compression Equivalence

Prediction-compression equivalence is the information-theoretic link between probabilistic prediction and lossless coding: a model that assigns high probability to the next symbol can be turned into a compressor, and a compressor's code lengths can be read as implicit predictive probabilities.

## Why It Matters

- Arithmetic coding converts predictive likelihoods into near-optimal code lengths, so minimizing cross-entropy is equivalent to improving compression rate.
- The equivalence explains why language-modeling loss is not just a text benchmark: it measures how well a model captures regularities in the data stream.
- It also lets classical compressors act as conditional generative models by comparing code lengths, although their samples are usually weaker than modern neural generators.
- In the language-modeling-as-compression view, model size matters because the compressed representation can be treated as a two-part code: model parameters plus encoded data.

## Related Pages

- [Compression and Language Models](../topics/compression-and-language-models.md)

## Sources

- [Language Modeling Is Compression](../sources/language-modeling-is-compression.md)
