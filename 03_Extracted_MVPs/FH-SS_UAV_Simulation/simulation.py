import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict, Tuple

# --- Configuration ---
FREQ_BASE = 40000  # 40 kHz
FREQ_HOP_RANGE = 5000  # +/- 5 kHz
PRN_LENGTH = 2047
JAMMING_THRESHOLD = 0.3

@dataclass
class SystemState:
    timestamp: float
    altitude: float
    jamming_score: float # 0.0 - 1.0
    snr: float
    mode: str = "EKF" # EKF or UKF
    energy_level: float = 100.0

class FH_SS_Array:
    """Frequency-Hopping Spread Spectrum module."""
    def __init__(self):
        self.prn_sequence = [random.choice([-1, 1]) for _ in range(PRN_LENGTH)]
        self.current_freq = FREQ_BASE
        
    def update(self, time_step: int, jamming_score: float) -> float:
        """
        adapt frequency based on jamming:
        f(t) = f0 + Delta_f * PRN(t) * [1 + alpha * J(t)]
        """
        alpha = 0.5 # Adaptability factor
        prn_val = self.prn_sequence[time_step % PRN_LENGTH]
        shift = FREQ_HOP_RANGE * prn_val * (1 + alpha * jamming_score)
        self.current_freq = FREQ_BASE + shift
        return self.current_freq

class RamanSpectroscopy:
    """Jamming-triggered atmospheric correction."""
    def __init__(self):
        self.active = False
        self.correction_factor = 1.0
        
    def update(self, jamming_score: float):
        """Activates if jamming > threshold."""
        if jamming_score > JAMMING_THRESHOLD:
            self.active = True
            # Simulate correction factor calculation
            # c_corrected = c0 * sqrt(1 + ... + alpha_R * R_factor)
            # Simplified for simulation:
            self.correction_factor = 1.0 + (0.01 * jamming_score) 
        else:
            self.active = False
            self.correction_factor = 1.0
            
    def get_sound_speed_correction(self) -> float:
        return 343.0 * self.correction_factor

class PINN_Optimizer:
    """Physics-Informed Neural Network Optimizer (Simulated)."""
    def __init__(self):
        self.weights = {"data": 1.0, "physics": 1.0, "energy": 1.0}
        
    def compute_loss(self, state: SystemState) -> float:
        """
        L = w1*L_data + w2*L_physics + w3*L_energy
        """
        l_data = abs(state.altitude - 10.0) # Target 10m
        l_physics = 0.1 * state.jamming_score # Mock physics residue (aerodynamics)
        l_energy = max(0, 100 - state.energy_level)
        
        loss = (self.weights["data"] * l_data + 
                self.weights["physics"] * l_physics + 
                self.weights["energy"] * l_energy)
        return loss
    
    def adapt_weights(self, jamming_score: float):
        """Adapt weights based on threat level."""
        if jamming_score > 0.5:
            # Prioritize physics/robustness over data
            self.weights["physics"] = 2.0
            self.weights["data"] = 0.5

class SensorFusion:
    """Adaptive EKF/UKF Switching."""
    def __init__(self):
        self.mode = "EKF" # or UKF
        self.covariance = np.eye(3) * 0.1
        
    def update(self, jamming_score: float, nonlinearity: float):
        """
        Switch to UKF if highly nonlinear or high jamming.
        Switch_to_UKF = (nonlinearity > theta) OR (J > theta_jam)
        """
        theta_jam = 0.4
        if jamming_score > theta_jam or nonlinearity > 0.8:
            self.mode = "UKF"
        else:
            self.mode = "EKF"
            
        # Adapt covariance: R_adaptive = R0 * [1 + beta * J^2/(1+J^2)]
        beta_jam = 5.0
        factor = 1 + beta_jam * (jamming_score**2 / (1 + jamming_score**2))
        self.covariance = np.eye(3) * 0.1 * factor

def run_simulation(steps=100):
    print("Initialize FH-SS UAV Landing Simulation...")
    
    fh_ss = FH_SS_Array()
    raman = RamanSpectroscopy()
    pinn = PINN_Optimizer()
    fusion = SensorFusion()
    
    # Initial state
    altitude = 50.0 # meters
    energy = 100.0
    
    history = []
    
    print(f"{'Step':<5} | {'Jamming':<8} | {'Freq (Hz)':<10} | {'Raman':<6} | {'Mode':<4} | {'Covariance':<10} | {'PINN Loss':<10}")
    print("-" * 80)
    
    for t in range(steps):
        # 1. Simulate Environment (Jamming increases over time)
        jamming = min(1.0, max(0.0, (t - 20) / 50.0 + random.normalvariate(0, 0.05)))
        nonlinearity = min(1.0, altitude / 100.0) # High altitude -> more linear
        
        # 2. Update FH-SS
        freq = fh_ss.update(t, jamming)
        
        # 3. Update Raman
        raman.update(jamming)
        speed_sound = raman.get_sound_speed_correction()
        
        # 4. Update Fusion
        fusion.update(jamming, nonlinearity)
        
        # 5. Update PINN
        state = SystemState(float(t), altitude, jamming, 1.0, fusion.mode, energy)
        pinn.adapt_weights(jamming)
        loss = pinn.compute_loss(state)
        
        # 6. Physics Step (landing)
        altitude = max(0.0, altitude - 0.5)
        
        # Log
        if t % 10 == 0:
            cov_diag = fusion.covariance[0,0]
            print(f"{t:<5} | {jamming:<8.2f} | {freq:<10.0f} | {str(raman.active):<6} | {fusion.mode:<4} | {cov_diag:<10.3f} | {loss:<10.3f}")
            
    print("-" * 80)
    print("Simulation Complete.")

if __name__ == "__main__":
    run_simulation()
