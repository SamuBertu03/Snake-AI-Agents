# SnAIke

A didactic project that implements and visualizes various search algorithms applied to the classic Snake game. The project compares uninformed (BFS, DFS) and informed (Greedy, A*) search algorithms in two versions: relaxed and complete.

## Description

This project implements a Snake environment where an AI agent must find the optimal path to reach the food while avoiding collisions. The system allows you to:

* Visualize the search process in real time (explored nodes, frontier, path)
* Compare the performance of different pathfinding algorithms
* Test relaxed (no snake body) and complete versions of the algorithms
* Play manually and compare human strategies with AI strategies

## Features

* Four main search algorithms:

  * BFS (Breadth-First Search)
  * DFS (Depth-First Search)
  * Greedy Best-First Search
  * A* Search

* Two search modes:

  * Relaxed: considers only the snake head (simplified problem)
  * Complete: considers the entire snake body (realistic problem)

* Interactive visualization:

  * Animated representation of the algorithm's reasoning
  * Visualization of visited nodes (light red dots)
  * Planned path (red lines)
  * Real-time metrics (expanded nodes, cost, depth)

* Evaluation metrics:

  * Number of expanded nodes

## Installation

### Requirements

* Python 3.7+
* pip

### Dependencies

```bash
pip install pygame
```

## Usage

### Basic execution

```bash
python main.py --agent bfs
```

### Available parameters

```bash
python main.py --agent <algorithm> --n <apples> --grid <size> --seed <seed> --fps <speed> --think-speed <thinking_speed>
```

Parameters:

* `--agent`: Algorithm to use

  * `bfs`, `dfs`, `greedy`, `astar` (complete versions)
  * `relaxed_bfs`, `relaxed_dfs`, `relaxed_greedy`, `relaxed_astar` (relaxed versions)
  * `human` (manual control)
* `--n`: Number of apples to eat (default: 50)
* `--grid`: Grid size (default: 10)
* `--seed`: Seed for random generation (default: 42)
* `--fps`: Snake execution speed (default: 10)
* `--think-speed`: Visualization speed of the thought process (default: 0.08)
* `--no-render`: Disable graphical rendering

### Examples

```bash
# Relaxed A*, grid 15x15, 100 apples
python main.py --agent relaxed_astar --grid 15 --n 100

# Complete BFS, fast visualization
python main.py --agent bfs --fps 20 --think-speed 0.01

# Manual mode
python main.py --agent human

# Run without graphics for benchmarking
python main.py --agent astar --no-render
```

## Project Structure

```
snake-ai/
├── main.py                      # Application entry point
├── game.py                      # Snake game logic
├── search_agents.py             # Complete algorithms (BFS, DFS, Greedy, A*)
├── search_agents_relaxed.py     # Relaxed algorithms
├── heuristics.py                # Heuristic functions (Manhattan, Euclidean, Diagonal)
├── human_agent.py               # Manual controller
├── renderer.py                  # Pygame visualization
├── .gitignore                  # Git ignore file
└── README.md                    # Project documentation
```

## Implemented Algorithms

### BFS (Breadth-First Search)

Explores level by level, ensuring the shortest path in terms of number of moves.

### DFS (Depth-First Search)

Explores in depth, may find solutions faster but not optimal ones.

### Greedy Best-First Search

Uses a heuristic (Manhattan distance) to choose the most promising node.

### A* Search

Combines real cost and heuristic to efficiently find the optimal path.

## Differences Between Versions

### Relaxed Version

* State space: considers only the snake head
* Advantages: much faster search, fewer nodes to expand
* Disadvantages: the path may cause collisions with the snake body

### Complete Version

* State space: considers the full snake configuration
* Advantages: guarantees valid solutions, avoids collisions
* Disadvantages: slower search, many more states to explore

## Visual Legend

* Light green: Snake head
* Dark green: Snake body
* Red: Food
* Light red dots: Visited search nodes
* Red lines: Planned path
* Gray: Empty cells

## Notes

To modify animation speed during execution, use the parameters `--fps` (snake speed) and `--think-speed` (search visualization speed).
