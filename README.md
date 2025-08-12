# AI & Algorithm Techniques Showcase

This repository contains implementations of three fundamental AI and algorithmic techniques, each demonstrated with a Python example.  
They are designed for learning, experimenting, and understanding how different problem-solving strategies work in practice.


## 📌 Techniques Covered

### 1. **A\* Pathfinding**
A* (A-star) is a popular search algorithm for finding the shortest path between two points.  
It uses both the actual cost from the start (`g-cost`) and a heuristic estimate to the goal (`h-cost`) to prioritize which paths to explore.

**Features:**
- Works on grid-based maps.
- Supports obstacles.
- Guaranteed optimal path if the heuristic is admissible.

**Example Usage:**
```python
if a_star(draw_function, grid, start_node, goal_node):
    print("Path found!")
else:
    print("No path available.")
````

### 2. **Tic-Tac-Toe Brute Force Move Finder**

A simple AI that determines the best next move by simulating all possible outcomes.
It evaluates each move's result to avoid losing situations and maximize winning chances.

**Features:**

* Works for both players `'X'` and `'O'`.
* Considers immediate wins and blocks opponent victories.
* Lightweight and easy to understand.

**Example Usage:**

```python
board = ["X", "O", "X",
         " ", "O", " ",
         " ", " ", "X"]

move = optimal_move_search(board, "O")
print(f"Best move for O: {move}")
```

### 3. **Dijkstra’s Shortest Path**

An algorithm to find the shortest distance from a starting node to all other nodes in a weighted graph.
It is widely used in networking, routing, and GPS systems.

**Features:**

* Works on weighted graphs with non-negative weights.
* Returns the minimum cost to reach each node.
* Easy to adapt for both directed and undirected graphs.

**Example Usage:**

```python
travel_times = transport_network.compute_shortest_paths('West')
for i, time in enumerate(travel_times):
    print(f"Minimum time from West to {transport_network.node_labels[i]}: {time}")
```


## 📚 Learning Goals

* Understand how different algorithms work for pathfinding, game AI, and graph traversal.
* See practical applications of search, heuristics, and optimization.
* Explore modular Python code that’s easy to modify and extend.


## 🛠 Technologies Used

* **Python 3.x**
* Standard Python libraries (`queue`, `itertools`, etc.)
* Optionally, `pygame` for A\* visualization.

