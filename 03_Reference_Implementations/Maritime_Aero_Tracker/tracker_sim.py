import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List

# -----------------------------------------------------------------------------
# Module 07: Maritime & Aero Tracker (ADS-B / VDES)
# -----------------------------------------------------------------------------
# Scientific Simulation of RF Surveillance Systems.
# Models Free Space Path Loss (FSPL) and signal detection probability
# for 1090 MHz (ADS-B) and 162 MHz (AIS/VDES).
# -----------------------------------------------------------------------------

@dataclass
class Target:
    id: str
    type: str # 'AIRCRAFT' or 'VESSEL'
    azimuth_deg: float
    distance_km: float
    altitude_m: float
    signal_strength_dbm: float = -100.0

def friis_transmission_equation(pt_dbm: float, gt_dbi: float, gr_dbi: float, freq_mhz: float, dist_km: float) -> float:
    """
    Calculate Received Signal Strength (RSS) using Friis Transmission Equation.
    PR = PT + GT + GR - FSPL
    FSPL (dB) = 20log10(d) + 20log10(f) + 32.44
    """
    if dist_km <= 0: return pt_dbm
    
    fspl = 20 * np.log10(dist_km) + 20 * np.log10(freq_mhz) + 32.44
    
    pr_dbm = pt_dbm + gt_dbi + gr_dbi - fspl
    
    # Add stochastic noise (fading/multipath)
    noise = np.random.normal(0, 3.0) 
    return pr_dbm + noise

def simulate_surveillance_scenario(num_targets: int = 50):
    targets: List[Target] = []
    
    # --- Receiver Parameters ---
    gr_dbi = 12.0 # High gain antenna
    sensitivity_dbm = -105.0
    
    for i in range(num_targets):
        is_aircraft = np.random.random() > 0.4
        
        if is_aircraft:
            # Aircraft (ADS-B 1090 MHz)
            # High altitude, high speed, long range
            type_str = 'AIRCRAFT'
            freq = 1090.0
            pt_dbm = 51.0 # ~125 Watts (Transponder)
            gt_dbi = 3.0 
            dist = np.random.uniform(10, 350) # up to 350km horizon
            alt = np.random.uniform(1000, 12000)
            az = np.random.uniform(0, 360)
        else:
            # Maritime (AIS/VDES 162 MHz)
            # Sea level, shorter horizon (curvature)
            type_str = 'VESSEL'
            freq = 162.0
            pt_dbm = 41.0 # ~12.5 Watts
            gt_dbi = 2.0
            dist = np.random.uniform(1, 80) # Horizon limited
            alt = 0
            az = np.random.uniform(0, 360)
            
        rss = friis_transmission_equation(pt_dbm, gt_dbi, gr_dbi, freq, dist)
        
        targets.append(Target(f"TRK-{i:03}", type_str, az, dist, alt, rss))

    # --- Visualization (Radar Plot) ---
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='polar')
    
    # Filter detectable targets
    detected_air = [t for t in targets if t.type == 'AIRCRAFT' and t.signal_strength_dbm > sensitivity_dbm]
    detected_sea = [t for t in targets if t.type == 'VESSEL' and t.signal_strength_dbm > sensitivity_dbm]
    
    # Plot Aircraft
    theta_air = [np.radians(t.azimuth_deg) for t in detected_air]
    r_air = [t.distance_km for t in detected_air]
    colors_air = [t.signal_strength_dbm for t in detected_air]
    
    sc1 = ax.scatter(theta_air, r_air, c=colors_air, cmap='plasma', marker='^', s=100, label='Aircraft (ADS-B)', vmin=-110, vmax=-60)
    
    # Plot Vessels
    theta_sea = [np.radians(t.azimuth_deg) for t in detected_sea]
    r_sea = [t.distance_km for t in detected_sea]
    
    # Normalized color adaptation for visibility
    sc2 = ax.scatter(theta_sea, r_sea, c='cyan', marker='s', s=80, label='Vessel (VDES/AIS)', alpha=0.8)

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rmax(350)
    ax.set_title(f"Multi-Domain RF Surveillance Simulation\nTotal Targets: {len(detected_air) + len(detected_sea)}", fontweight='bold')
    
    plt.legend(loc='lower left')
    
    # Colorbar
    cbar = plt.colorbar(sc1, ax=ax, pad=0.1)
    cbar.set_label('Received Signal Strength (dBm)')
    
    plt.savefig('surveillance_plot.png', dpi=300)
    print("Generated surveillance_plot.png")

if __name__ == "__main__":
    print("Running Maritime & Aero Surveillance Simulation...")
    simulate_surveillance_scenario()
