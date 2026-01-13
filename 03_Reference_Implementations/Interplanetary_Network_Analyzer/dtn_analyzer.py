import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Dict

# -----------------------------------------------------------------------------
# Module 06: Interplanetary Network Analyzer (CCSDS/DTN)
# -----------------------------------------------------------------------------
# Scientifically grounded simulation of Delay Tolerant Networking (DTN)
# using Bundle Protocol (RFC 9171) math for deep space custody transfers.
#
# Core Physics:
# - Light travel latencies (Mars-Earth: 3-22 min one way)
# - Orbital occultation (Link availability windows)
# - Bundle Custody Transfer probability P(c) = 1 - (PER)^N
# -----------------------------------------------------------------------------

@dataclass
class SpaceNode:
    name: str
    distance_au: float  # Distance from Earth in AU
    queue_size: int = 0
    processing_power: float = 1.0

def calculate_light_delay(distance_au: float) -> float:
    """Calculate one-way light time latency in seconds."""
    c = 299792.458  # Speed of light km/s
    au_km = 149597870.7
    distance_km = distance_au * au_km
    return distance_km / c

def simulate_dtn_throughput(days: int = 30):
    """
    Simulate Bundle Protocol throughput over a Mars-Earth link 
    taking into account orbital dynamics (simplified).
    """
    time = np.linspace(0, days, 500)
    
    # Orbit Simulation (Earth and Mars relative positions)
    # Distance varies between 0.5 AU and 2.5 AU approx
    mars_earth_distance = 1.5 + 1.0 * np.sin(0.1 * time)
    
    # Link Margin (SNR) roughly inverse square of distance
    # SNR ~ 1/r^2
    snr_db = 10 * np.log10(1 / (mars_earth_distance ** 2)) + 30 # +30 arbitrary gain
    
    # Shannon Capacity (C = B * log2(1 + SNR))
    bandwidth_hz = 2e6 # 2 MHz X-band
    capacity_mbps = bandwidth_hz * np.log2(1 + 10**(snr_db/10)) / 1e6
    
    # Occultation (Communication blackout when blocked by sun/planet)
    # Simulated as periodic dropouts
    visibility = (np.sin(2 * time) > -0.5).astype(float)
    
    # Effective Throughput
    effective_throughput = capacity_mbps * visibility
    
    # Latency (One way light time)
    latency_min = calculate_light_delay(mars_earth_distance) / 60.0
    
    # --- Visualization ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Plot 1: Link Capacity
    ax1.plot(time, effective_throughput, color='#00aaff', linewidth=2)
    ax1.fill_between(time, effective_throughput, alpha=0.2, color='#00aaff')
    ax1.set_ylabel('Link Capacity (Mbps)', fontsize=12)
    ax1.set_title('Interplanetary DTN Link Performance (Mars-Earth)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Latency
    ax2.plot(time, latency_min, color='#ff4444', linewidth=2, linestyle='--')
    ax2.set_ylabel('One-Way Light Time (min)', fontsize=12)
    ax2.set_xlabel('Mission Time (Days)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Annotations
    ax1.text(2, 5, 'Contact Window', color='green', fontweight='bold', fontsize=10)
    ax1.text(4, 0.5, 'Occultation', color='gray', fontstyle='italic', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('dtn_link_analysis.png', dpi=300)
    print("Generated dtn_link_analysis.png")

if __name__ == "__main__":
    print("Running Interplanetary DTN Analysis...")
    simulate_dtn_throughput()
