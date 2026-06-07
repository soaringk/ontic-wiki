# Wiki Log

## [2026-06-08] lint | normalized source frontmatter YAML

- Audited the local wiki for orphan pages, broken links, stale claims, weak source connections, debate/synthesis duplication, and obvious duplicate pages.
- Found no broken internal links, no non-index orphan content pages, no duplicate titles or slugs, and no debate/synthesis duplication in the current inventory.
- Quoted seven source-page `title` frontmatter values containing colons so all wiki frontmatter parses as valid YAML.
- Refreshed `state/reports/latest_lint_report.md`; page counts remain 26 sources, 10 topics, 22 concepts, 0 debates, and 1 synthesis.
- Left `wiki/index.md` unchanged because page inventory and index summaries did not change.

## [2026-06-03] reindex | processed 2 duplicate Transformer markdown captures

- Processed pending source `raw/3.2 Transformer全貌及代码实现.md` and folded it into the canonical source page `Transformer Overview and Code Implementation`.
- Processed pending source `raw/🔥 Transformer架构：快速入门篇.md` and folded it into the canonical source page `Transformer Architecture Quick Start`.
- Updated `Transformer Architecture and Attention`, `Attention Mechanism`, `Parallelism in LLM Serving`, and `Prefill-Decode Disaggregation` with reinforced mask, QKV, tensor-parallel, and prefill/decode details.
- Rebuilt `wiki/index.md`; page counts remain 26 sources, 10 topics, 22 concepts, 0 debates, and 1 synthesis.
- Blocked sources: none. Unsupported sources: none.

## [2026-06-01] lint | repaired weak compression-topic connectivity

- Audited the local wiki for orphan pages, broken links, stale claims, weak source connections, debate/synthesis duplication, and obvious duplicate pages.
- Found no broken internal links, no link-orphan content pages, no duplicate titles, and no debate/synthesis duplication in the current inventory.
- Added `wiki/concepts/prediction-compression-equivalence.md` and linked it from `Language Modeling Is Compression` and `Compression and Language Models` to strengthen the previously one-source/one-topic compression cluster.
- Rebuilt `wiki/index.md` to include 22 concept pages.

## [2026-05-26] reindex | consolidated duplicate Geometry of Consolidation source page

- Removed duplicate source page `wiki/sources/geometry-of-consolidation-repo.md` because `raw/geometry-of-consolidation.md` is a companion GitHub README for the same work as `raw/GeometryOfConsolidation-v6.pdf`, not a separate durable wiki source.
- Folded the README's repository and reproduction notes into `wiki/sources/geometry-of-consolidation-v6.md` and added both source IDs to that canonical source page.
- Updated `wiki/index.md`, `Embedding Memory Geometry`, and `Effective Dimension` links. Current page counts are 26 sources, 10 topics, 21 concepts, 0 debates, and 1 synthesis.

## [2026-05-26] reindex | processed 5 pending sources (2 PDF, 3 markdown)

- Added source page for `raw/GeometryOfConsolidation-v6.pdf` (NeurIPS 2026 paper, published 2026-04-19) from extracted markdown sidecar.
- Added source page for `raw/geometry-of-consolidation.md` (GitHub repository README for the same paper).
- Added source page for `raw/Language Modeling Is Compression.pdf` (DeepMind paper on prediction-compression equivalence) from extracted markdown sidecar.
- Added source page for `raw/kv-cache-architecture-survey.md` (Chinese KVCache architecture survey from Zhihu).
- Added source page for `raw/vector-database.md` (Chinese vector database introduction, published 2023-07-15).
- Added topic page `Embedding Memory Geometry` with the Consolidation-Interference Duality, tight/spread regime analysis, and centroid near-optimality on real text.
- Added topic page `Compression and Language Models` covering prediction-compression equivalence, adjusted compression rates, and LLMs as general-purpose compressors.
- Added topic page `Vector Database and ANN Search` covering ANN algorithms (K-Means, PQ, HNSW, LSH), similarity measures, and filtering strategies.
- Added concept page `Effective Dimension` — participation ratio that governs the Consolidation-Interference Duality bound.
- Added concept page `Multi-head Latent Attention (MLA)` — DeepSeek's 96% KV dimension compression via low-rank latent caching.
- Added concept page `Product Quantization` — sub-vector codebook compression for billion-scale ANN search.
- Added concept page `Hierarchical Navigable Small Worlds (HNSW)` — multi-layer graph-based ANN with top-down search.
- Updated `Transformer Architecture and Attention` with sparse attention, linear attention, and cross-layer attention details.
- Updated `KV Cache in LLM Serving` with MLA, CSA+HCA, linear attention, CLA, FP8/FP4 quantization, and MoE implications.
- Updated `Attention Mechanism` with MLA, sparse attention, and linear attention variants.
- Updated `Context Caching in LLM Serving` with MLA and KVCache survey connections.
- Rebuilt `wiki/index.md` with 27 sources, 10 topics, 21 concepts, 0 debates, and 1 synthesis.
- Blocked sources: none. Unsupported sources: none.

## [2026-05-24] lint | refreshed wiki audit

- Audited the local wiki for broken links, orphan pages, stale claims, weak source connections, debate/synthesis duplication, and obvious duplicate pages.
- Found no broken internal links, no non-index orphan content pages, no obvious duplicate pages, no weak source-link candidates, and no debate/synthesis duplication in the current inventory.
- Refreshed `state/reports/latest_lint_report.md`; page counts are 22 sources, 7 topics, 17 concepts, 0 debates, and 1 synthesis.
- Left `wiki/index.md` unchanged because page inventory and index summaries did not change.

## [2026-05-24] reindex | processed 1 self-attention markdown source

- Added raw Defuddle extraction for `raw/self-attention-mechanism-deep-dive.md` with source publication date `2026-04-18`.
- Added source page for `raw/self-attention-mechanism-deep-dive.md`.
- Updated `Transformer Architecture and Attention`, `Attention Mechanism`, `KV Cache in LLM Serving`, and `Model Bandwidth Utilization` with self-attention, FlashAttention, and KV-cache compression details.
- Rebuilt `wiki/index.md`.

## [2026-05-20] reindex | processed 2 transformer markdown sources

- Added source page for `raw/transformer-architecture-quick-start.md`.
- Added source page for `raw/transformer-overview-and-code.md`.
- Updated `Transformer Architecture and Attention`, `Attention Mechanism`, and `KV Cache in LLM Serving` with infrastructure-oriented Transformer details.
- Rebuilt `wiki/index.md`.

Append-only timeline of ingest, synthesis, and lint activity.

## [2026-05-18] lint | refreshed wiki audit

- Audited the local wiki for broken links, orphan pages, stale claims, weak source connections, debate/synthesis duplication, and obvious duplicate pages.
- Found no broken internal links, no orphan content pages, no obvious duplicate pages, and no debate/synthesis duplication in the current inventory.
- Refreshed `state/reports/latest_lint_report.md`; page counts remained 19 sources, 7 topics, 17 concepts, 0 debates, and 1 synthesis.
- Left `wiki/index.md` unchanged because page inventory and index summaries did not change.

## [2026-05-11] lint | normalized source parser metadata

- Audited the local wiki for broken links, orphan pages, stale claims, weak source connections, debate/synthesis duplication, and obvious duplicate pages.
- Found no broken internal links, no orphan content pages, no obvious duplicate pages, and no debate/synthesis duplication in the current inventory.
- Added explicit `parser` frontmatter to non-video source pages: `direct` for Markdown sources and `mineru` for PDF sources.
- Left `wiki/index.md` unchanged because page inventory and index summaries did not change.

## [2026-05-06] reindex | processed 1 pending video source

- Added source page for `raw/videos/20260505_youtube_et3gjrsi-0_ai.video.md` using the generated ASR parser output at `state/extracted/raw-videos-20260505-youtube-et3gjrsi-0-ai-video-md-5fcb4c03ffd7/full.md`.
- Added topic page `AI-Native Learning` and concept page `Brain-Inspired AI`.
- Updated `Experiential AI` and `Utility Problem` with the source's claims about open-ended learning, grounded perception-action, and closed-dataset evaluation limits.
- Rebuilt `wiki/index.md`.
- Blocked sources: none. Unsupported sources: none.

## [2026-05-06] reindex | no pending sources; logged blocked video

- Processed pending sources from `state/reports/latest_reindex_report.md`: none.
- Left source, topic, and concept pages unchanged because no supported pending source was available to ingest.
- Rechecked `wiki/index.md`; page inventory and summaries were already current.
- Blocked source: `raw/videos/20260505_youtube_et3gjrsi-0_ai.video.md` (`source_type: video`, `parser: asr`) failed audio download because `yt-dlp` rejected audio format `webm`.
- Unsupported sources: none.

## [2026-04-25] reindex | processed 10 pending serving and transformer sources

- Added 10 source pages for the pending PDFs and markdown notes from the latest reindex report.
- Added topic pages `Disaggregated LLM Inference` and `Transformer Architecture and Attention`.
- Added concept pages for attention, context caching, integer-only quantization, iteration-level scheduling, PagedAttention, and prefill-decode disaggregation.
- Expanded `LLM Deployment and Capacity Planning`, `KV Cache in LLM Serving`, and `Parallelism in LLM Serving` with disaggregation, cache-management, and quantization links.
- Rebuilt `wiki/index.md`.
- Blocked sources: none. Unsupported sources: none.

## [2026-04-20] synthesis | polished AI conflict narrative and links

- Linked the AI conflict synthesis and debate notes to the relevant local source pages.
- Tightened wording around priors, algorithms, and reliability to avoid false binaries while preserving the substantive conflict.
- Refreshed the `Experiential AI` topic and `wiki/index.md` summary to match the revised synthesis.

## [2026-04-20] synthesis | tightened AI priors conflict analysis

- Revalidated `The Second Half` against `The Bitter Lesson`, `Welcome to the Era of Experience`, and `Two Lessons from ICLR 2025`.
- Updated the synthesis to separate hand-built human knowledge, learned language priors, and human-data ceilings.
- Tightened `Experiential AI` and related source pages around the live dispute over priors, algorithms, evaluation, reliability, and factual accuracy.
- Rebuilt `wiki/index.md`.

## [2026-04-20] reindex | processed 2 manually added markdown sources and validated the comparison

- Added source page for `raw/the-bitter-lesson.md`.
- Added source page for `raw/two-lessons-from-iclr-2025.md`.
- Updated `We're at AI's Halftime` and `Welcome to the Era of Experience` with stronger comparative open questions.
- Updated `Experiential AI` and `Utility Problem` to capture the dispute over priors, algorithms, evaluation, and reliability.
- Added synthesis page `AI Halftime vs Bitter Lesson and Era of Experience`.
- Rebuilt `wiki/index.md`.

## [2026-04-20] reindex | processed 1 pending markdown source

- Added source page for `raw/the-second-half.md`.
- Updated `Experiential AI` with the shift from benchmark hillclimbing toward evaluation-for-utility.
- Expanded `Streams of Experience` with sequential evaluation implications.
- Added concept page `Utility Problem`.
- Rebuilt `wiki/index.md`.

## [2026-04-13] reindex | processed 1 pending pdf source

- Added source page for `raw/The Era of Experience Paper.pdf` from its extracted markdown sidecar.
- Added topic page for experiential AI.
- Added concept pages for streams of experience and grounded rewards.
- Rebuilt `wiki/index.md`.

## [2026-04-11] reindex | processed 2 pending markdown sources

- Added source pages for `raw/CUDA_basic.md` and `raw/llm_model_calculation_cheat_sheet.md`.
- Added topic pages for CUDA programming and LLM deployment/capacity planning.
- Added concept pages for CUDA thread hierarchy, GPU memory hierarchy, KV cache, and LLM serving parallelism.
- Rebuilt `wiki/index.md`.

## [2026-04-12] lint | tightened wiki connectivity and refreshed index summaries

- Audited the local wiki for broken links, orphans, stale claims, duplicate topics, and weak source connections.
- Found no broken links or obvious duplicate pages in the current inventory.
- Added topic-to-concept and concept-to-concept links on concept pages to reduce orphan risk and strengthen navigation.
- Rebuilt `wiki/index.md` with compact one-line summaries for each tracked page.

## [2026-04-17] reindex | processed 2 markdown sources

- Added source page for `raw/LLM Inference Performance Engineering Best Practices.md`.
- Updated `LLM Deployment and Capacity Planning` with latency metrics, batching, memory-bandwidth, and scaling trade-offs.
- Expanded `KV Cache in LLM Serving` and `Parallelism in LLM Serving` with performance-engineering details.
- Added concept page for `Model Bandwidth Utilization`.
- Parsed `raw/private_credit_podcast.md` as a markdown source.
- Added source page `Private Credit Podcast`.
- Added topic page `Private Credit`.
- Added concept pages `Unitranche Loans` and `Rated Note Feeders`.
- Rebuilt `wiki/index.md`.

## [2026-04-20] lint | tightened topic summaries and source coverage

- Audited the local wiki for broken links, orphans, stale claims, duplicate pages, and weak source connections.
- Found no broken links, no literal orphan content pages, and no obvious duplicate pages in the current inventory.
- Strengthened `Experiential AI` with the source-backed claim that language priors and reasoning can act as a reusable internal action space.
- Strengthened `Private Credit` with the source-backed expansion into asset-based finance and AI-related infrastructure collateral.
- Rebuilt `wiki/index.md` to reflect the refreshed topic summaries.

## [2026-04-27] lint | tightened source-page reciprocal links

- Audited the local wiki for broken links, orphan pages, stale claims, duplicate pages, weak source connections, and debate/synthesis duplication.
- Found no broken internal links, no orphan content pages, no obvious duplicate pages, and no debate/synthesis duplication in the current inventory.
- Strengthened reciprocal navigation by adding missing source-to-topic and source-to-concept links on `Inference without Interference`, `Efficient Memory Management for Large Language Model Serving with PagedAttention`, and `MemServe`.
- Left `wiki/index.md` unchanged because page inventory and index summaries did not change.

## [2026-05-04] lint | normalized unknown publication metadata on source pages

- Audited the local wiki for broken links, orphan pages, stale claims, weak source connections, debate/synthesis duplication, and obvious duplicate pages.
- Found no broken internal links, no orphan content pages, no obvious duplicate pages, and no debate/synthesis duplication in the current inventory.
- Added explicit `published: unknown` frontmatter to source pages whose raw material was blank, missing, or ambiguous on publication time, so chronology-sensitive queries do not silently fall back to local maintenance dates.
- Left `wiki/index.md` unchanged because page inventory and index summaries did not change.
