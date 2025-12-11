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
        
        # MAIN BOOK - Blue, at center (0, 0), can move but starts centered
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
            fixed=False  # Can move but starts at center
        )
        added_nodes.add(main_book)
    
    # Add SIMILAR BOOKS - positioned in a LARGER CIRCLE for good initial separation
    similar_books = [b for b, info in book_info.items() if not info['is_main']]
    num_books = len(similar_books)
    # Larger radius for good initial separation, but allows physics to adjust
    radius = 900 if num_books > 5 else 700
    
    for i, book in enumerate(similar_books):
        info = book_info[book]
        book_label = book[:40] + "..." if len(book) > 40 else book
        shared_count = len(info['shared_tags'])
        
        # Calculate position on circle - spread evenly
        angle = (2 * math.pi * i) / max(num_books, 1)
        x_pos = int(radius * math.cos(angle))
        y_pos = int(radius * math.sin(angle))
        
        # SIMILAR BOOKS - Green, spread in circle, can move but start separated
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
            fixed=False  # Can move but starts in good position
        )
        added_nodes.add(book)

    # Add TAG nodes - positioned in multiple outer rings for better separation
    tag_list = list(tag_connections.items())
    num_tags = len(tag_list)
    
    # Use multiple rings to distribute tags better
    rings = 3
    tags_per_ring = max(1, num_tags // rings)
    
    for idx, (tag, connections) in enumerate(tag_list):
        tag_size = min(12 + (connections * 4), 32)
        
        # Distribute tags across multiple rings to prevent clustering
        if num_tags > 0:
            ring_num = min(idx // tags_per_ring, rings - 1)
            tag_idx_in_ring = idx % tags_per_ring
            tags_in_this_ring = min(tags_per_ring, num_tags - ring_num * tags_per_ring)
            
            # Calculate angle within the ring
            tag_angle = (2 * math.pi * tag_idx_in_ring) / max(tags_in_this_ring, 1)
            
            # Each ring is progressively further out
            tag_radius = radius * 1.8 + (ring_num * 400) + (idx % 5) * 50
            tag_x = int(tag_radius * math.cos(tag_angle))
            tag_y = int(tag_radius * math.sin(tag_angle))
        else:
            tag_x = None
            tag_y = None
        
        # Build node parameters - tags are NOT fixed so they can adjust slightly
        node_kwargs = {
            'label': tag,
            'title': f"TAG: {tag}\n\n{connections} books with this tag",
            'color': "#D4A84B",  # Orange to match poster theme
            'shape': "dot",
            'size': tag_size,
            'font': {"size": 12, "color": "#333333"},
            'borderWidth': 2
        }
        
        # Set initial position to help with layout
        if tag_x is not None and tag_y is not None:
            node_kwargs['x'] = tag_x
            node_kwargs['y'] = tag_y
        
        net.add_node(tag, **node_kwargs)

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
            'repulsion': 6000,  # High for separation but allows movement
            'spring': 350,       # Good spacing
            'damping': 0.95,     # Higher damping to reduce jitter and shaking
            'central': 0.05     # Small central pull to keep graph centered
        }
    
    # Calculate better node distance based on number of nodes
    total_nodes = len(book_info) + len(tag_connections)
    # Good node distance for separation while allowing movement
    node_distance = max(physics_settings['spring'] + 200, 500)
    
    # Build physics options - use barnesHut solver which is better for many nodes
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
        }},
        "mass": 1
      }},
      "edges": {{
        "smooth": {{
          "enabled": true,
          "type": "continuous",
          "roundness": 0.3
        }},
        "length": {node_distance * 0.6},
        "width": 1
      }},
      "layout": {{
        "improvedLayout": true,
        "hierarchical": {{
          "enabled": false
        }}
      }},
      "physics": {{
        "enabled": true,
        "solver": "barnesHut",
        "barnesHut": {{
          "gravitationalConstant": -{physics_settings['repulsion']},
          "centralGravity": {physics_settings['central']},
          "springLength": {physics_settings['spring']},
          "springConstant": 0.005,
          "damping": {physics_settings['damping']},
          "avoidOverlap": 1
        }},
        "stabilization": {{
          "enabled": true,
          "iterations": 2500,
          "fit": true,
          "onlyDynamicEdges": false
        }},
        "maxVelocity": 25,
        "minVelocity": 0.5,
        "timestep": 0.35
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
