---
kind: source
title: "Language Modeling Is Compression"
slug: language-modeling-is-compression
source_ids:
  - raw-language-modeling-is-compression
status: active
raw_path: raw/Language Modeling Is Compression.pdf
source_type: pdf
parser: mineru
published: unknown
created: 2026-05-26
updated: 2026-05-26
---

# Summary

This DeepMind paper advocates for viewing language modeling through the lens of lossless compression. It shows that large foundation models are powerful general-purpose compressors: Chinchilla 70B, trained primarily on text, compresses ImageNet patches to 43.4% and LibriSpeech samples to 16.4% of their raw size, beating domain-specific compressors like PNG (58.5%) or FLAC (30.3%). It revisits scaling laws through adjusted compression rates (accounting for model size) and demonstrates that compressors like gzip can be used as conditional generative models.

# Key Claims

- **Prediction equals compression.** Arithmetic coding transforms any predictive model into a lossless compressor; conversely, any compressor defines a conditional distribution via coding lengths, enabling generation.
- **LLMs are general-purpose (raw) compressors.** Chinchilla 70B and Llama 2 7B, despite text-only training, achieve competitive raw compression rates on image and audio data — outperforming modality-specific codecs.
- **Adjusted compression rate reveals optimal model size.** When model parameters are counted in the compressed output, the adjusted compression rate creates a U-shaped curve with dataset size: scaling beyond a critical point worsens compression because parameter overhead dominates. Each dataset has an optimal model size.
- **Tokenization is pre-compression.** Tokenizers compress the raw byte stream before the model sees it. Larger vocabularies pack more information per token but make the prediction task harder; for large models, simpler tokenizers (e.g., ASCII) often achieve better raw compression.
- **In-context compression.** Foundation models rely on in-context learning to adapt their compression within a short context window, unlike classical compressors which rely on long context windows and small programs.

# Why It Matters

This paper connects two fields — information theory and large language models — through the rigorous equivalence of prediction and compression. It provides practical insights for model scaling (optimal model size depends on dataset size), tokenization (simpler is better for raw compression), and the cross-modal generalization capabilities of LLMs.

# Connections

- Topic: [Compression and Language Models](../topics/compression-and-language-models.md)
- Concept: [Prediction-Compression Equivalence](../concepts/prediction-compression-equivalence.md)

# Open Questions

- The paper's adjusted compression rate penalizes model size in a two-part code; prequential (online) coding would give a different picture for overparameterized models.
- The generative samples from compression-based models are still qualitatively poor compared to dedicated generative models.
