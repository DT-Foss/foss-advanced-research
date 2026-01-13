import numpy as np
from dataclasses import dataclass

@dataclass
class NFMILinkBudget:
    frequency_hz: float
    transmit_power_dbm: float
    distance_m: float
    coil_radius_m: float
    permeability_rel: float = 1.0 # Air

class NFMIPhysicsEngine:
    """
    Physics simulation of Near-Field Magnetic Induction (NFMI) channel.
    Key Characteristic: H-field falls off as 1/r^3, Power as 1/r^6.
    Unlike RF (1/r^2), this creates a 'Bubble of Silence' secure zone.
    """
    
    def __init__(self):
        self.mu_0 = 4 * np.pi * 1e-7 # Vacuum permeability
        
    def calculate_path_loss(self, link: NFMILinkBudget) -> float:
        """
        Calculate Path Loss in dB for Near Field Magnetic Induction.
        Formula derived from Agbinya (2011):
        PL = 60 * log10(d) + 20 * log10(f) + Constants...
        
        Simplified Model:
        P_rx = P_tx * (r_coil / d)^6
        """
        # Critical Distance (boundary between near/far field)
        # d_c = lambda / 2*pi
        wavelength = 3e8 / link.frequency_hz
        d_c = wavelength / (2 * np.pi)
        
        if link.distance_m > d_c:
            print(f"⚠️ Warning: Distance {link.distance_m}m exceeds Near-Field limit ({d_c:.2f}m). Radiation dominates.")
        
        # Power Transfer Factor (Magnetic Coupling)
        # Factor decreases with r^6
        coupling_factor = (link.coil_radius_m / max(link.coil_radius_m, link.distance_m)) ** 6
        
        # Convert to dB
        path_loss_db = -10 * np.log10(coupling_factor + 1e-20)
        return path_loss_db

    def simulate_security_zone(self, max_dist=2.0):
        print(f"🔬 Simulating NFMI 'Bubble of Silence' (Security Zone)")
        print(f"{'Dist (m)':<10} | {'Signal (dBm)':<15} | {'Status':<15}")
        print("-" * 45)
        
        tx_power = 0.0 # dBm (1mW)
        distances = np.linspace(0.1, max_dist, 20)
        
        secure_threshold = -90.0 # Noise floor
        
        for d in distances:
            link = NFMILinkBudget(
                frequency_hz=13.56e6, # HF band
                transmit_power_dbm=tx_power,
                distance_m=d,
                coil_radius_m=0.01 # 1cm coil
            )
            pl = self.calculate_path_loss(link)
            rx_power = tx_power - pl
            
            # Security Check
            status = "🔒 SECURE" if rx_power > secure_threshold else "❌ NO SIGNAL"
            if rx_power < secure_threshold and rx_power > secure_threshold - 10:
                status = "📉 FADING"
                
            print(f"{d:<10.2f} | {rx_power:<15.2f} | {status:<15}")

if __name__ == "__main__":
    engine = NFMIPhysicsEngine()
    engine.simulate_security_zone()
