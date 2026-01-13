# Synthetic Data Factory

> **Status:** Reference Implementation (Simulation Only)
> **Technique:** Automated Curriculum Learning

## Overview
This module simulates the industrial-scale production of training data for Large Language Models (LLMs). It implements a multi-stage filtering pipeline to convert noisy "Raw Web" data into "Supervised Fine-Tuning (SFT)" quality datasets.

## Scientific Core
The pipeline optimizes for the **Signal-to-Noise Ratio (SNR)**. The utility function $U(D)$ of a dataset $D$ is defined not by size, but by the density of high-complexity tokens:

$$
U(D) = \sum_{x \in D} Q(x) \cdot \log(\text{Diversity}(x))
$$

Where $Q(x)$ is the quality score from a helper reward model.

## Visualization
The [data_pipeline.png](./data_pipeline.png) funnel chart illustrates the drastic filtering process (1000B raw tokens $\rightarrow$ 12B gold tokens) required to achieve 99.5% quality scores for sovereign model training.

## Usage
```bash
python synthetic_pipeline.py
```
