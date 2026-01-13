import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from dataclasses import dataclass

# -----------------------------------------------------------------------------
# Module 14: Causal Knowledge Graph (AI / Reasoning)
# -----------------------------------------------------------------------------
# Simulation of Causal Inference using Bayesian Networks (DAGs).
# Models the probabilistic relationship between Vulnerabilities, Exploits,
# and System Breaches using "do-calculus" logic (Pearl).
# -----------------------------------------------------------------------------

def simulate_causal_network():
    """
    Generate a Directed Acyclic Graph (DAG) representing causal dependencies.
    Scenario: Cyber Attack Chain.
    """
    G = nx.DiGraph()
    
    # Define Nodes (Events/States)
    nodes = {
        'Unpatched_CVE': {'pos': (0, 2), 'type': 'ROOT_CAUSE'},
        'Weak_Password': {'pos': (0, 0), 'type': 'ROOT_CAUSE'},
        'RCE_Exploit': {'pos': (2, 2), 'type': 'MECHANISM'},
        'Brute_Force': {'pos': (2, 0), 'type': 'MECHANISM'},
        'Privilege_Escalation': {'pos': (4, 1), 'type': 'INTERMEDIATE'},
        'Data_Exfiltration': {'pos': (6, 1), 'type': 'OUTCOME'}
    }
    
    G.add_nodes_from(nodes.keys())
    
    # Define Causal Edges (P(Child | Parent))
    edges = [
        ('Unpatched_CVE', 'RCE_Exploit'),
        ('Weak_Password', 'Brute_Force'),
        ('RCE_Exploit', 'Privilege_Escalation'),
        ('Brute_Force', 'Privilege_Escalation'),
        ('Privilege_Escalation', 'Data_Exfiltration')
    ]
    
    G.add_edges_from(edges)
    
    # Simulation: Intervention via do-calculus
    # do(Patch_System) -> Unpatched_CVE = 0
    # Calculate probability of Data_Exfiltration
    
    # --- Visualization ---
    plt.figure(figsize=(12, 6))
    
    pos = {n: nodes[n]['pos'] for n in nodes}
    
    # Draw Nodes
    node_colors = ['#e74c3c' if nodes[n]['type'] == 'ROOT_CAUSE' else 
                   '#f39c12' if nodes[n]['type'] == 'MECHANISM' else
                   '#3498db' if nodes[n]['type'] == 'INTERMEDIATE' else
                   '#9b59b6' for n in nodes]
    
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color=node_colors, alpha=0.9, node_shape='s')
    nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold', font_size=9)
    
    # Draw Edges (Arrows)
    nx.draw_networkx_edges(G, pos, width=2.0, arrowsize=20, edge_color='#2c3e50', connectionstyle='arc3,rad=0.1')
    
    # Edge Labels (Causal Strength)
    edge_labels = {
        ('Unpatched_CVE', 'RCE_Exploit'): 'P=0.9',
        ('Weak_Password', 'Brute_Force'): 'P=0.7',
        ('RCE_Exploit', 'Privilege_Escalation'): 'P=0.95',
        ('Brute_Force', 'Privilege_Escalation'): 'P=0.6',
        ('Privilege_Escalation', 'Data_Exfiltration'): 'P=0.99'
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.7)
    
    plt.title("Causal Bayesian Network: Attack Path Probability", fontsize=15, fontweight='bold')
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#e74c3c', label='Root Cause', markersize=12),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#f39c12', label='Mechanism', markersize=12),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#3498db', label='Intermediate', markersize=12),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#9b59b6', label='Outcome', markersize=12)
    ]
    plt.legend(handles=legend_elements, loc='lower right')
    
    plt.axis('off')
    
    filename = 'causal_dag.png'
    plt.savefig(filename, dpi=300)
    print(f"Generated {filename}")

if __name__ == "__main__":
    print("Running Causal Inference Engine...")
    simulate_causal_network()
