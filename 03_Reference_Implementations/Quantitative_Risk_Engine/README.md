# Quantitative Risk Engine (VaR/CVaR)

> **Status:** Reference Implementation (Simulation Only)
> **Methodology:** Monte Carlo Simulation (N=10,000)

## Overview
This module calculates portfolio risk metrics under stress conditions. It uses **Cholesky Decomposition** to apply stress-scenario correlations to random walk simulations, allowing for the calculation of **Value at Risk (VaR)** and **Expected Shortfall (CVaR)**.

## Scientific Core
Correlated asset returns are generated using the matrix decomposition equation:

$$
\mathbf{R}_{corr} = \mathbf{L} \cdot \mathbf{R}_{uncorr}
$$

Where $\mathbf{L}$ is the lower triangular matrix from the Cholesky decomposition of the correlation matrix $\Sigma$ ($\Sigma = LL^T$).
VaR is then defined as the quantile of the loss distribution:

$$
VaR_{\alpha}(X) = - \inf \{ x \in \mathbb{R} : P(X \le x) \ge \alpha \}
$$

## Visualization
The [risk_heatmap.png](./risk_heatmap.png) dashboard displays:
1.  **Correlation Matrix:** Inter-asset dependencies during stress events.
2.  **Loss Distribution:** Histogram of PnL outcomes with VaR cutoffs.
3.  **Efficient Frontier:** Risk/Return optimization landscape.

## Usage
```bash
python risk_engine_var.py
```
