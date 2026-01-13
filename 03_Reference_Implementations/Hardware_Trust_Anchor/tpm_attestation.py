import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import unittest
import sys

# -----------------------------------------------------------------------------
# Module 10: Hardware Trust Anchor (TPM 2.0 / SGX)
# -----------------------------------------------------------------------------
# Simulation of a Trusted Platform Module (TPM) Measured Boot process.
# Validates the strict "Chain of Trust" from BIOS to Kernel.
# -----------------------------------------------------------------------------

class TPMVerificator:
    def __init__(self, simulate_tamper=True):
        self.golden_state = {
            'PCR 00 (BIOS)': 0.95,
            'PCR 02 (ROMs)': 0.88,
            'PCR 04 (Boot)': 0.92,
            'PCR 08 (Cmd)': 0.98,
            'PCR 09 (Kernel)': 0.99
        }
        self.simulate_tamper = simulate_tamper

    def measure_boot(self):
        """Perform simulated boot measurements."""
        current_state = {k: v + np.random.normal(0, 0.001) for k, v in self.golden_state.items()}
        
        if self.simulate_tamper:
            # Rootkit Injection detected in Kernel Space
            current_state['PCR 09 (Kernel)'] = 0.65 
            
        return current_state

    def attest(self, current_state):
        """Verify measurements against Golden State."""
        valid = True
        for key, val in current_state.items():
            if abs(val - self.golden_state[key]) > 0.05: # Threshold
                valid = False
        return valid

    def visualize(self, current_state, output_file='tpm_attestation.png'):
        labels = list(self.golden_state.keys())
        golden_vals = list(self.golden_state.values())
        current_vals = list(current_state.values())
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(labels))
        width = 0.35
        
        ax.bar(x - width/2, golden_vals, width, label='Reference (Golden)', color='#2ecc71', alpha=0.8)
        ax.bar(x + width/2, current_vals, width, label='Measured (Current)', color='#e74c3c', alpha=0.8)
        
        ax.set_ylabel('Integrity Score (Normalized Hash Match)', fontsize=12)
        ax.set_title('TPM 2.0 Measured Boot: Remote Attestation', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=15)
        ax.set_ylim(0, 1.2)
        ax.legend()
        
        if not self.attest(current_state):
            ax.annotate('INTEGRITY FAILURE\n(Rootkit detected)',
                        xy=(4 + width/2, 0.65), xycoords='data',
                        xytext=(3.5, 0.9), textcoords='data',
                        arrowprops=dict(facecolor='black', shrink=0.05),
                        color='red', fontweight='bold')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        print(f"Generated {output_file}")

# --- UNIT TESTS ---
class TestTPM(unittest.TestCase):
    def test_clean_boot(self):
        tpm = TPMVerificator(simulate_tamper=False)
        state = tpm.measure_boot()
        self.assertTrue(tpm.attest(state), "Clean boot should pass attestation")

    def test_tampered_boot(self):
        tpm = TPMVerificator(simulate_tamper=True)
        state = tpm.measure_boot()
        self.assertFalse(tpm.attest(state), "Tampered boot should fail attestation")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TPM Remote Attestation Simulator')
    parser.add_argument('--clean', action='store_true', help='Simulate a clean, untampered boot')
    parser.add_argument('--test', action='store_true', help='Run unit tests')
    args = parser.parse_args()

    if args.test:
        sys.argv = [sys.argv[0]]
        unittest.main()
    else:
        print(f"Running TPM Attestation (Tamper Simulation: {not args.clean})...")
        tpm = TPMVerificator(simulate_tamper=not args.clean)
        state = tpm.measure_boot()
        tpm.visualize(state)
        if tpm.attest(state):
            print("System Integrity: VERIFIED")
        else:
            print("System Integrity: COMPROMISED")
