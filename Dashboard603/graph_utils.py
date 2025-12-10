from pyvis.network import Network
import math


def build_recommendation_graph(data, physics_settings=None):
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

    # Add MAIN BOOK first to ensure it's prominent
    main_book = None
    for book, info in book_info.items():
        if info['is_main']:
            main_book = book
            break
    
    # Add MAIN BOOK first (most prominent) - at center
    if main_book:
        info = book_info[main_book]
        book_label = main_book[:35] + "..." if len(main_book) > 35 else main_book
        shared_count = len(info['shared_tags'])
        
        # MAIN BOOK - Blue, at center (0, 0)
        net.add_node(
            main_book,
            label=f"[SELECTED] {book_label}",
            title=f"YOUR SELECTED BOOK\n{main_book}\n\nRating: {info['rating']:.2f}\nTotal Tags: {info['tag_count']}\nShown Tags: {shared_count}\n\nThis book is used to find similar books via shared tags.",
            color="#2563eb",
            shape="box",
            size=70,
            font={"size": 20, "color": "#ffffff", "face": "arial", "bold": True},
            borderWidth=6,
            x=0,
            y=0,
            fixed=False
        )
        added_nodes.add(main_book)
    
    # Add SIMILAR BOOKS - positioned in a CIRCLE around center
    similar_books = [b for b, info in book_info.items() if not info['is_main']]
    num_books = len(similar_books)
    radius = 400  # Distance from center
    
    for i, book in enumerate(similar_books):
        info = book_info[book]
        book_label = book[:40] + "..." if len(book) > 40 else book
        shared_count = len(info['shared_tags'])
        
        # Calculate position on circle
        angle = (2 * math.pi * i) / max(num_books, 1)
        x_pos = int(radius * math.cos(angle))
        y_pos = int(radius * math.sin(angle))
        
        # SIMILAR BOOKS - Green, spread in circle
        size = min(30 + (shared_count * 2), 45)
        net.add_node(
            book,
            label=book_label,
            title=f"SIMILAR BOOK\n{book}\n\nRating: {info['rating']:.2f}\nShared Tags: {shared_count}\nTotal Tags: {info['tag_count']}",
            color="#10b981",
            shape="ellipse",
            size=size,
            font={"size": 15, "color": "#ffffff"},
            borderWidth=3,
            x=x_pos,
            y=y_pos,
            fixed=False
        )
        added_nodes.add(book)

    # Add TAG nodes - sized by how many books share them
    for tag, connections in tag_connections.items():
        tag_size = min(12 + (connections * 4), 32)
        net.add_node(
            tag,
            label=tag,
            title=f"TAG: {tag}\n\n{connections} books with this tag",
            color="#D4A84B",  # Orange to match poster theme
            shape="dot",
            size=tag_size,
            font={"size": 12, "color": "#333333"},
            borderWidth=2
        )

    # Add EDGES (book-to-tag connections)
    for record in data:
        book_title = record["book_title"]
        tag = record["tag"]
        is_main = record["is_main"]
        
        if is_main:
            # Main book connections - MUCH thicker, brighter, more visible
            net.add_edge(book_title, tag, color="#3b82f6", width=5)  # Thicker and brighter
        else:
            # Similar book connections - thinner
            net.add_edge(book_title, tag, color="#94a3b8", width=1.5)

    # Use provided physics settings or defaults
    if physics_settings is None:
        physics_settings = {
            'repulsion': 2000,
            'spring': 150,
            'damping': 0.9,
            'central': 0.3
        }
    
    # Build physics options - use repulsion solver for better node separation
    options = f"""
    {{
      "nodes": {{
        "font": {{
          "size": 14,
          "face": "arial"
        }},
        "scaling": {{
          "min": 10,
          "max": 70
        }}
      }},
      "edges": {{
        "smooth": {{
          "enabled": true,
          "type": "continuous",
          "roundness": 0.5
        }}
      }},
      "layout": {{
        "improvedLayout": true
      }},
      "physics": {{
        "enabled": true,
        "solver": "repulsion",
        "repulsion": {{
          "nodeDistance": {physics_settings['spring'] + 100},
          "centralGravity": {physics_settings['central']},
          "springLength": {physics_settings['spring']},
          "springConstant": 0.05,
          "damping": {physics_settings['damping']}
        }},
        "stabilization": {{
          "enabled": true,
          "iterations": 1000,
          "fit": true
        }},
        "maxVelocity": 20,
        "minVelocity": 0.5
      }},
      "interaction": {{
        "hover": true,
        "tooltipDelay": 100,
        "navigationButtons": true,
        "keyboard": true,
        "zoomView": true,
        "dragView": true,
        "dragNodes": true
      }}
    }}
    """
    net.set_options(options)

    return net
