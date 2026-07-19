# Vector Database and ANN Search

Vector databases store high-dimensional embedding vectors and support efficient similarity search. They are a core infrastructure layer for retrieval-augmented generation (RAG), semantic search, recommendation systems, and many AI applications requiring long-term memory over unstructured data. Approximate Nearest Neighbor (ANN) algorithms form the computational heart of vector databases.

## Core Ideas

- **Vector Embeddings.** AI models map unstructured data (text, images, audio) to high-dimensional vectors that encode semantic features. Similar inputs map to nearby points in embedding space.
- **ANN algorithms approximate exact search.** Exact-search cost grows with corpus size; ANN methods trade some recall for lower search cost using clustering, quantization, graphs, or hashing.
- **Key algorithm families:**
  - **Clustering-based (K-Means, Faiss IVF).** Partition the space into Voronoi cells; search only the nearest cells. Simple and effective but risks missing boundary neighbors.
  - **Product Quantization (PQ).** Sub-divide each vector into sub-vectors; quantize each sub-vector independently using learned codebooks. Dramatically reduces memory footprint with moderate accuracy loss.
  - **Graph-based (HNSW).** Build a hierarchical navigable small-world graph; greedy search from top-level (long jumps) to bottom-level (dense neighbors). High search accuracy at the cost of larger memory for graph structure.
  - **Hashing-based (LSH).** Use locality-sensitive hash functions that map similar vectors to the same bucket with high probability. Fast but often lower accuracy than graph-based methods.
- **Similarity measures.** Euclidean distance (absolute magnitude matters), cosine similarity (direction only, length-invariant), and dot product (magnitude-and-direction) are the three standard options, each suited to different data and model characteristics.
- **Filtering.** Real applications combine vector search with metadata filters. Pre-filtering vs. post-filtering presents a fundamental trade-off between search scope and result completeness.
- **Production considerations.** Distributed deployment, sharding by vector similarity, replication for availability, access control, monitoring, backup, and API/SDK design can all matter beyond the core ANN algorithm.

## Sub-areas

- **ANN algorithms.** IVF, PQ, HNSW, LSH, and their many variants — each occupying a different point on the accuracy / speed / memory Pareto frontier.
- **Vector compression.** Quantization reduces per-vector storage from 4d bytes (FP32) to compact codes. Product Quantization is a widely used approach.

## Related Concepts

- [Product Quantization](../concepts/product-quantization.md)
- [Hierarchical Navigable Small Worlds (HNSW)](../concepts/hierarchical-navigable-small-worlds-hnsw.md)

## Sources

- [向量数据库 (Vector Database)](../sources/vector-database-overview.md)
