import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from typing import List

# -----------------------------------------------------------------------------
# Module 12: Quantitative Risk Engine (VaR / CVaR)
# -----------------------------------------------------------------------------
# Simulation of Portfolio Risk using Monte Carlo methods.
# Calculates Value at Risk (VaR) and Expected Shortfall (CVaR) for a 
# multi-asset portfolio under stress conditions.
# -----------------------------------------------------------------------------

def simulate_portfolio_risk():
    """
    Simulate correlated asset returns to generate a Risk Heatmap and 
    Portfolio Loss Distribution.
    """
    np.random.seed(42)
    
    # Portfolio Configuration
    assets = ['Equities', 'Bonds', 'Crypto', 'Commodities', 'Real Estate']
    weights = np.array([0.30, 0.20, 0.10, 0.20, 0.20])
    num_assets = len(assets)
    
    # Simulation Parameters
    num_simulations = 10000
    horizon_days = 21 # 1 month
    
    # Correlation Matrix (Stress Scenario - Correlations increase in crisis)
    corr_matrix = np.array([
        [1.0, 0.2, 0.6, 0.4, 0.3],
        [0.2, 1.0, 0.1, -0.1, 0.4],
        [0.6, 0.1, 1.0, 0.3, 0.1],
        [0.4, -0.1, 0.3, 1.0, 0.2],
        [0.3, 0.4, 0.1, 0.2, 1.0]
    ])
    
    # Volatilities (Annualized)
    vols = np.array([0.15, 0.05, 0.80, 0.20, 0.10])
    
    # Cholesky Decomposition for Correlated Random Walking
    L = np.linalg.cholesky(corr_matrix)
    
    # Generate Correlated Returns
    uncorrelated_randoms = np.random.normal(0, 1, (num_assets, num_simulations))
    correlated_randoms = np.dot(L, uncorrelated_randoms)
    
    # Scale by Volatility and Time
    dt = horizon_days / 252.0
    daily_returns = correlated_randoms * vols[:, np.newaxis] * np.sqrt(dt)
    
    # Calculate Portfolio PnL
    portfolio_returns = np.dot(weights, daily_returns)
    initial_value = 1_000_000 # $1M Portfolio
    ending_values = initial_value * (1 + portfolio_returns)
    pnl = ending_values - initial_value
    
    # VaR Calculations
    var_95 = np.percentile(pnl, 5)
    var_99 = np.percentile(pnl, 1)
    cvar_99 = pnl[pnl <= var_99].mean() # Expected Shortfall
    
    # --- Visualization ---
    fig = plt.figure(figsize=(14, 8))
    gs = fig.add_gridspec(2, 2)
    
    # Plot 1: Correlation Heatmap
    ax1 = fig.add_subplot(gs[0, 0])
    sns.heatmap(corr_matrix, annot=True, xticklabels=assets, yticklabels=assets, 
                cmap='coolwarm', ax=ax1, vmin=-1, vmax=1)
    ax1.set_title('Asset Correlation Matrix (Stress Scenario)', fontweight='bold')
    
    # Plot 2: PnL Distribution
    ax2 = fig.add_subplot(gs[0, 1])
    sns.histplot(pnl, kde=True, ax=ax2, color='#3498db', bins=50)
    ax2.axvline(var_95, color='#f1c40f', linestyle='--', linewidth=2, label=f'VaR 95%: ${var_95:,.0f}')
    ax2.axvline(var_99, color='#e74c3c', linestyle='--', linewidth=2, label=f'VaR 99%: ${var_99:,.0f}')
    ax2.set_xlabel('Portfolio Profit/Loss ($)')
    ax2.set_title('Monte Carlo Loss Distribution (N=10,000)', fontweight='bold')
    ax2.legend()
    
    # Plot 3: Efficient Frontier (Conceptual)
    ax3 = fig.add_subplot(gs[1, :])
    # Generate random portfolios for frontier
    rand_vols = np.random.uniform(0.05, 0.30, 200)
    rand_rets = np.log(rand_vols * 10) * 0.1 + np.random.normal(0, 0.02, 200)
    sc = ax3.scatter(rand_vols, rand_rets, c=rand_rets/rand_vols, cmap='viridis')
    ax3.set_xlabel('Portfolio Risk (Volatility)')
    ax3.set_ylabel('Expected Return')
    ax3.set_title('Efficient Frontier Optimization', fontweight='bold')
    plt.colorbar(sc, label='Sharpe Ratio', ax=ax3)
    
    plt.tight_layout()
    filename = 'risk_heatmap.png'
    plt.savefig(filename, dpi=300)
    print(f"Generated {filename}")

if __name__ == "__main__":
    print("Running Quantitative Risk Engine...")
    simulate_portfolio_risk()
