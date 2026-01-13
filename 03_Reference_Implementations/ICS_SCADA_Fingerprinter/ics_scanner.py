import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from dataclasses import dataclass
from typing import List, Dict

# -----------------------------------------------------------------------------
# Module 08: ICS/SCADA Fingerprinter (Modbus/DNP3)
# -----------------------------------------------------------------------------
# Simulation of Industrial Control Systems network discovery.
# Models hierarchical SCADA topology and Modbus protocol anomalies.
# -----------------------------------------------------------------------------

@dataclass
class ICSDevice:
    ip: str
    role: str # 'MASTER', 'PLC', 'HMI', 'SENSOR'
    protocol: str # 'MODBUS', 'DNP3'
    risk_score: float

def simulate_ics_network(num_plc: int = 15):
    """
    Simulate a SCADA network topology and visualize risk levels.
    """
    G = nx.Graph()
    
    # Core Infrastructure
    master_node = "SCADA_MASTER (10.0.0.1)"
    historian = "HISTORIAN (10.0.0.2)"
    hmi = "HMI_Console (10.0.0.5)"
    
    G.add_node(master_node, role='MASTER', risk=0.1)
    G.add_node(historian, role='DB', risk=0.2)
    G.add_node(hmi, role='HMI', risk=0.4)
    
    G.add_edge(master_node, historian)
    G.add_edge(master_node, hmi)
    
    devices = []
    
    # Generate PLCs (Programmable Logic Controllers)
    for i in range(num_plc):
        plc_id = f"PLC_{i:02d}"
        
        # Simulate vulnerabilities (e.g., default credentials, open ports)
        # Risk score 0.0 (Safe) to 1.0 (Critical)
        risk = np.random.beta(2, 5) 
        if i % 5 == 0: risk += 0.4 # Inject simulated critical flaws
        
        protocol = "MODBUS" if np.random.random() > 0.3 else "DNP3"
        
        G.add_node(plc_id, role='PLC', risk=risk, protocol=protocol)
        G.add_edge(master_node, plc_id)
        
        # Add sensors behind PLCs
        for j in range(np.random.randint(1, 4)):
            sensor_id = f"IO_{i}_{j}"
            G.add_node(sensor_id, role='SENSOR', risk=0.0)
            G.add_edge(plc_id, sensor_id)

    # --- Visualization ---
    plt.figure(figsize=(14, 10))
    
    pos = nx.spring_layout(G, seed=42, k=0.5)
    
    # Draw Nodes based on Risk
    risks = [G.nodes[n].get('risk', 0) for n in G.nodes()]
    
    # Color map: Green (Safe) -> Red (Critical)
    nodes = nx.draw_networkx_nodes(G, pos, node_size=800, 
                                 node_color=risks, cmap='RdYlGn_r', 
                                 alpha=0.9, vmin=0, vmax=1.0)
    
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    
    plt.title("ICS/SCADA Network Topology & Vulnerability Heatmap", fontsize=15, fontweight='bold')
    plt.colorbar(nodes, label='Vulnerability Risk Score (CVE-Based)')
    plt.axis('off')
    
    # Add Legend
    plt.text(0.95, 0.05, "Protocol: Modbus/TCP & DNP3", transform=plt.gca().transAxes, 
             fontsize=10, verticalalignment='bottom', horizontalalignment='right', 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    filename = 'ics_topology.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Generated {filename}")

if __name__ == "__main__":
    print("Running ICS/SCADA Network Scanner...")
    simulate_ics_network()
