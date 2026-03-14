# 🧩 A* Maze Solver

A Python implementation of the **A\* (A-Star) Search Algorithm** that finds the shortest path through a maze with **live step-by-step animation** using matplotlib.

---

## 📺 Demo

The solver animates in two phases:
- 🔵 **Blue cells** — A\* actively exploring the maze in real time
- 🟡 **Gold cells** — The final shortest path traced from Start to Goal

---

## 🚀 How to Run

### 1. Install dependency
```bash
pip install matplotlib
```

### 2. Run the solver
```bash
python maze_solver.py
```

---

## 🗂️ Project Structure
```
├── maze_solver.py   # Main Python file — algorithm + animation
└── README.md        # This file
```

---

## ⚙️ Configuration

All settings are at the top of `maze_solver.py`:

| Setting | Default | Description |
|---|---|---|
| `START` | `(0, 0)` | Starting cell (row, col) |
| `GOAL` | `(9, 9)` | Goal cell (row, col) |
| `DIAGONAL` | `False` | Allow diagonal movement (8-dir) |
| `ANIMATION_SPEED` | `80` | Milliseconds per frame (lower = faster) |
| `CHOSEN_HEURISTIC` | `"manhattan"` | Heuristic function to use |

### Editing the Maze
In `maze_solver.py`, edit the `MAZE` grid directly:
```python
MAZE = [
    [0, 0, 0, 1, 0],   # 0 = open cell
    [0, 1, 0, 1, 0],   # 1 = wall
    [0, 0, 0, 0, 0],
]
```

---

## 🧠 How A* Works

A\* is a best-first search algorithm that finds the shortest path by combining two costs:
```
f(n) = g(n) + h(n)
```

| Term | Meaning |
|---|---|
| `g(n)` | Actual cost from the start node to node n |
| `h(n)` | Estimated cost from node n to the goal (heuristic) |
| `f(n)` | Total estimated cost — A\* always explores the lowest f first |

A\* uses a **min-heap (priority queue)** to always process the most promising node next, guaranteeing the shortest path when an admissible heuristic is used.

---

## 📐 Heuristics

Three heuristic functions are available:

### Manhattan Distance
```python
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```
Best for **4-directional** grids (up, down, left, right).

### Euclidean Distance
```python
def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
```
Best when **diagonal movement** is allowed.

### Chebyshev Distance
```python
def chebyshev(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
```
Best for **8-directional** grids (includes diagonals).

To switch heuristic, change this line in `maze_solver.py`:
```python
CHOSEN_HEURISTIC = "manhattan"   # or "euclidean" or "chebyshev"
```

---

## 🗺️ Maze Legend

| Symbol | Console | Colour | Meaning |
|---|---|---|---|
| Start | `S` | 🟢 Green | Starting position |
| Goal | `G` | 🔴 Red | Target position |
| Path | `*` | 🟡 Gold | Shortest path found |
| Explored | `o` | 🔵 Blue | Cells A\* examined |
| Wall | `#` | ⬛ Dark | Blocked cell |
| Open | `.` | — | Walkable cell |

---

## 🧱 Node Structure

Each cell in the maze is represented as a `Node` object:
```python
class Node:
    pos     # (row, col) position in the grid
    g       # cost from start to this node
    h       # heuristic estimate from this node to goal
    f       # f = g + h  (A* priority value)
    parent  # reference to previous node (for path reconstruction)
```

---

## 📋 Requirements

- Python 3.x
- matplotlib
```bash
pip install matplotlib
```

---

## 📚 What I Learned

- How to model a grid as a graph of nodes
- How the A\* search algorithm works with open/closed lists
- How heuristic functions affect search efficiency
- How to animate algorithms step by step using `matplotlib.animation`
- How to reconstruct a path using parent pointers

---
## 🖼️ Screenshots




## 👤 Author

**Asna Haris** — Artificial Intelligence Intern

- GitHub: https://github.com/asnaharis06-bot
- LinkedIn: https://www.linkedin.com/in/asna-haris-684058319

## 🔗 Project Links

- 📂 GitHub: [A* Maze Solver](https://github.com/asnah/data-redundancy-removal-system)

## 📄 License

This project is built as part of my Artificial Intelligence Internship Program.

Website: [https://www.codealpha.tech](https://syntecxhub.com/)
