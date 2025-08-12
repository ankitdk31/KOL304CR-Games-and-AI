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
```

### 2. **AI for Air Hockey**

A real-time AI opponent for a physics-based Air Hockey game.
The AI tracks the puck, predicts its path, and switches between offense and defense depending on the situation.

**Features:**

* Real-time puck tracking and movement prediction.
* Defensive positioning to block shots.
* Offensive plays to aim and score.
* Adaptive behavior for more engaging gameplay.

**Example Usage:**

```python
ai_player.ai_move(puck)
puck.move()
```


### 3. **AI for Snake Game**

An AI-controlled Snake game where the snake automatically navigates toward food while avoiding collisions.
Uses **Breadth-First Search (BFS)** pathfinding with fallback survival logic.

**Features:**

* Finds shortest safe path to food.
* Avoids collisions with walls and itself.
* Random survival moves if no safe path exists.
* Fully automated gameplay — no human input needed.

**Example Usage:**

```python
game.ai_decision()
if not game.step():
    print(f"Game over! Score: {game.score}")
    game.reset()
```


## 📚 Learning Goals

* Understand how AI algorithms handle real-time decision-making.
* Explore practical implementations of search, heuristics, and optimization.
* Learn how to integrate algorithms into interactive simulations and games.


## 🛠 Technologies Used

* **Python 3.x**
* Standard Python libraries (`queue`, `collections`, etc.)
* **Pygame** for interactive visualization.
