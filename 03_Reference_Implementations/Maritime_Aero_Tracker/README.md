# Maritime & Aero Surveillance Tracker

> **Status:** Reference Implementation (Simulation Only)
> **Protocols:** ADS-B (1090 MHz), VDES/AIS (162 MHz)

## Overview
This module simulates a multi-domain passive surveillance system that tracks transponder signals from aircraft and maritime vessels. It implements a physics-based **RF Signal Propagation Model** to determine detection probabilities based on the Friis Transmission Equation.

## Scientific Core
The system calculates the **Received Signal Strength (RSS)** $P_r$ for each target to determine if it exceeds the receiver sensitivity threshold ($S_{min} \approx -105 \text{ dBm}$).

### Free Space Path Loss Model
$$
P_r = P_t + G_t + G_r - 20\log_{10}(d) - 20\log_{10}(f) - 32.44 + \mathcal{N}(0, \sigma)
$$

Where:
*   $P_t$: Transmitter Power (51 dBm for Aircraft, 41 dBm for Vessels)
*   $G_t, G_r$: Antenna Gains
*   $d$: Distance in km
*   $f$: Frequency in MHz (1090 vs 162)
*   $\mathcal{N}$: Stochastic noise (fading)

## Visualization
The generated polar plot [surveillance_plot.png](./surveillance_plot.png) visualizes the tactical situation display, color-coding targets by RSS to indicate signal integrity and proximity.

## Usage
```bash
python tracker_sim.py
```
