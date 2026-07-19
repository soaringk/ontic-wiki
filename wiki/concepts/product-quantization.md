# Product Quantization

Product Quantization (PQ) compresses high-dimensional vectors by splitting each vector into M sub-vectors of dimension d/M, quantizing each sub-vector independently using a learned codebook (typically K=256 centroids via k-means). The compressed representation is M log₂(K) bits per vector — e.g., 64 bits for M=8, K=256.

## Why It Matters

- PQ avoids the curse of dimensionality for quantization: on a 128-dim vector, naively learning a single codebook would require ~2^64 centroids for reasonable quality. PQ splits into 8×16-dim sub-vectors, needing only 8×256 = 2048 centroids.
- Distance computation becomes efficient: pre-compute sub-vector-to-centroid distance tables and sum M lookups per query.
- PQ sits at a key point on the accuracy/speed/memory Pareto frontier for large-scale similarity search and is a common component of production ANN systems.
- Optimized PQ (OPQ) adds a learned rotation to decorrelate sub-vectors before chunking, improving quantization quality.

## Related Pages

- [Vector Database and ANN Search](../topics/vector-database-and-ann-search.md)
- [Hierarchical Navigable Small Worlds (HNSW)](hierarchical-navigable-small-worlds-hnsw.md)
- [Effective Dimension](effective-dimension.md)

## Sources

- [向量数据库 (Vector Database)](../sources/vector-database-overview.md)
