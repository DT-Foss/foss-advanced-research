import torch
import matplotlib
matplotlib.use('Agg') # Headless mode for CI/CD and Docker
import matplotlib.pyplot as plt
import torch.nn as nn
from dataclasses import dataclass

# --- Configuration ---
# Physical Constants
G = 9.81          # Gravity (m/s^2)
MASS = 25.0       # Satellite/Drone Mass (kg)
MAX_THRUST = 400.0 # Max Thrust (N) - > T/W > 1 required for hovering
T_END = 10.0      # Landing duration (s)

# PINN Hyperparameters
LAYERS = [1, 32, 32, 1] # Time -> [Hidden] -> Altitude
LEARNING_RATE = 0.01
EPOCHS = 1000

@dataclass
class PhysicsState:
    t: float
    z: float
    v: float
    a: float
    thrust: float
    residual: float

class TrajectoryPINN(nn.Module):
    """
    Approximates the vertical trajectory z(t) using a neural network.
    The physics loss enforces the dynamics: m*z'' = T - m*g
    """
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, 32),
            nn.Tanh(), # Tanh is C^inf differentiable, crucial for PINNs
            nn.Linear(32, 32),
            nn.Tanh(),
            nn.Linear(32, 1) # Output: Altitude z(t)
        )

    def forward(self, t):
        return self.net(t)

def get_derivatives(model, t):
    """Compute z, z', z'' using automatic differentiation."""
    t.requires_grad = True
    z = model(t)
    
    # First derivative (Velocity)
    v = torch.autograd.grad(z, t, torch.ones_like(z), create_graph=True)[0]
    
    # Second derivative (Acceleration)
    a = torch.autograd.grad(v, t, torch.ones_like(v), create_graph=True)[0]
    
    return z, v, a

def train_pinn_planner(target_alt=0.0, start_alt=50.0):
    """
    Trains the PINN to find a physically valid landing trajectory.
    Loss = Boundary_Loss + Physics_Loss + Control_Loss
    """
    print(f"🚀 Initializing PINN Trajectory Optimization (PyTorch)")
    print(f"   Objective: Soft-Landing from {start_alt}m to {target_alt}m in {T_END}s")
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TrajectoryPINN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    # Training Loop
    # We sample time points within the domain [0, T_END]
    t_physics = torch.linspace(0, T_END, 100).view(-1, 1).to(device)
    
    for epoch in range(EPOCHS):
        optimizer.zero_grad()
        
        # 1. Forward Pass (Derivatives)
        z, v, a = get_derivatives(model, t_physics)
        
        # 2. Physics & Inverse Dynamics
        # Force Balance: F_net = m*a
        # Thrust = m*(a + g)
        required_thrust = MASS * (a + G)
        
        # 3. Define Losses
        
        # A) Boundary Conditions
        # z(0) = start_alt
        z_start_pred = model(torch.tensor([[0.0]]).to(device))
        loss_bc_start = (z_start_pred - start_alt)**2
        
        # z(T) = target_alt
        z_end_pred = model(torch.tensor([[T_END]]).to(device))
        loss_bc_end = (z_end_pred - target_alt)**2

        # v(T) = 0 (Soft landing)
        _, v_end_pred, _ = get_derivatives(model, torch.tensor([[T_END]]).to(device))
        loss_bc_vel = (v_end_pred - 0.0)**2
        
        # B) Control Constraints (Thrust Limits)
        # We penalize thrust < 0 or > MAX_THRUST
        relu = nn.ReLU()
        loss_control = torch.mean(relu(-required_thrust)) + torch.mean(relu(required_thrust - MAX_THRUST))
        
        # C) Physics Regularization (Minimize Jerk/Energy for smoothness)
        # Minimizing Acceleration^2 helps simulate energy efficiency
        loss_energy = torch.mean(required_thrust**2) * 1e-4

        # Total Loss
        loss = loss_bc_start + loss_bc_end + loss_bc_vel + loss_control + loss_energy
        
        loss.backward()
        optimizer.step()
        
        if epoch % 200 == 0:
            print(f"   Epoch {epoch:04d} | Loss: {loss.item():.6f} | Z_End: {z_end_pred.item():.2f}m")
            
    return model

def run_simulation():
    """Run the trained PINN and simulate the flight."""
    model = train_pinn_planner()
    
    print("\n🎥 Executing Flight Simulation based on PINN Solution...\n")
    print(f"{'Time (s)':<10} | {'Alt (m)':<10} | {'Vel (m/s)':<10} | {'Accel':<10} | {'Thrust (N)':<10} | {'Status':<10}")
    print("-" * 75)
    
    # Generate Plot Data (Grad enabled for physics derivatives)
    t_eval = torch.linspace(0, T_END, 100).view(-1, 1)
    t_eval.requires_grad = True
    z, v, a = get_derivatives(model, t_eval)
    
    # Generate Plot
    print("📊 Generating Trajectory Plot: landing_trajectory.png")
    plt.figure(figsize=(10, 6))
    
    # Plot Altitude
    plt.subplot(3, 1, 1)
    plt.plot(t_eval.numpy(), z.numpy(), 'b-', label='Altitude (m)')
    plt.axhline(y=0.0, color='r', linestyle='--', alpha=0.5)
    plt.title(f"PINN Autonomous Landing Trajectory (Mass={MASS}kg)")
    plt.ylabel("Height (m)")
    plt.grid(True)
    plt.legend()
    
    # Plot Velocity
    plt.subplot(3, 1, 2)
    plt.plot(t_eval.numpy(), v.numpy(), 'g-', label='Velocity (m/s)')
    plt.ylabel("Vel (m/s)")
    plt.grid(True)
    plt.legend()
    
    # Plot Acceleration/Thrust
    plt.subplot(3, 1, 3)
    thrust = MASS * (a.numpy() + G)
    plt.plot(t_eval.numpy(), thrust, 'r-', label='Thrust (N)')
    plt.axhline(y=MAX_THRUST, color='k', linestyle=':', label='Max Thrust')
    plt.xlabel("Time (s)")
    plt.ylabel("Thrust (N)")
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('landing_trajectory.png')
    print("✅ Plot saved.")

    # Re-run for logging (using fewer points)
    t_eval_log = torch.linspace(0, T_END, 20).view(-1, 1)
    t_eval_log.requires_grad = True
    z, v, a = get_derivatives(model, t_eval_log)
    
    for i in range(len(t_eval_log)):
        t_val = t_eval[i].item()
        z_val = z[i].item()
        v_val = v[i].item()
        a_val = a[i].item()
        
        thrust_val = MASS * (a_val + G)
        
        status = "FLIGHT"
        if t_val >= T_END: status = "LANDED"
        if z_val < 0.1: status = "TOUCHDOWN"
        
        print(f"{t_val:<10.2f} | {z_val:<10.2f} | {v_val:<10.2f} | {a_val:<10.2f} | {thrust_val:<10.2f} | {status:<10}")

if __name__ == "__main__":
    # Check dependencies
    try:
        import torch
        run_simulation()
    except ImportError:
        print("CRITICAL: PyTorch not found. Please run 'pip install torch'")
