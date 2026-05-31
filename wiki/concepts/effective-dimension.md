# Effective Dimension

Effective dimension is the participation ratio of a cluster's covariance spectrum: `d_eff = (tr Σ)² / tr(Σ²) = (Σ λ_i)² / Σ λ_i²`, where λ_i are the eigenvalues of the sample covariance. It measures how many truly independent directions a set of vectors occupies.

## Why It Matters

- It is **scale-invariant** (multiplying Σ by a constant leaves it unchanged) and **weighted** (two large eigenvalues and one thousand small ones give d_eff ≈ 2, not ~1002) — making it the right spectral summary for cluster shape.
- It is the exponential of the Rényi-2 entropy of the normalized eigenvalue spectrum.
- It appears as the critical exponent in the Consolidation–Interference Duality bound: `(θ′/d̄)^(d_eff/2)` determines how much compression a cluster can tolerate before identity retrieval fails.
- Production sentence encoders concentrate ≥99% of variance in at most d_eff ≈ 16 effective dimensions globally; local per-cluster d_eff is often below 5.

## Related Pages

- [Embedding Memory Geometry](../topics/embedding-memory-geometry.md)
- [Product Quantization](product-quantization.md)

## Sources

- [The Geometry of Consolidation v6 (Paper)](../sources/geometry-of-consolidation-v6.md)
