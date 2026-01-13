# ICS/SCADA Fingerprinter

> **Status:** Reference Implementation (Simulation Only)
> **Protocols:** Modbus/TCP, DNP3

## Overview
This module simulates the reconnaissance phase of a security audit for Critical Infrastructure (CI). It enumerates Industrial Control Systems (ICS) devices and calculates a hierarchical **Risk Score** based on simulated Common Vulnerabilities and Exposures (CVEs).

## Scientific Core
The system builds a **Network Topology Graph** $G(V, E)$ where nodes $V$ represent Master Terminal Units (MTUs) and Remote Terminal Units (RTUs). The connectivity risk is modeled as:

$$
R_{network} = \sum_{v \in V} R(v) \cdot C(v)
$$

Where $R(v)$ is the intrinsic vulnerability of a node and $C(v)$ is its centrality in the control graph.

## Visualization
The [ics_topology.png](./ics_topology.png) heatmap highlights critical nodes in the SCADA network, identifying single points of failure.

## Usage
```bash
python ics_scanner.py
```
