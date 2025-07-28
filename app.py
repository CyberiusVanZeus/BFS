# Import necessary libraries for Flask web app, graph processing, and plotting
from flask import Flask, render_template, request, redirect, url_for
from collections import deque
import networkx as nx
import matplotlib

# Use non-GUI backend for rendering matplotlib graphs in server-side environment
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json

app = Flask(__name__)

# Global variables to hold graph structure, BFS traversal order, and node levels
graph = {}
bfs_result = []
bfs_levels = {}

@app.route('/')
def index():
    # If graph image exists, provide path for rendering on the web page
    image_url = url_for('static', filename='graph.png') if os.path.exists("static/graph.png") else None
    return render_template(
        "index.html",
        graph=graph,
        bfs_result=bfs_result,
        bfs_levels=bfs_levels,
        image_url=image_url,
        graph_json=json.dumps(graph)  # Send graph data to the frontend as JSON for vis.js rendering
    )

@app.route('/submit', methods=['POST'])
def submit():
    # Clear previous inputs/results
    global graph, bfs_result, bfs_levels
    graph.clear()
    bfs_result.clear()
    bfs_levels.clear()

    # Retrieve graph data and start node from the submitted form
    raw_data = request.form['graph_data']
    start_node = request.form['start_node'].strip()

    # Parse input into graph dictionary (adjacency list format)
    for line in raw_data.strip().split('\n'):
        if ':' not in line:
            continue
        node, neighbors = line.split(':', 1)
        node = node.strip()
        neighbors = [n.strip() for n in neighbors.strip().split()] if neighbors.strip() else []
        graph[node] = neighbors

    # Validate that start node exists in the graph
    if start_node not in graph:
        return redirect(url_for('index'))

    # Breadth-First Search (BFS) algorithm
    visited = set()
    queue = deque([(start_node, 0)])  # Each queue item holds a (node, level)

    while queue:
        node, level = queue.popleft()
        if node not in visited:
            visited.add(node)
            bfs_result.append(node)
            bfs_levels[node] = level
            for neighbor in graph.get(node, []):
                if neighbor not in visited and neighbor not in [q[0] for q in queue]:
                    queue.append((neighbor, level + 1))

    # Generate and save static graph image
    draw_graph()
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    # Clear all global data and delete graph image
    global graph, bfs_result, bfs_levels
    graph.clear()
    bfs_result.clear()
    bfs_levels.clear()
    if os.path.exists("static/graph.png"):
        os.remove("static/graph.png")
    return redirect(url_for('index'))

def draw_graph():
    # Use NetworkX to build a directed graph
    G = nx.DiGraph()
    for u, neighbors in graph.items():
        for v in neighbors:
            G.add_edge(u, v)

    # Generate positions for graph nodes
    pos = nx.spring_layout(G, seed=42)

    # Initialize plot
    plt.figure(figsize=(8, 6))

    # Draw nodes and all edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, arrowsize=20)

    # Highlight BFS tree edges in red based on BFS levels
    bfs_edges = [(u, v) for u, neighbors in graph.items() for v in neighbors if u in bfs_levels and v in bfs_levels and bfs_levels[v] == bfs_levels[u] + 1]
    nx.draw_networkx_edges(G, pos, edgelist=bfs_edges, edge_color='red', width=2.5, arrows=True)

    # Hide axes
    plt.axis('off')

    # Save the image to static directory
    os.makedirs("static", exist_ok=True)
    plt.savefig("static/graph.png")
    plt.close()

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)

# Reference:
# Thinkxacademy. (2021, April 5). Breadth First Search (BFS) in Python | Graph Theory | Data Structures in Python [Video]. YouTube. https://www.youtube.com/watch?v=tswq532WVF4