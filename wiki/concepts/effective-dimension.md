# Effective Dimension

Effective dimension is the participation ratio of a cluster's covariance spectrum: `d_eff = (tr Σ)² / tr(Σ²) = (Σ λ_i)² / Σ λ_i²`, where λ_i are the eigenvalues of the sample covariance. It measures the effective number of variance-bearing directions in a set of vectors.

## Why It Matters

- It is **scale-invariant** (multiplying Σ by a constant leaves it unchanged) and **weighted** (two large eigenvalues and one thousand small ones give `d_eff ≈ 2`, rather than about 1002, when the small eigenvalues contribute negligible total mass), making it a useful spectral summary for cluster shape in the manuscript's bound and evaluated setup.
- It is the exponential of the Rényi-2 entropy of the normalized eigenvalue spectrum.
- It appears as the critical exponent in the manuscript's formal Consolidation–Interference Duality lower bound, `ε_id ≥ 1 - c₁m(θ′/d̄)^(d_eff/2)`. The theorem's regime assumption conflicts with the empirical section's opposite tight-regime inequality, so the bound should not yet be read as predicting the reported empirical boundary.
- The consolidation manuscript attributes the global result—at least 99% of variance within about 16 effective dimensions across six encoder families—to a predecessor paper; its own experiments report local per-cluster `d_eff` often below 5.

## Related Pages

- [Embedding Memory Geometry](../topics/embedding-memory-geometry.md)
- [Product Quantization](product-quantization.md)

## Sources

- [The Geometry of Consolidation v6 (Paper)](../sources/geometry-of-consolidation-v6.md)
