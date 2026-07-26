# Product Quantization

Product Quantization (PQ) compresses high-dimensional vectors by splitting each vector into sub-vectors and quantizing each part independently with a learned codebook.

## Why It Matters

- Factorizing vector quantization into smaller codebooks mitigates codebook growth as vector dimension increases.
- The compact codes reduce memory use at the cost of approximate distances and some retrieval accuracy.
- PQ occupies one point on the workload-dependent accuracy, speed, and memory trade-off for ANN search.

## Related Pages

- [Vector Database and ANN Search](../topics/vector-database-and-ann-search.md)
- [Hierarchical Navigable Small Worlds (HNSW)](hierarchical-navigable-small-worlds-hnsw.md)
- [Effective Dimension](effective-dimension.md)

## Sources

- [向量数据库 (Vector Database)](../sources/vector-database-overview.md)
