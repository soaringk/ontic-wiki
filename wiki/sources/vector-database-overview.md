---
kind: source
title: "向量数据库 (Vector Database)"
slug: vector-database-overview
source_ids:
  - raw-vector-database
status: active
raw_path: raw/vector-database.md
source_type: markdown
parser: direct
published: 2023-07-15
created: 2026-05-26
updated: 2026-05-26
---

# Summary

A Chinese introductory article on vector databases, covering their motivation (GPT's token limits, semantic search), Vector Embeddings, similarity search algorithms (K-Means + Faiss, Product Quantization, HNSW, LSH), similarity measurement (Euclidean, cosine, dot product), filtering strategies, and practical database selection. Published July 2023.

# Key Claims

- **Vector databases solve GPT's context-window problem.** By pre-embedding documents and retrieving only relevant chunks at query time, vector databases drastically reduce token costs and bypass context-length limits.
- **Vector Embeddings encode semantic features.** AI models (text-embedding-ada-002, CLIP, wav2vec2) produce high-dimensional vectors that capture latent semantics — similar inputs map to nearby points in embedding space.
- **ANN algorithms trade accuracy for speed.** Clustering (K-Means with Faiss), Product Quantization (sub-vector compression), HNSW (multi-layer graph), and LSH (locality-sensitive hashing) each occupy different points on the accuracy/speed/memory Pareto frontier.
- **Product Quantization.** Sub-divides vectors into sub-vectors, quantizes each independently, and uses a codebook; dramatically reduces memory at the cost of some accuracy.
- **HNSW.** Hierarchical navigable small-world graphs combine fast approximate search (top-level long jumps) with accurate results (bottom-level dense connections) — a classic space-for-speed trade-off.
- **Filtering adds complexity.** Pre-filtering (search before filter) may miss results; post-filtering (filter after search) may waste computation. Both are active research areas.

# Why It Matters

Vector databases are a core infrastructure layer for retrieval-augmented generation (RAG), semantic search, and AI-powered applications. This article provides a practitioner-oriented introduction to the core algorithms (K-Means, PQ, HNSW, LSH) and practical selection criteria (distributed support, access control, API/SDK design) for choosing a vector database.

# Connections

- Topic: [Vector Database and ANN Search](../topics/vector-database-and-ann-search.md)
- Concept: [Product Quantization](../concepts/product-quantization.md)
- Concept: [Hierarchical Navigable Small Worlds (HNSW)](../concepts/hierarchical-navigable-small-worlds-hnsw.md)

# Open Questions

- The article was published in July 2023; the field has evolved rapidly (new databases, new ANN algorithms). The specific product comparisons and GitHub stars are likely outdated.
- Practical trade-offs between dedicated vector databases (Milvus, Qdrant, Weaviate, Pinecone) and extension-based approaches (pgvector, Redis) depend heavily on workload characteristics not covered here.
