# Algorithmic Arbitrage Engine

> **Status:** Reference Implementation (Simulation Only)
> **Model:** Geometric Brownian Motion (GBM) + Monte Carlo

## Overview
This module implements a **High-Frequency Trading (HFT)** logic that exploits latency differentials between market venues. It detects price discrepancies caused by signal propagation delays and executes theoretical trades.

## Scientific Core
Asset prices are modeled using Stochastic Differential Equations (GBM):

$$
dS_t = \mu S_t dt + \sigma S_t dW_t
$$

Risk management is enforced via **Value at Risk (VaR)** calculation using Monte Carlo simulation to ensure the probability of ruin remains below the threshold $\alpha = 0.05$.

## Visualization
The [arbitrage_risk.png](./arbitrage_risk.png) dashboard displays:
1.  **Microstructure:** The time-lag between Exchange A and Exchange B.
2.  **Risk Profile:** A probability distribution of Daily PnL with the 95% VaR threshold marked.

## Usage
```bash
python arbitrage_engine.py
```
