# MazeAI
MazeAI is a Python-based application for generating and solving mazes. It includes various maze generation algorithms (e.g., Recursive Backtracker, Randomized Prim's) and search algorithms (e.g., A*, BFS, DFS). The project is designed to be modular, scalable, and easy to replicate in other languages.


### Setting up the project

#### Install UV Package Manager
Go [here](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to get the instructions. I'll summarize it here: 

```
<!-- Installs UV globally from the internet -->
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

<!-- Verifies installation -->
uv
```

#### Clone and setup GitHub Repo
```
<!-- Clone the project -->
https://github.com/Knguyen-dev/MazeAI.git

<!-- Make sure you're in the project directory. Then Download dependencies -->
uv sync

<!-- Runs the program with specific configurations -->
uv run src/App.py --n=50 --imperfection_rate=0 --start 0 0 --end 49 49 --render --animate_generation --animate_solving --cell_size=8 --generator=prim --solver=bfs
```


### Project Scripts 
```Bash
# Run the program
uv run src/App.py

# Managing dependencies
uv add <package-name>
uv add <package-name> --dev
uv remove <package-name>

# Formatting and linting
uv run ruff format
uv run ruff check

# Running tests
uv run pytest <test_file_name>
uv run pytest 
uv build
```

### General Procedures
- Use snake_case for variable and function names. Then PascalCase for class names. This isn't critical, but it's just nice to do.
- If you're adding a new feature, create a feature branch. Before pushing the branch, pull from main to ensure you have the latest changes.
- To avoid doing work that others are already working on, look at the issues tab and find an issue that no one is working on. Then assign yourself to it. 

## Credits
- [MazeAI GitHub Repo](https://github.com/Knguyen-dev/MazeAI.git)