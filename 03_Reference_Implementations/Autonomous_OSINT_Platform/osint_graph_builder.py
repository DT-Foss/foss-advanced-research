import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import argparse
import unittest
import sys

# -----------------------------------------------------------------------------
# Module 13: Autonomous OSINT Platform (Intelligence)
# -----------------------------------------------------------------------------
# Simulation of Entity Resolution and Link Analysis for Open Source Intelligence.
# Builds a Knowledge Graph from unstructured data fragments to identify
# hidden relationships between actors (Schein-Identities).
# -----------------------------------------------------------------------------

class OSINTGraph:
    def __init__(self, num_shell_entities=10):
        self.G = nx.Graph()
        self.num_shells = num_shell_entities

    def build_graph(self):
        """Construct the intelligence graph."""
        # Core Targets
        targets = ["Target_Alpha", "Target_Bravo"]
        self.G.add_nodes_from(targets, type='PERSON', color='#e74c3c')
        
        # Shell Companies
        companies = ["Global_Logistics_Ltd", "Oceanic_Holdings_Inc", "Quantum_Ventures"]
        self.G.add_nodes_from(companies, type='COMPANY', color='#3498db')
        
        # Assets
        assets = ["Offshore_Account_KY", "Yacht_Marina_Monaco", "Crypto_Wallet_BTC"]
        self.G.add_nodes_from(assets, type='ASSET', color='#f1c40f')
        
        # Relationships
        self.G.add_edge("Target_Alpha", "Global_Logistics_Ltd", relation="Director")
        self.G.add_edge("Global_Logistics_Ltd", "Offshore_Account_KY", relation="Beneficiary")
        self.G.add_edge("Target_Bravo", "Quantum_Ventures", relation="Investor")
        self.G.add_edge("Target_Alpha", "Quantum_Ventures", relation="Co-Founder")
        self.G.add_edge("Target_Alpha", "Yacht_Marina_Monaco", relation="Geotag_Match")
        self.G.add_edge("Target_Bravo", "Yacht_Marina_Monaco", relation="Geotag_Match")
        
        # Synthetic clutter
        for i in range(self.num_shells):
            node_id = f"Shell_Entity_{i:02d}"
            self.G.add_node(node_id, type='SHELL', color='#95a5a6')
            target = np.random.choice(companies + targets)
            self.G.add_edge(node_id, target, relation="Frequent_Interaction")

    def visualize(self, output_file='knowledge_graph.png'):
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(self.G, seed=42, k=0.6, iterations=50)
        
        colors = [self.G.nodes[n].get('color', 'gray') for n in self.G.nodes()]
        node_sizes = [2000 if self.G.nodes[n].get('type') in ['PERSON', 'COMPANY'] else 800 for n in self.G.nodes()]
        
        nx.draw_networkx_nodes(self.G, pos, node_color=colors, node_size=node_sizes, alpha=0.9)
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_weight='bold')
        
        nx.draw_networkx_edges(self.G, pos, edge_color='#7f8c8d', width=1.5, alpha=0.6)
        
        edge_labels = nx.get_edge_attributes(self.G, 'relation')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=7)
        
        plt.title(f"OSINT Knowledge Graph ({self.G.number_of_nodes()} Entities)", fontsize=16, fontweight='bold')
        
        # Legend (simplified)
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c', label='Target', markersize=10),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498db', label='Company', markersize=10),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#f1c40f', label='Asset', markersize=10)
        ]
        plt.legend(handles=legend_elements, loc='upper left')
        plt.axis('off')
        
        plt.savefig(output_file, dpi=300)
        print(f"Generated {output_file}")

# --- UNIT TESTS ---
class TestOSINTGraph(unittest.TestCase):
    def test_graph_construction(self):
        engine = OSINTGraph(num_shell_entities=5)
        engine.build_graph()
        # 2 Targets + 3 Companies + 3 Assets + 5 Shells = 13 Nodes
        self.assertEqual(engine.G.number_of_nodes(), 13)
        self.assertTrue(engine.G.has_edge("Target_Alpha", "Global_Logistics_Ltd"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Autonomous OSINT Graph Builder')
    parser.add_argument('--shells', type=int, default=10, help='Number of synthetic shell entities')
    parser.add_argument('--test', action='store_true', help='Run unit tests')
    args = parser.parse_args()

    if args.test:
        sys.argv = [sys.argv[0]]
        unittest.main()
    else:
        print(f"Building OSINT Graph with {args.shells} shell entities...")
        engine = OSINTGraph(num_shell_entities=args.shells)
        engine.build_graph()
        engine.visualize()
