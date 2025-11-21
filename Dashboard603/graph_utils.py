from pyvis.network import Network


def build_recommendation_graph(data):
    """
    Build a beautiful interactive graph for book recommendations.
    Data must contain dictionaries with:
    - main_book
    - tag
    - recommended_book
    """

    # Limit data to prevent overcrowding
    data = data[:20] if len(data) > 20 else data

    # Create network graph with clean dark theme
    net = Network(
        height="700px",
        width="100%",
        bgcolor="#2d3748",  # Clean dark gray
        font_color="white",
        directed=False
    )

    added_nodes = set()
    tag_count = {}

    # Count tag occurrences for sizing
    for record in data:
        tag = record["tag"]
        tag_count[tag] = tag_count.get(tag, 0) + 1

    for record in data:
        main = record["main_book"]
        tag = record["tag"]
        rec = record["recommended_book"]

        # Truncate long titles for readability
        main_label = main[:35] + "..." if len(main) > 35 else main
        rec_label = rec[:35] + "..." if len(rec) > 35 else rec

        # Add MAIN BOOK node (Blue)
        if main not in added_nodes:
            net.add_node(
                main,
                label=main_label,
                title=main,
                color="#3b82f6",  # Clean blue
                shape="box",
                size=28,
                font={"size": 15, "color": "#ffffff", "face": "arial"},
                borderWidth=2
            )
            added_nodes.add(main)

        # Add TAG node (Purple - size based on connections)
        if tag not in added_nodes:
            tag_size = min(12 + (tag_count[tag] * 2), 25)
            net.add_node(
                tag,
                label=tag,
                title=f"{tag} ({tag_count[tag]} connections)",
                color="#8b5cf6",  # Softer purple
                shape="dot",
                size=tag_size,
                font={"size": 12, "color": "#ffffff"},
                borderWidth=1
            )
            added_nodes.add(tag)

        # Add RECOMMENDED BOOK node (Green)
        if rec not in added_nodes:
            net.add_node(
                rec,
                label=rec_label,
                title=rec,
                color="#10b981",  # Clean green
                shape="ellipse",
                size=20,
                font={"size": 13, "color": "#ffffff"},
                borderWidth=2
            )
            added_nodes.add(rec)

        # Add edges with subtle colors
        net.add_edge(main, tag, color="#94a3b8", width=1.5)
        net.add_edge(tag, rec, color="#94a3b8", width=1)

    # Set clean physics options
    net.set_options("""
    {
      "nodes": {
        "font": {
          "size": 14,
          "face": "arial"
        }
      },
      "edges": {
        "smooth": {
          "enabled": true,
          "type": "continuous"
        }
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -30000,
          "centralGravity": 0.3,
          "springLength": 150,
          "springConstant": 0.05,
          "damping": 0.4
        },
        "stabilization": {
          "iterations": 150
        }
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true
      }
    }
    """)

    return net
