import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Dict

# -----------------------------------------------------------------------------
# Module 10: Hardware Trust Anchor (TPM 2.0 / SGX)
# -----------------------------------------------------------------------------
# Simulation of a Trusted Platform Module (TPM) Measured Boot process.
# Validates the strict "Chain of Trust" from BIOS to Kernel.
# -----------------------------------------------------------------------------

@dataclass
class PCRBank:
    pcr_00: str # BIOS
    pcr_02: str # Option ROMs
    pcr_04: str # MBR/Bootloader
    pcr_08: str # Kernel Command Line
    pcr_09: str # Kernel Image

def simulate_measured_boot():
    """
    Simulate the extension of hashes into TPM PCRs and compare against
    a 'Golden State' (Signed Reference Manifest).
    """
    
    # Define "Golden" hashes (SHA-256 truncated for display)
    golden_state = {
        'PCR 00 (BIOS)': 0.95,
        'PCR 02 (ROMs)': 0.88,
        'PCR 04 (Boot)': 0.92,
        'PCR 08 (Cmd)': 0.98,
        'PCR 09 (Kernel)': 0.99
    }
    
    # Simulate Current Boot State (with potential tampering in Kernel)
    current_state = {
        'PCR 00 (BIOS)': 0.95 + np.random.normal(0, 0.001), # Tiny measurement noise (negligible)
        'PCR 02 (ROMs)': 0.88 + np.random.normal(0, 0.001),
        'PCR 04 (Boot)': 0.92 + np.random.normal(0, 0.001),
        'PCR 08 (Cmd)': 0.98 + np.random.normal(0, 0.001),
        'PCR 09 (Kernel)': 0.65 # <--- TAMPERING DETECTED (Rootkit)
    }
    
    labels = list(golden_state.keys())
    golden_vals = list(golden_state.values())
    current_vals = list(current_state.values())
    
    # --- Visualization ---
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(labels))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, golden_vals, width, label='Reference (Golden)', color='#2ecc71', alpha=0.8)
    rects2 = ax.bar(x + width/2, current_vals, width, label='Measured (Current)', color='#e74c3c', alpha=0.8)
    
    ax.set_ylabel('Integrity Score (Normalized Hash Match)', fontsize=12)
    ax.set_title('TPM 2.0 Measured Boot: Remote Attestation Failure', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15)
    ax.set_ylim(0, 1.2)
    ax.legend()
    
    # Add annotations for tampering
    ax.annotate('INTEGRITY FAILURE\n(Rootkit detected)',
                xy=(4 + width/2, 0.65), xycoords='data',
                xytext=(3.5, 0.9), textcoords='data',
                arrowprops=dict(facecolor='black', shrink=0.05),
                color='red', fontweight='bold')

    plt.tight_layout()
    filename = 'tpm_attestation.png'
    plt.savefig(filename, dpi=300)
    print(f"Generated {filename}")

if __name__ == "__main__":
    print("Running Hardware Root of Trust Simulation...")
    simulate_measured_boot()
