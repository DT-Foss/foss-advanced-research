import numpy as np
import random
import time
from dataclasses import dataclass

# --- Hyperdimensional Computing Engine (Mock) ---
class HDComputing:
    def __init__(self, dim=10000):
        self.dim = dim
    
    def create_random_vector(self):
        return np.random.choice([-1, 1], size=self.dim)
    
    def bind(self, v1, v2):
        return v1 * v2  # Element-wise multiplication
    
    def bundle(self, v1, v2):
        return np.sign(v1 + v2) # Majority rule
        
    def permute(self, v, k=1):
        return np.roll(v, k)

# --- Geometry & Projection ---
class Tesseract4D:
    def __init__(self):
        # 16 vertices of a tesseract
        self.vertices = []
        for i in range(16):
            # Binary repr to coords: 0 -> -1, 1 -> 1
            coords = [(2 * int(c) - 1) for c in format(i, '04b')]
            self.vertices.append(np.array(coords))
            
    def get_vertices(self):
        return np.array(self.vertices)

class ProjectionEngine:
    def __init__(self):
        self.rotation_angles = [0.0, 0.0] # theta1, theta2
        self.noise_intensity = 0.0
        
    def stochastic_rotation_matrix_4d(self, theta1, theta2):
        # Simplified 4D rotation (double isoclinic)
        # R(theta1, theta2) block diag
        c1, s1 = np.cos(theta1), np.sin(theta1)
        c2, s2 = np.cos(theta2), np.sin(theta2)
        
        # Planar rotation xy and zw (simplified)
        R_xy = np.eye(4)
        R_xy[0,0], R_xy[0,1] = c1, -s1
        R_xy[1,0], R_xy[1,1] = s1, c1
        
        R_zw = np.eye(4)
        R_zw[2,2], R_zw[2,3] = c2, -s2
        R_zw[3,2], R_zw[3,3] = s2, c2
        
        return R_xy @ R_zw

    def project_to_3d(self, points_4d, method="coxeter"):
        # Coxeter-Banchoff Projection Vector
        # Maps 4D -> 3D preserving symmetry
        # P = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]] - Standard orthographic
        # Coxeter uses specific weights
        if method == "coxeter":
            # Simplified projection matrix for visual symmetry
            # This is a common visualization tech for tesseracts
            s3 = np.sqrt(3)
            P = np.array([
                [1,  0, 0, 0],
                [0,  1, 0, 0],
                [0,  0, 1, 0]
            ])
            # Apply stochastic rotation first
            R = self.stochastic_rotation_matrix_4d(*self.rotation_angles)
            rotated = points_4d @ R.T
            return rotated @ P.T
        return points_4d[:, :3]

# --- Neuroadaptive Loop ---
class NeuroFeedbackAgent:
    def __init__(self):
        self.mutual_info_history = []
        self.learning_rate = 0.1
        
    def get_mock_eeg_signal(self):
        # Simulate 30Hz Gamma band
        return np.random.normal(0, 1) + np.sin(time.time() * 30)
        
    def get_mock_fnirs_signal(self):
        # Simulate 1Hz Hemodynamic response
        return np.sin(time.time() * 1)
        
    def optimize(self, current_angles):
        # PPO Logic (Simplified)
        # Reward = Mutual Information (mocked as stability of projection)
        reward = random.uniform(0, 1) # Mock reward
        
        # Update policy (angles)
        new_angles = [
            current_angles[0] + np.random.normal(0, 0.05),
            current_angles[1] + np.random.normal(0, 0.05)
        ]
        return new_angles, reward

# --- Main Simulation ---
def run_simulation(steps=100):
    print("Initialize Multisensory 4D Projection Simulation...")
    
    hdc = HDComputing()
    tesseract = Tesseract4D()
    projector = ProjectionEngine()
    agent = NeuroFeedbackAgent()
    
    # 1. Encode Data (Mock: Bind Axis Concepts)
    axis_x = hdc.create_random_vector()
    axis_y = hdc.create_random_vector()
    bound = hdc.bind(axis_x, axis_y)
    print(f"HDC Binding Complete. Vector Dim: {hdc.dim}")
    
    points_4d = tesseract.get_vertices()
    print(f"Loaded 4D Geometry: {len(points_4d)} vertices")
    
    print("-" * 60)
    print(f"{'Step':<5} | {'Theta1':<8} | {'Theta2':<8} | {'Reward':<6} | {'Status':<15}")
    print("-" * 60)
    
    for t in range(steps):
        # 1. Neuro Feedback
        eeg = agent.get_mock_eeg_signal()
        fnirs = agent.get_mock_fnirs_signal()
        
        # 2. Optimize Projection
        new_angles, reward = agent.optimize(projector.rotation_angles)
        projector.rotation_angles = new_angles
        
        # 3. Render (Project)
        points_3d = projector.project_to_3d(points_4d)
        
        # 4. Status
        status = "Stabilizing" if reward > 0.5 else "Searching"
        
        if t % 10 == 0:
            t1 = projector.rotation_angles[0]
            t2 = projector.rotation_angles[1]
            print(f"{t:<5} | {t1:<8.2f} | {t2:<8.2f} | {reward:<6.2f} | {status:<15}")
            
    print("-" * 60)
    print("Simulation Complete.")

if __name__ == "__main__":
    run_simulation()
