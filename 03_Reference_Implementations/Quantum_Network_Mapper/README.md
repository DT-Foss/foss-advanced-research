# Quantum Network Mapper (QKD)

> **Status:** Reference Implementation (Simulation Only)
> **Protocols:** BB84, E91, ISO/IEC 23837

## Overview
This module models a **Quantum Key Distribution (QKD)** backbone, simulating the generation of secure key material across geographically separated Trusted Nodes. It accounts for photon loss in optical fiber to predict achievable Secret Key Rates (SKR).

## Scientific Core
The simulation implements the exponential decay of key rates due to fiber attenuation ($\alpha \approx 0.2 \text{ dB/km}$ at 1550nm):

$$
SKR(L) \approx R_{source} \cdot \eta_{det} \cdot 10^{-\frac{\alpha L}{10}}
$$

Where $L$ is the distance in kilometers. This demonstrates the "distance limit" of QKD without Quantum Repeaters.

## Visualization
The [qkd_topology.png](./qkd_topology.png) map shows the network graph with edges labeled by their specific key generation rates (kbps), illustrating the trade-off between security and distance.

## Usage
```bash
python qkd_mapper.py
```
