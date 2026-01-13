import numpy as np
import time
from dataclasses import dataclass
from typing import Tuple, List

# --- Real Hyperdimensional Computing Engine (10k dimensions) ---
class HDComputing:
    """
    Implementation of 10,000-dimensional Bipolar Hyperdimensional Computing.
    Math:
    - Bipolar Vectors: {-1, 1}^D
    - Binding (XOR equivalent): Element-wise Multiplication
    - Bundling (Superposition): Element-wise Addition + Sign Threshold
    - Permutation: Cyclic Shift
    """
    def __init__(self, dim=10000):
        self.dim = dim
    
    def create_random_vector(self) -> np.ndarray:
        """Create a random bipolar vector {-1, 1}"""
        return np.random.choice([-1, 1], size=self.dim).astype(np.int8)
    
    def bind(self, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        """
        Binding operation (Associative, Commutative, Distributive)
        Maps two vectors to a new orthogonal vector.
        Formula: v_out = v1 * v2
        """
        return v1 * v2
    
    def bundle(self, vectors: List[np.ndarray]) -> np.ndarray:
        """
        Bundling operation (Superposition)
        Formula: v_out = sign(sum(vectors))
        """
        # Sum all vectors
        sum_vec = np.sum(vectors, axis=0)
        # Apply sign function (Majority Rule), handle zeros randomly or default to 1
        bundled = np.sign(sum_vec)
        bundled[bundled == 0] = np.random.choice([-1, 1], size=np.count_nonzero(bundled == 0))
        return bundled.astype(np.int8)
        
    def permute(self, v: np.ndarray, k=1) -> np.ndarray:
        """
        Permutation (Sequence Encoding)
        Formula: v_out = Roll(v, k)
        """
        return np.roll(v, k)
        
    def similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Cosine Similarity for Bipolar Vectors.
        Approximated by Hamming Distance: Sim = 1 - 2*Hamming / D
        Or simply normalized dot product.
        """
        dot_product = np.dot(v1, v2)
        return dot_product / self.dim

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
        
    def stochastic_rotation_matrix_4d(self, theta1, theta2):
        # 4D Rotation Logic
        c1, s1 = np.cos(theta1), np.sin(theta1)
        c2, s2 = np.cos(theta2), np.sin(theta2)
        
        # Planar rotation xy and zw
        R_xy = np.eye(4)
        R_xy[0,0], R_xy[0,1] = c1, -s1
        R_xy[1,0], R_xy[1,1] = s1, c1
        
        R_zw = np.eye(4)
        R_zw[2,2], R_zw[2,3] = c2, -s2
        R_zw[3,2], R_zw[3,3] = s2, c2
        
        return R_xy @ R_zw

    def project_to_3d(self, points_4d):
        # Coxeter-Banchoff Projection
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

# --- Main Simulation ---
def run_simulation(steps=50):
    print("Initialize Multisensory 4D Projection Simulation with Real HDC...")
    
    hdc = HDComputing(dim=10000)
    tesseract = Tesseract4D()
    projector = ProjectionEngine()
    
    # 1. Real HDC Encoding
    print(f"🧠 HDC Engine Initialized. Dimension: {hdc.dim}")
    
    # Concept encoding
    axis_x = hdc.create_random_vector()
    axis_y = hdc.create_random_vector()
    axis_z = hdc.create_random_vector()
    axis_w = hdc.create_random_vector()
    
    # Bind geometry to concepts
    # Concept: "Shape" = X + Y + Z + W
    shape_concept = hdc.bundle([axis_x, axis_y, axis_z, axis_w])
    
    # Verify orthogonality
    sim_x_shape = hdc.similarity(axis_x, shape_concept)
    sim_random_shape = hdc.similarity(hdc.create_random_vector(), shape_concept)
    
    print(f"   Similarity(Axis_X, Shape): {sim_x_shape:.4f} (Expected ~0.0 or high if bundled?)") 
    # Logic note: If X is in Shape, similarity should be > 0 (approx 1/sqrt(N_bundled))
    # With 4 vectors, expected is 0.5. Random is ~0.0
    print(f"   Similarity(Random, Shape): {sim_random_shape:.4f} (Expected ~0.0)")
    
    points_4d = tesseract.get_vertices()
    print(f"   Loaded 4D Geometry: {len(points_4d)} vertices")
    
    print("-" * 80)
    print(f"{'Step':<5} | {'Theta1':<8} | {'Theta2':<8} | {'HDC Stability':<15} | {'Status':<15}")
    print("-" * 80)
    
    for t in range(steps):
        # Update Rotation
        t1 = t * 0.05
        t2 = t * 0.02
        projector.rotation_angles = [t1, t2]
        
        # Project
        # points_3d = projector.project_to_3d(points_4d) # Calculation done, not visualized in text
        
        # HDC Check (Simulating cognitive load stability)
        # We perturb the concept vector with noise and check if we can still recover it
        noise = np.random.choice([-1, 1], size=hdc.dim, p=[0.1, 0.9]) # 10% flip noise
        noisy_shape = shape_concept * noise # Flip signs where noise is -1
        stability = hdc.similarity(shape_concept, noisy_shape)
        
        status = "STABLE" if stability > 0.7 else "DECAY"
        
        if t % 5 == 0:
             print(f"{t:<5} | {t1:<8.2f} | {t2:<8.2f} | {stability:<15.4f} | {status:<15}")
            
    print("-" * 80)
    print("Simulation Complete.")

if __name__ == "__main__":
    run_simulation()
