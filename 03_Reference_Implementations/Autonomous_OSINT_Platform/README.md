# Autonomous OSINT Platform

> **Status:** Reference Implementation (Simulation Only)
> **Technique:** Graph Theory / Entity Resolution

## Overview
This module demonstrates an automated intelligence gathering pipeline that ingests unstructured data points and constructs a **Knowledge Graph**. It uses link analysis to identify non-obvious relationships between High-Value Targets (HVTs), shell companies, and assets.

## Scientific Core
The system utilizes **Force-Directed Graph Algorithms** (Fruchterman-Reingold) to cluster entities based on interaction density. Relationship strength $S_{rel}$ is calculated as:

$$
S_{rel}(u, v) = \sum_{p \in Paths(u,v)} \frac{1}{|p| \cdot \text{HopCount}(p)}
$$

This allows the system to identify "Bridges" in the criminal network that connect disparate clusters.

## Visualization
The [knowledge_graph.png](./knowledge_graph.png) visualization reveals the hidden ownership structure connecting two targets via a shared offshore entity and geotagged asset matches.

## Usage
```bash
python osint_graph_builder.py
```
