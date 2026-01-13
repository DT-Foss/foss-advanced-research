import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from dataclasses import dataclass
from typing import List

# -----------------------------------------------------------------------------
# Module 13: Autonomous OSINT Platform (Intelligence)
# -----------------------------------------------------------------------------
# Simulation of Entity Resolution and Link Analysis for Open Source Intelligence.
# Builds a Knowledge Graph from unstructured data fragments to identify
# hidden relationships between actors (Schein-Identities).
# -----------------------------------------------------------------------------

def simulate_intelligence_graph():
    """
    Generate a Knowledge Graph connecting targets, assets, and communications.
    Uses 'Force-Directed Layout' to cluster related entities.
    """
    G = nx.Graph()
    
    # Core Targets (The "Center" of the investigation)
    targets = ["Target_Alpha", "Target_Bravo"]
    G.add_nodes_from(targets, type='PERSON', color='#e74c3c')
    
    # Shell Companies (The "mask")
    companies = ["Global_Logistics_Ltd", "Oceanic_Holdings_Inc", "Quantum_Ventures"]
    G.add_nodes_from(companies, type='COMPANY', color='#3498db')
    
    # Add Assets (The "proof")
    assets = ["Offshore_Account_KY", "Yacht_Marina_Monaco", "Crypto_Wallet_BTC"]
    G.add_nodes_from(assets, type='ASSET', color='#f1c40f')
    
    # Add Connections (The "Intel")
    # Alpha owns Logistics -> owns Account
    G.add_edge("Target_Alpha", "Global_Logistics_Ltd", relation="Director")
    G.add_edge("Global_Logistics_Ltd", "Offshore_Account_KY", relation="Beneficiary")
    
    # Bravo connected to Ventures -> connected to Alpha
    G.add_edge("Target_Bravo", "Quantum_Ventures", relation="Investor")
    G.add_edge("Target_Alpha", "Quantum_Ventures", relation="Co-Founder")
    
    # Shared Assets
    G.add_edge("Target_Alpha", "Yacht_Marina_Monaco", relation="Geotag_Match")
    G.add_edge("Target_Bravo", "Yacht_Marina_Monaco", relation="Geotag_Match")
    
    # Add synthetic sub-network of shell entities
    for i in range(10):
        node_id = f"Shell_Entity_{i:02d}"
        G.add_node(node_id, type='SHELL', color='#95a5a6')
        # Randomly link to main nodes
        target = np.random.choice(companies + targets)
        G.add_edge(node_id, target, relation="Frequent_Interaction")

    # --- Visualization ---
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, seed=42, k=0.6, iterations=50)
    
    # Draw Nodes by Type
    colors = [G.nodes[n]['color'] for n in G.nodes()]
    node_sizes = [2000 if G.nodes[n]['type'] in ['PERSON', 'COMPANY'] else 800 for n in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=node_sizes, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', font_color='black')
    
    # Draw Edges
    nx.draw_networkx_edges(G, pos, edge_color='#7f8c8d', width=1.5, alpha=0.6)
    
    # Edge Labels (Relationship Types)
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    
    plt.title("OSINT Knowledge Graph: Entity Resolution & Link Analysis", fontsize=16, fontweight='bold')
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c', label='Target (Person)', markersize=10),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498db', label='Front Company', markersize=10),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#f1c40f', label='Asset / Account', markersize=10),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#95a5a6', label='Associated Entity', markersize=10)
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    plt.axis('off')
    
    filename = 'knowledge_graph.png'
    plt.savefig(filename, dpi=300)
    print(f"Generated {filename}")

if __name__ == "__main__":
    print("Running OSINT Graph Builder...")
    simulate_intelligence_graph()
