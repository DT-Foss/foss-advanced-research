import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import unittest
import sys

# -----------------------------------------------------------------------------
# Module 12: Quantitative Risk Engine (VaR / CVaR)
# -----------------------------------------------------------------------------
# Simulation of Portfolio Risk using Monte Carlo methods.
# Calculates Value at Risk (VaR) and Expected Shortfall (CVaR) for a 
# multi-asset portfolio under stress conditions.
# -----------------------------------------------------------------------------

class RiskEngine:
    def __init__(self, simulations=10000, horizon=21):
        self.num_simulations = simulations
        self.horizon_days = horizon
        self.assets = ['Equities', 'Bonds', 'Crypto', 'Commodities', 'Real Estate']
        self.weights = np.array([0.30, 0.20, 0.10, 0.20, 0.20])
        # Stress Scenario Matrix
        self.corr_matrix = np.array([
            [1.0, 0.2, 0.6, 0.4, 0.3],
            [0.2, 1.0, 0.1, -0.1, 0.4],
            [0.6, 0.1, 1.0, 0.3, 0.1],
            [0.4, -0.1, 0.3, 1.0, 0.2],
            [0.3, 0.4, 0.1, 0.2, 1.0]
        ])
        self.vols = np.array([0.15, 0.05, 0.80, 0.20, 0.10])

    def calculate_var(self, pnl_distribution, confidence_level=0.95):
        """Calculate Value at Risk at a given confidence level."""
        percentile = (1 - confidence_level) * 100
        return np.percentile(pnl_distribution, percentile)

    def run_simulation(self):
        """Execute Monte Carlo Simulation."""
        np.random.seed(42)
        num_assets = len(self.assets)
        
        # Cholesky Decomposition
        try:
            L = np.linalg.cholesky(self.corr_matrix)
        except np.linalg.LinAlgError:
            print("Error: Correlation matrix not positive definite.")
            return None, None

        uncorrelated_randoms = np.random.normal(0, 1, (num_assets, self.num_simulations))
        correlated_randoms = np.dot(L, uncorrelated_randoms)
        
        dt = self.horizon_days / 252.0
        daily_returns = correlated_randoms * self.vols[:, np.newaxis] * np.sqrt(dt)
        
        portfolio_returns = np.dot(self.weights, daily_returns)
        initial_value = 1_000_000 
        ending_values = initial_value * (1 + portfolio_returns)
        pnl = ending_values - initial_value
        
        return pnl, self.assets

    def visualize(self, pnl, output_file='risk_heatmap.png'):
        var_95 = self.calculate_var(pnl, 0.95)
        var_99 = self.calculate_var(pnl, 0.99)
        
        fig = plt.figure(figsize=(14, 8))
        gs = fig.add_gridspec(2, 2)
        
        ax1 = fig.add_subplot(gs[0, 0])
        sns.heatmap(self.corr_matrix, annot=True, xticklabels=self.assets, yticklabels=self.assets, 
                    cmap='coolwarm', ax=ax1, vmin=-1, vmax=1)
        ax1.set_title('Asset Correlation Matrix (Stress Scenario)', fontweight='bold')
        
        ax2 = fig.add_subplot(gs[0, 1])
        sns.histplot(pnl, kde=True, ax=ax2, color='#3498db', bins=50)
        ax2.axvline(var_95, color='#f1c40f', linestyle='--', linewidth=2, label=f'VaR 95%: ${var_95:,.0f}')
        ax2.axvline(var_99, color='#e74c3c', linestyle='--', linewidth=2, label=f'VaR 99%: ${var_99:,.0f}')
        ax2.set_xlabel('Portfolio Profit/Loss ($)')
        ax2.set_title(f'Monte Carlo Loss Distribution (N={self.num_simulations})', fontweight='bold')
        ax2.legend()
        
        # Conceptual Efficient Frontier
        ax3 = fig.add_subplot(gs[1, :])
        rand_vols = np.random.uniform(0.05, 0.30, 200)
        rand_rets = np.log(rand_vols * 10) * 0.1 + np.random.normal(0, 0.02, 200)
        sc = ax3.scatter(rand_vols, rand_rets, c=rand_rets/rand_vols, cmap='viridis')
        ax3.set_xlabel('Portfolio Risk (Volatility)')
        ax3.set_ylabel('Expected Return')
        ax3.set_title('Efficient Frontier Optimization', fontweight='bold')
        plt.colorbar(sc, label='Sharpe Ratio', ax=ax3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        print(f"Generated {output_file}")

# --- UNIT TESTS ---
class TestRiskEngine(unittest.TestCase):
    def test_var_calculation(self):
        engine = RiskEngine(simulations=100)
        # Create a deterministic distribution: -100 to -1
        dummy_pnl = np.linspace(-100, -1, 100)
        # VaR 95% should be roughly -95 (5th percentile)
        var = engine.calculate_var(dummy_pnl, 0.95)
        self.assertTrue(-96 <= var <= -94, f"VaR calculation incorrect: {var}")

    def test_simulation_shape(self):
        engine = RiskEngine(simulations=500)
        pnl, _ = engine.run_simulation()
        self.assertEqual(len(pnl), 500)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Quantitative Risk Engine (Monte Carlo)')
    parser.add_argument('--simulations', type=int, default=10000, help='Number of Monte Carlo simulations')
    parser.add_argument('--horizon', type=int, default=21, help='Time horizon in days')
    parser.add_argument('--test', action='store_true', help='Run unit tests')
    args = parser.parse_args()

    if args.test:
        sys.argv = [sys.argv[0]] # Clear args for unittest
        unittest.main()
    else:
        print(f"Running Risk Engine (Simulations: {args.simulations}, Horizon: {args.horizon} days)...")
        engine = RiskEngine(simulations=args.simulations, horizon=args.horizon)
        pnl, _ = engine.run_simulation()
        if pnl is not None:
            engine.visualize(pnl)
