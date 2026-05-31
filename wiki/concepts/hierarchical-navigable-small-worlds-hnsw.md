# Hierarchical Navigable Small Worlds (HNSW)

HNSW is a graph-based Approximate Nearest Neighbor (ANN) algorithm that organizes vectors into a multi-layer navigable small-world graph. Higher layers have long edges for fast approximate search; lower layers have dense connections for accurate retrieval.

## Why It Matters

- HNSW typically offers the best recall-vs-speed trade-off among ANN algorithms at full precision, often reaching recall@95 with minimal search time.
- The multi-layer graph is inspired by skip-list data structures: search starts at the top layer (long jumps, coarse positioning) and descends layer by layer to the bottom (fine-grained neighbor traversal).
- Its main cost is memory — HNSW stores both the vectors and the graph edges, making it memory-intensive compared to Product Quantization or IVF approaches.
- At billion-scale, HNSW is often combined with PQ (HNSW+PQ) to reduce vector memory while keeping the graph structure.

## Related Pages

- [Vector Database and ANN Search](../topics/vector-database-and-ann-search.md)
- [Product Quantization](product-quantization.md)

## Sources

- [向量数据库 (Vector Database)](../sources/vector-database-overview.md)
