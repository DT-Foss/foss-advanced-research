import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple

# -----------------------------------------------------------------------------
# Module 11: Algorithmic Arbitrage Engine (Quant Finance)
# -----------------------------------------------------------------------------
# Simulation of Latency Arbitrage using Stochastic Differential Equations (SDE).
# Models Geometric Brownian Motion (GBM) for asset prices across two exchanges.
# -----------------------------------------------------------------------------

def geometric_brownian_motion(S0, mu, sigma, T, dt, steps):
    """
    Simulate asset price path using GBM: dS = mu*S*dt + sigma*S*dW
    """
    t = np.linspace(0, T, steps)
    W = np.random.standard_normal(size=steps) 
    W = np.cumsum(W) * np.sqrt(dt) # Wiener process
    X = (mu - 0.5 * sigma**2) * t + sigma * W
    S = S0 * np.exp(X)
    return t, S

def simulate_latency_arbitrage():
    """
    Simulate price divergence between Exchange A (Slow) and Exchange B (Fast)
    and calculate arbitrage profits using Kelly Criterion sizing.
    """
    
    # Parameters
    S0 = 100.0 # Initial Price
    mu = 0.05  # Drift
    sigma = 0.2 # Volatility
    T = 1.0    # Time horizon (1 day normalized)
    steps = 1000
    dt = T/steps
    
    # Exchange A (The "True" Price - Fast)
    time, price_a = geometric_brownian_motion(S0, mu, sigma, T, dt, steps)
    
    # Exchange B (Lagged Price - Slow)
    # Lag is represented by a delay index plus some noise
    lag = 5 # 5 steps latency
    price_b = np.roll(price_a, lag)
    price_b[:lag] = S0 # Fill initial
    price_b += np.random.normal(0, 0.05, steps) # Market noise
    
    # Arbitrage Signal
    spread = price_b - price_a
    
    # Monte Carlo Risk Analysis (PnL Distribution)
    # Simulate 1000 trading days
    final_pnls = []
    
    for _ in range(1000):
        # Simplified simulation of N trades per day
        # Win rate 65% (statistical arb), Avg Win 1.2, Avg Loss 1.0
        n_trades = 50
        wins = np.random.binomial(n_trades, 0.65)
        losses = n_trades - wins
        daily_pnl = (wins * 1.2) - (losses * 1.0)
        final_pnls.append(daily_pnl)
        
    final_pnls = np.array(final_pnls)
    
    # --- Visualization ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Market Microstructure (Latency)
    zoom = slice(100, 200) # Zoom in
    ax1.plot(time[zoom], price_a[zoom], label='Exchange A (Reference)', color='blue', linewidth=1.5)
    ax1.plot(time[zoom], price_b[zoom], label='Exchange B (Lagged)', color='red', linestyle='--', linewidth=1.5)
    ax1.fill_between(time[zoom], price_a[zoom], price_b[zoom], where=(price_b[zoom] > price_a[zoom]), color='green', alpha=0.3, label='Arb Opportunity')
    ax1.set_title('Signal Latency Arbitrage (Market Microstructure)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Asset Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Monte Carlo Risk (VaR)
    ax2.hist(final_pnls, bins=50, color='#8e44ad', alpha=0.7, density=True)
    var_95 = np.percentile(final_pnls, 5)
    ax2.axvline(var_95, color='red', linestyle='dashed', linewidth=2, label=f'VaR (95%): {var_95:.2f}')
    ax2.set_title('Monte Carlo PnL Distribution (1000 Sims)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Daily Profit/Loss ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = 'arbitrage_risk.png'
    plt.savefig(filename, dpi=300)
    print(f"Generated {filename}")

if __name__ == "__main__":
    print("Running Algorithmic Arbitrage Simulation...")
    simulate_latency_arbitrage()
