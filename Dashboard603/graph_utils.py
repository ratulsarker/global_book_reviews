from pyvis.network import Network


def build_recommendation_graph(data):
    """
    Build an interactive graph showing book communities and their shared tags.
    Shows how multiple books connect through common genres/tags.
    """
    
    if not data:
        return None

    # Create network graph
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#2d3748",
        font_color="white",
        directed=False
    )

    added_nodes = set()
    tag_connections = {}
    book_info = {}

    # Collect book and tag information
    for record in data:
        book_title = record["book_title"]
        tag = record["tag"]
        is_main = record["is_main"]
        rating = record.get("rating", 0)
        tag_count = record.get("tag_count", 0)
        
        # Store book info
        if book_title not in book_info:
            book_info[book_title] = {
                'is_main': is_main,
                'rating': rating,
                'tag_count': tag_count,
                'shared_tags': []
            }
        book_info[book_title]['shared_tags'].append(tag)
        
        # Count tag usage
        tag_connections[tag] = tag_connections.get(tag, 0) + 1

    # Add BOOK nodes
    for book, info in book_info.items():
        book_label = book[:40] + "..." if len(book) > 40 else book
        shared_count = len(info['shared_tags'])
        
        if info['is_main']:
            # MAIN BOOK - Blue, larger
            net.add_node(
                book,
                label=f"⭐ {book_label}",
                title=f"📚 YOUR BOOK\n{book}\n━━━━━━━━━━━━\nRating: {info['rating']:.2f}⭐\nTotal Tags: {info['tag_count']}\nShown Tags: {shared_count}",
                color="#3b82f6",
                shape="box",
                size=38,
                font={"size": 16, "color": "#ffffff", "face": "arial", "bold": True},
                borderWidth=4
            )
        else:
            # SIMILAR BOOKS - Green, sized by connections
            size = min(22 + (shared_count * 2), 32)
            net.add_node(
                book,
                label=book_label,
                title=f"📖 SIMILAR BOOK\n{book}\n━━━━━━━━━━━━\nRating: {info['rating']:.2f}⭐\nShared Tags: {shared_count}\nTotal Tags: {info['tag_count']}",
                color="#10b981",
                shape="ellipse",
                size=size,
                font={"size": 13, "color": "#ffffff"},
                borderWidth=2
            )
        added_nodes.add(book)

    # Add TAG nodes - sized by how many books share them
    for tag, connections in tag_connections.items():
        tag_size = min(12 + (connections * 4), 32)
        net.add_node(
            tag,
            label=tag,
            title=f"🏷️ GENRE/TAG\n{tag}\n━━━━━━━━━━━━\n{connections} books with this tag",
            color="#a78bfa",
            shape="dot",
            size=tag_size,
            font={"size": 12, "color": "#ffffff"},
            borderWidth=2
        )

    # Add EDGES (book-to-tag connections)
    for record in data:
        book_title = record["book_title"]
        tag = record["tag"]
        is_main = record["is_main"]
        
        if is_main:
            # Main book connections - thicker, brighter
            net.add_edge(book_title, tag, color="#60a5fa", width=3)
        else:
            # Similar book connections - thinner
            net.add_edge(book_title, tag, color="#94a3b8", width=1.5)

    # Minimal movement - very high damping, physics disabled quickly
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
          "type": "continuous",
          "roundness": 0.5
        }
      },
      "layout": {
        "improvedLayout": true
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -800,
          "centralGravity": 0.01,
          "springLength": 300,
          "springConstant": 0.004,
          "damping": 0.99,
          "avoidOverlap": 1.0
        },
        "stabilization": {
          "enabled": true,
          "iterations": 400,
          "fit": true,
          "updateInterval": 10,
          "onlyDynamicEdges": false
        },
        "adaptiveTimestep": true,
        "maxVelocity": 1
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "navigationButtons": true,
        "keyboard": true,
        "zoomView": true,
        "dragView": true,
        "dragNodes": true
      }
    }
    """)

    return net
