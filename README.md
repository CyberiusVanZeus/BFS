# Data Structure and Algorithms
## PHD25CMP0001

# BFS Web App

A simple Flask web application for visualizing Breadth-First Search (BFS) traversal on user-defined graphs. Users can input a graph in adjacency list format, specify a start node, and view both the BFS traversal order and a visual representation of the graph.

## Features

- Input any directed graph using adjacency list format
- Specify the start node for BFS
- See BFS traversal order and node levels
- Interactive graph visualization with [vis-network](https://visjs.org/)
- Static graph image highlighting BFS tree edges

## Getting Started

### Prerequisites

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/CyberiusVanZeus/BFS.git
   cd BFS
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the App

```sh
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

1. Enter your graph in adjacency list format:
   ```
   A: B C
   B: D
   C: D E
   D:
   E:
   ```
2. Enter the start node (e.g., `A`)
3. Click **Submit** to see the BFS traversal and graph visualization
4. Click **Reset** to clear the graph and results

## File Structure

- `app.py` — Main Flask application
- `Templates/index.html` — Web interface
- `static/graph.png` — Generated graph image

## Dependencies

- Flask
- NetworkX
- Matplotlib
- vis-network (via CDN)

## License

MIT License

## Reference

- Thinkxacademy. (2021, April 5). Breadth First Search (BFS) in Python | Graph Theory | Data Structures in Python [Video]. [YouTube](https://www.youtube.com/watch?v=tswq532WVF4)
