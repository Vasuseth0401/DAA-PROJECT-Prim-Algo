
# NetOptima
### Intelligent Network Infrastructure Planning & Cost Optimization System

NetOptima is a Python-based network infrastructure planning application that uses Prim's Minimum Spanning Tree (MST) algorithm to identify a minimum-cost network connecting multiple locations.

## Problem Statement

Connecting multiple facilities requires selecting network links while minimizing installation costs.

NetOptima models locations as vertices and potential connections as weighted edges in an undirected graph. It applies Prim's algorithm to find a Minimum Spanning Tree.

## Key Features

- Graph-based network modeling
- Add and remove network locations
- Add and remove connections
- Prim's Minimum Spanning Tree algorithm
- Minimum-cost network calculation
- Cost reduction analysis
- Interactive graph visualization
- Network save and load using JSON
- Desktop dashboard using CustomTkinter

## Technologies Used

- Python
- CustomTkinter
- Tkinter
- NetworkX
- Matplotlib
- Heap-based Prim's Algorithm
- JSON
- Unittest

## Project Architecture

```text
NetOptima/
│
├── app.py
├── main.py
│
├── core/
│   ├── graph.py
│   ├── network_manager.py
│   └── prims.py
│
├── visualization/
│   └── visualizer.py
│
├── analysis/
│   └── cost_analysis.py
│
├── data/
│   └── network.json
│
├── tests/
│   ├── test_graph.py
│   ├── test_prims.py
│   ├── test_cost_analysis.py
│   ├── test_visualization.py
│   └── test_network_manager.py
│
└── README.md
```

## Algorithm

NetOptima uses Prim's Minimum Spanning Tree algorithm.

The implementation uses a min-heap to select the lowest-cost edge connecting a visited vertex to an unvisited vertex.

### Time Complexity

With an adjacency list and binary min-heap:

O(E log E)

### Space Complexity

O(V + E)

Where:
- V = Number of vertices
- E = Number of edges

## Sample Cost Analysis

| Metric | Value |
|---|---:|
| Total Network Cost | ₹70,000 |
| Minimum Network Cost | ₹45,000 |
| Cost Reduction | ₹25,000 |
| Savings Percentage | 35.71% |

The savings percentage compares the MST cost with the sum of all available connection costs in the sample network.

## Installation

Install the required dependencies:

```bash
pip install customtkinter matplotlib networkx
```

## Running the Application

Open the project in VS Code.

Run:

```bash
python3 app.py
```

## Testing

The project includes automated tests for:

- Graph operations
- Prim's algorithm
- Cost analysis
- Visualization input data
- Network persistence

19 automated tests have been reported as passing during development.

## Limitations

- MST optimizes total installation cost only.
- It does not provide redundant connections or fault tolerance.
- It assumes all selected network links are available.
- It does not optimize bandwidth, latency or traffic.

## Future Enhancements

- Network reliability analysis
- Redundant network path planning
- Advanced interactive visualization
- Exportable cost reports
- Geographic network mapping

## Author

Developed as a Python-based Data Structures and Algorithms project.
