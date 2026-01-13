import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Module 15: Synthetic Data Factory (AI Ops)
# -----------------------------------------------------------------------------
# Simulation of a high-throughput pipeline for LLM training data generation.
# Models the "Quality vs Quantity" trade-off and the rejection rates of
# toxic/low-quality synthetic tokens.
# -----------------------------------------------------------------------------

def simulate_data_pipeline():
    """
    Simulate the flow of tokens through a curatorial pipeline:
    Raw Scraping -> De-Duplication -> Quality Filter -> Synthetic Augmentation.
    """
    
    stages = ['Raw Ingest', 'De-Duplication', 'Quality Filter', 'Safety Check', 'Fine-Tuning Ready']
    
    # Volume (Billions of Tokens) - Logarithmic Decay
    volumes = [1000, 450, 120, 115, 12] # Drastic reduction for high quality
    
    # Quality Score (0-100) - Increasing
    quality = [15, 30, 65, 85, 99.5]
    
    # --- Visualization ---
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # Plot 1: Volume Funnel (Bar)
    color = '#2c3e50'
    bars = ax1.bar(stages, volumes, color=color, alpha=0.6, label='Token Volume (Billions)')
    ax1.set_ylabel('Volume (B Tokens)', color=color, fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 1200)
    
    # Add volume labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'{height}B', ha='center', va='bottom', color=color, fontweight='bold')

    # Plot 2: Quality Curve (Line)
    ax2 = ax1.twinx()  # Shared X-axis
    color_line = '#27ae60'
    ax2.plot(stages, quality, color=color_line, linewidth=4, marker='o', markersize=10, label='Data Quality Score')
    ax2.set_ylabel('Quality Score (0-100)', color=color_line, fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color_line)
    ax2.set_ylim(0, 110)
    
    # Title & Layout
    plt.title("Synthetic Data Factory: The 'Quality vs Quantity' Funnel", fontsize=16, fontweight='bold')
    ax1.grid(True, axis='y', alpha=0.3)
    
    # Annotations
    plt.annotate('Gold Standard\n(Sovereign CoT Data)', 
                 xy=(4, 99.5), xycoords='data',
                 xytext=(3, 80), textcoords='data',
                 arrowprops=dict(facecolor='black', shrink=0.05))

    filename = 'data_pipeline.png'
    plt.savefig(filename, dpi=300)
    print(f"Generated {filename}")

if __name__ == "__main__":
    print("Running Synthetic Data Factory Simulation...")
    simulate_data_pipeline()
