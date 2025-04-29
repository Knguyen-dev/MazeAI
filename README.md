## MazeAI

**MazeAI** is a Python application that generates and solves mazes with visualization. It supports different generation and search algorithms and is designed for modularity, extensibility, and educational purposes. Users can use command line arguments to select things like maze size and algorithm to be used, and watch an animation of the maze being solved in real time.

---

### Features

- **Maze Generation Algorithms**:
  - `random_dfs` (Recursive Backtracker)
  - `prim` (Randomized Prim's)
  - `kruskal` (Randomized Kruskal's)

- **Maze Solving Algorithms**:
  - `bfs` (Breadth-First Search)
  - `dfs` (Depth-First Search)
  - `dijkstra` (Dijkstra's Algorithm)
  - `astar` (A* Search)
  - `greedy` (Greedy Best-First Search)

- Visualization with real-time animation
- Profiling support to time generation and solving phases

---
#### Main Application Components
The application has four main components:
- `App.py`: The App class acts as the entrypoint in the application, as it lets the user input in command line arguments, and it orchestrates the rest of the components to work together. As a result, the maze will be able to generate the maze, solve it, and render the entire process at the same time.
- `Renderer.py`: The renderer is solely responsible for all rendering related actions, allowing us to see the maze generation and solving on the screen.
- `MazeGenerator.py`: The class that's responsible for data manipulation and using an algorithm to randomly generate the maze.
- `MazeSolver.py`: The class responsible for using a search algorithm to solve the maze.
- `Grid.py` and `Cell`: The internal representation of the maze, as the maze is just a grid. Then each cell in that grid represents a position in the maze. 


---

### Setup Instructions

#### 1. Install the UV Package Manager

We use **uv** as our Python package and virtual environment manager.

Follow the official instructions to install it on your OS [here](https://docs.astral.sh/uv/getting-started/installation/)

#### 2. Clone and Run the Project

```bash
# Clone the project
git clone https://github.com/Knguyen-dev/MazeAI.git
cd MazeAI

# Install all dependencies
uv sync

# run the program with default arguments
uv run src/App.py

# Run with custom configuration
uv run src/App.py --n=50 --imperfection_rate=0 --start 0 0 --end 49 49 --render --animate_generation --animate_solving --cell_size=8 --generator=prim --solver=bfs
```

---

### Command Line Arguments

| Argument                  | Type     | Description |
|---------------------------|----------|-------------|
| `--n`                     | `int`    | Size of the grid (e.g., `--n=30` creates a 30x30 maze). |
| `--cell_size`             | `int`    | Pixel size of each cell in the rendered grid. |
| `--cell_wall_width`       | `int`    | Width of walls between cells (in pixels). |
| `--start x y`             | `int` x2 | Starting cell coordinates (e.g., `--start 0 0`). |
| `--end x y`               | `int` x2 | Ending cell coordinates (e.g., `--end 29 29`). |
| `--generator`             | `str`    | Maze generation algorithm (`random_dfs`, `prim`, `kruskal`). |
| `--solver`                | `str`    | Maze solving algorithm (`bfs`, `dfs`, `astar`, `dijkstra`, `greedy`). |
| `--imperfection_rate`     | `float`  | Value from 0.0 to 1.0 (in steps of 0.1) to randomly remove walls and introduce loops. |
| `--render`                | `flag`   | Enable graphical rendering with Pygame. |
| `--animate_generation`    | `flag`   | Animate the maze generation process (requires `--render`). |
| `--animate_solving`       | `flag`   | Animate the maze solving process (requires `--render`). |
| `--log`                   | `flag`   | Enable profiling (logs time to generate and solve maze). |
| `--save`                  | `flag`   | Save the final rendered maze as a `.png` image. |
| `--seed`                  | `int`    | Seed for the random number generator (ensures reproducibility). |

---

### Example Commands

```bash
# Generate and solve a 30x30 maze using DFS with animation and logging
uv run src/App.py --n=30 --generator=random_dfs --solver=dfs --render --animate_generation --animate_solving --log

# Run with no rendering or animation
uv run src/App.py --n=20 --generator=kruskal --solver=astar
```

---

### Credits

- [MazeAI GitHub Repository](https://github.com/Knguyen-dev/MazeAI)
- Developed by Kevin Nguyen, Lucas Germinari Carreira, and Jesus Rendon Quintanilla
- TAs and mentors: Sanjana Agrawal, Owen Kleinmaier
