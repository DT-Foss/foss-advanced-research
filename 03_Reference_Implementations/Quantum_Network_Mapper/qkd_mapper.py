import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------------------------------------------------------
# Module 09: Quantum Network Mapper (QKD)
# -----------------------------------------------------------------------------
# Simulation of a Quantum Key Distribution (QKD) backbone.
# Models Trusted Nodes and Quantum Channel attenuation over optical fiber.
# -----------------------------------------------------------------------------

def simulate_qkd_network():
    """
    Simulate QKD Key Rates across a metropolitan quantum network.
    Physics: Attenuation in optical fiber (0.2 dB/km).
    """
    G = nx.Graph()
    
    # Define Quantum Nodes (Cities/Hubs)
    cities = {
        'Geneva': (0, 0),
        'Lausanne': (50, 10),
        'Bern': (80, 60),
        'Zurich': (120, 50),
        'Basel': (70, 90)
    }
    
    G.add_nodes_from(cities.keys())
    
    # Define Physical Links (Fiber optic cables)
    links = [
        ('Geneva', 'Lausanne', 60), # 60km
        ('Lausanne', 'Bern', 90),
        ('Bern', 'Zurich', 120),
        ('Bern', 'Basel', 80),
        ('Zurich', 'Basel', 85)
    ]
    
    for u, v, dist in links:
        # Calculate Secure Key Rate (SKR)
        # SKR ~ 10^(-Loss/10)
        # Fiber loss @ 1550nm = 0.2 dB/km
        loss_db = 0.2 * dist
        # Baseline rate 10 Mbps at 0km, decreases exponentially
        skr_kbps = 10000 * (10 ** (-loss_db / 10))
        
        G.add_edge(u, v, weight=dist, skr=skr_kbps)

    # --- Visualization ---
    plt.figure(figsize=(12, 8))
    
    pos = cities
    
    # Draw Nodes (Trusted Nodes)
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='#2c3e50', alpha=1.0)
    nx.draw_networkx_labels(G, pos, font_color='white', font_size=10, font_weight='bold')
    
    # Draw Edges (Quantum Channels)
    edges = G.edges(data=True)
    weights = [np.log10(d['skr']) for u, v, d in edges] # Thickness by key rate (log scale)
    
    nx.draw_networkx_edges(G, pos, width=weights, edge_color='#8e44ad', alpha=0.8)
    
    # Edge Labels (Key Rates)
    edge_labels = { (u,v): f"{d['skr']:.1f} kbps\n({d['weight']}km)" for u,v,d in edges }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    
    plt.title("Quantum Key Distribution (QKD) Network Backbone", fontsize=15, fontweight='bold')
    plt.suptitle("Secure Key Rate (SKR) vs Fiber Attenuation (0.2 dB/km)", fontsize=10, y=0.92)
    plt.axis('off')
    
    # Annotations
    plt.text(0.05, 0.05, "Protocol: BB84 Decoy State", transform=plt.gca().transAxes,
             fontsize=10, color='gray', fontstyle='italic')

    filename = 'qkd_topology.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Generated {filename}")

if __name__ == "__main__":
    print("Running QKD Network Mapper...")
    simulate_qkd_network()
