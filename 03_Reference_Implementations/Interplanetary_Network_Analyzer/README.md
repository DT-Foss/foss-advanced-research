# Interplanetary Network Analyzer (CCSDS/DTN)

> **Status:** Reference Implementation (Simulation Only)
> **Compliance:** RFC 9171 (Bundle Protocol v7)

## Overview
This module simulates the performance of a **Delay Tolerant Network (DTN)** link between Earth and Mars. Unlike terrestrial TCP/IP, which fails under high latency (>500ms), DTN uses a store-and-forward mechanism to handle disruptions caused by orbital mechanics and planetary occultation.

## Scientific Core
The simulation models the **Shannon Capacity** of the Deep Space Network (DSN) link under changing signal-to-noise ratios (SNR) governed by the inverse-square law of distance:

$$
C = B \cdot \log_2(1 + \frac{P_{rx}}{N_0 B})
$$

Where distance $r$ varies according to:

$$
r(t) \approx 1.5 + \sin(\omega t) \text{ (Au)}
$$

## Visualization
The generated plot [dtn_link_analysis.png](./dtn_link_analysis.png) demonstrates:
1.  **Link Capacity:** Fluctuating bandwidth based on orbital distance.
2.  **Occultation:** Periods of zero throughput when line-of-sight is lost.
3.  **Light Time Latency:** Varying communication delay (3-22 minutes).

## Usage
```bash
python dtn_analyzer.py
```
