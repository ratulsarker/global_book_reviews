#!/usr/bin/env python3
"""
Simple ASCII and Mermaid diagram generator for System Architecture
No external dependencies required - uses matplotlib for visualization
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch
import matplotlib.patches as mpatches

def create_architecture_diagram():
    """Create a visual architecture diagram using matplotlib."""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Colors
    user_color = '#4A90E2'
    app_color = '#50C878'
    mysql_color = '#F7931E'
    neo4j_color = '#008CC1'
    data_color = '#9B59B6'
    
    # Title
    ax.text(5, 10.5, 'Goodbooks Analytics Platform', 
            ha='center', fontsize=18, fontweight='bold')
    ax.text(5, 10.1, 'System Architecture', 
            ha='center', fontsize=14, style='italic')
    
    # User Layer - Larger
    user_box = FancyBboxPatch((3, 8.5), 4, 1, 
                             boxstyle="round,pad=0.15", 
                             facecolor=user_color, 
                             edgecolor='black', linewidth=2.5)
    ax.add_patch(user_box)
    ax.text(5, 9, 'End Users', ha='center', va='center', 
            fontsize=16, fontweight='bold', color='white')
    
    # Application Layer - Larger, simpler
    app_box = FancyBboxPatch((2, 6.5), 6, 1.5, 
                            boxstyle="round,pad=0.15", 
                            facecolor=app_color, 
                            edgecolor='black', linewidth=2.5)
    ax.add_patch(app_box)
    ax.text(5, 7.5, 'Streamlit Dashboard', ha='center', va='center', 
            fontsize=16, fontweight='bold', color='white')
    ax.text(5, 7, 'Python Web Application', 
            ha='center', va='center', fontsize=12, color='white')
    
    # MySQL Database - Larger, simpler
    mysql_box = FancyBboxPatch((0.5, 3.5), 4, 2, 
                               boxstyle="round,pad=0.15", 
                               facecolor=mysql_color, 
                               edgecolor='black', linewidth=2.5)
    ax.add_patch(mysql_box)
    ax.text(2.5, 5, 'MySQL', ha='center', va='center', 
            fontsize=18, fontweight='bold', color='white')
    ax.text(2.5, 4.5, 'Relational Database', ha='center', va='center', 
            fontsize=14, color='white')
    ax.text(2.5, 4, 'Port: 3306', ha='center', va='center', 
            fontsize=12, color='white')
    
    # Neo4j Database - Larger, simpler
    neo4j_box = FancyBboxPatch((5.5, 3.5), 4, 2, 
                              boxstyle="round,pad=0.15", 
                              facecolor=neo4j_color, 
                              edgecolor='black', linewidth=2.5)
    ax.add_patch(neo4j_box)
    ax.text(7.5, 5, 'Neo4j', ha='center', va='center', 
            fontsize=18, fontweight='bold', color='white')
    ax.text(7.5, 4.5, 'Graph Database', ha='center', va='center', 
            fontsize=14, color='white')
    ax.text(7.5, 4, 'Port: 7687', ha='center', va='center', 
            fontsize=12, color='white')
    
    # Data Sources - Simplified
    data_box = FancyBboxPatch((3.5, 0.5), 3, 1.5, 
                             boxstyle="round,pad=0.15", 
                             facecolor=data_color, 
                             edgecolor='black', linewidth=2.5)
    ax.add_patch(data_box)
    ax.text(5, 1.5, 'CSV Data', ha='center', va='center', 
            fontsize=14, fontweight='bold', color='white')
    ax.text(5, 1, 'Source Files', ha='center', va='center', 
            fontsize=12, color='white')
    
    # Arrows - Start/end just outside box boundaries to avoid visual overlap
    # User box: (3, 8.5) to (7, 9.5) - bottom edge at y=8.5
    # App box: (2, 6.5) to (8, 8) - top edge at y=8
    # User to App - Vertical: from just below user to just above app
    arrow1 = FancyArrowPatch((5, 8.45), (5, 8.05), 
                            arrowstyle='->', mutation_scale=25, 
                            color='#333333', linewidth=3)
    ax.add_patch(arrow1)
    ax.text(5.6, 8.2, 'HTTP\nPort: 8501', fontsize=10, color='#333333', 
            fontweight='bold', va='center')
    
    # App box: left edge at x=2, right edge at x=8, center y=7.25
    # MySQL box: (0.5, 3.5) to (4.5, 5.5) - top edge at y=5.5, center x=2.5
    # App to MySQL - from just left of app to just above MySQL
    arrow2 = FancyArrowPatch((1.95, 7.25), (2.5, 5.55), 
                             arrowstyle='->', mutation_scale=25, 
                             color='#333333', linewidth=3)
    ax.add_patch(arrow2)
    ax.text(1.3, 6.2, 'SQL Queries\nSQLAlchemy\n+ PyMySQL', fontsize=9, color='#333333', 
            fontweight='bold', ha='right', va='center')
    
    # Neo4j box: (5.5, 3.5) to (9.5, 5.5) - top edge at y=5.5, center x=7.5
    # App to Neo4j - from just right of app to just above Neo4j
    arrow3 = FancyArrowPatch((8.05, 7.25), (7.5, 5.55), 
                            arrowstyle='->', mutation_scale=25, 
                            color='#333333', linewidth=3)
    ax.add_patch(arrow3)
    ax.text(8.7, 6.2, 'Cypher Queries\nNeo4j Driver\nBolt Protocol', fontsize=9, color='#333333', 
            fontweight='bold', ha='left', va='center')
    
    # Data box: (3.5, 0.5) to (6.5, 2) - top edge at y=2, center x=5
    # MySQL box: bottom edge at y=3.5
    # Data to MySQL - from just above data to just below MySQL
    arrow4 = FancyArrowPatch((4, 2.05), (1.5, 3.45), 
                            arrowstyle='->', mutation_scale=20, 
                            color='#666666', linewidth=2, linestyle='--')
    ax.add_patch(arrow4)
    ax.text(2.3, 2.5, 'Data Import\nCSV Files', fontsize=9, color='#666666', 
            fontweight='bold', ha='center', va='center')
    
    # Neo4j box: bottom edge at y=3.5
    # Data to Neo4j - from just above data to just below Neo4j
    arrow5 = FancyArrowPatch((6, 2.05), (8.5, 3.45), 
                            arrowstyle='->', mutation_scale=20, 
                            color='#666666', linewidth=2, linestyle='--')
    ax.add_patch(arrow5)
    ax.text(7.7, 2.5, 'Data Import\nDump File', fontsize=9, color='#666666', 
            fontweight='bold', ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig('system_architecture.png', dpi=300, bbox_inches='tight')
    plt.savefig('system_architecture.pdf', bbox_inches='tight')
    print("✅ Architecture diagram saved as:")
    print("   - system_architecture.png (high resolution)")
    print("   - system_architecture.pdf (vector format)")

if __name__ == "__main__":
    create_architecture_diagram()

