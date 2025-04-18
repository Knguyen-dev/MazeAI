import csv
import os
import time
import tracemalloc
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd


class Profiler:
    def __init__(self):
        self.std_log_file_header = ["Timestamp", "Function", "Execution Time (s)", "Memory (KB)", "Peak Memory (KB)"]
        self.benchmark_log_file_header = ["Timestamp", "Function", "Runs", "Avg Execution Time (s)", "Avg Memory (KB)", "Avg Peak Memory (KB)"]
        self.solver_log_file = "solver.csv"
        self.generator_log_file = "generator.csv"
        self.plots_dir = "/plots"
    
    def _log_entry(self, log_file, entry, header):
        """Creates an entry in the log file; adds a header if one doesn't already exist"""
        file_exists = os.path.isfile(log_file)
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists or os.stat(log_file).st_size == 0:
                writer.writerow(header)
            writer.writerow(entry)
            
    @staticmethod
    def clear_log_file(log_file):
        """
        Clears the log file. Does not delete it, just clear the content.
        """
        # open in write mode to truncate the file (clear contents), or create it if it doesn't exist
        with open(log_file, 'w') as file:
            pass #opening file in write mode clears the content
            
    def profile_helper(self, func, *args, **kwargs):
        tracemalloc.start()
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        execution_time = end_time - start_time
        return (execution_time, current / 1024, peak / 1024)
 
    def profile_maze_generation(self, generator_fn, grid, *args, **kwargs):
        # Have a helper function that finds the execution times and memory usage and returns that stuff here
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        execution_time, end_memory_usage, peak_memory_usage = self.profile_helper(generator_fn, grid, *args, **kwargs)
        info = [
            grid.num_rows, 
            grid.num_cols, 
            generator_fn.__name__, 
            execution_time, 
            end_memory_usage, 
            peak_memory_usage, 
            timestamp
        ]
        header = ["Rows", "Cols", "Generator", "Execution Time (s)", "Memory Usage (KB)", "Peak Memory Usage (KB)", "Timestamp"]
        self._log_entry(self.generator_log_file, info, header)

    def profile_maze_solver(self, solver_fn, grid, *args, **kwargs):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        execution_time, end_memory_usage, peak_memory_usage = self.profile_helper(solver_fn, grid, *args, **kwargs)
        num_visited = grid.get_num_visited_cells()
        num_in_path = grid.get_num_path_cells()
        entry = [
            grid.num_rows,
            grid.num_cols,
            solver_fn.__name__,
            # Count the number of nodes that have been visited
            num_in_path / num_visited,
            num_in_path,
            num_visited,
            execution_time,
            end_memory_usage,
            peak_memory_usage,
            timestamp
        ]
        header = [
            "Rows", 
            "Cols",
            "Solver",
            "Ratio (num_in_path / num_visited_cells)", 
            "num_in_path", 
            "num_visited_cells", 
            "Execution Time (s)", 
            "Memory Usage (KB)", 
            "Peak Memory Usage (KB)", 
            "Timestamp"
        ]
        self._log_entry(self.solver_log_file, entry, header)

    def mass_profile(self):
        import random

        from algorithms.MazeGenerator import MazeGenerator
        from algorithms.MazeSolver import MazeSolver
        from grid.Grid import Grid
        random.seed()

        grid_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300]
        # Use randomized kruskal as the default maze generator
        maze_generator_fn = MazeGenerator.randomized_kruskal
        solver_arr = [
          MazeSolver.depth_first_search,
          MazeSolver.greedy_best_first,
          MazeSolver.breadth_first_search,
          MazeSolver.dijkstra,
          MazeSolver.a_star,
        ]

        # For each grid size, generate a maze and then run each solver on that maze; make sure to reset the maze (i.e. nested for loop)
        for size in grid_sizes:
            for solver_fn in solver_arr:
                grid = Grid(renderer=None, num_rows=size, num_cols=size)
                
                # Profile and log the information
                self.profile_maze_generation(maze_generator_fn, grid)
                self.profile_maze_solver(solver_fn, grid)
      
    def generate_visualizations(self): 
      os.makedirs(self.plots_dir, exist_ok=True)

      solver_df = pd.read_csv(self.solver_log_file)
      generator_df = pd.read_csv(self.generator_log_file)

      # --- Maze Generator Performance ---
      plt.figure(figsize=(12, 6))
      generator_grouped = generator_df.groupby("Rows").mean(numeric_only=True)
      
      plt.plot(generator_grouped.index, generator_grouped["Execution Time (s)"], marker='o', label="Execution Time (s)")
      plt.plot(generator_grouped.index, generator_grouped["Peak Memory Usage (KB)"], marker='x', label="Peak Memory Usage (KB)")
      plt.title("Maze Generator Performance")
      plt.xlabel("Grid Size (N x N)")
      plt.ylabel("Performance Metrics")
      plt.legend()
      plt.grid(True)
      plt.tight_layout()
      plt.savefig(os.path.join(self.plots_dir, "maze_generator_performance.png")) 
    
      # --- Maze Solver Execution Time ---
      plt.figure(figsize=(12, 6))
      for solver_name in solver_df["Solver"].unique():
          solver_data = solver_df[solver_df["Solver"] == solver_name]
          solver_grouped = solver_data.groupby("Rows").mean(numeric_only=True)
          plt.plot(solver_grouped.index, solver_grouped["Execution Time (s)"], marker='o', label=solver_name)
      plt.title("Maze Solver Execution Time")
      plt.xlabel("Grid Size (N x N)")
      plt.ylabel("Execution Time (s)")
      plt.legend()
      plt.grid(True)
      plt.tight_layout()
      plt.savefig(os.path.join(self.plots_dir, "maze_solver_execution_time.png"))
    
      # --- Maze Solver Peak Memory Usage ---
      plt.figure(figsize=(12, 6))
      for solver_name in solver_df["Solver"].unique():
          solver_data = solver_df[solver_df["Solver"] == solver_name]
          solver_grouped = solver_data.groupby("Rows").mean(numeric_only=True)
          plt.plot(solver_grouped.index, solver_grouped["Peak Memory Usage (KB)"], marker='x', label=solver_name)
      plt.title("Maze Solver Peak Memory Usage")
      plt.xlabel("Grid Size (N x N)")
      plt.ylabel("Peak Memory Usage (KB)")
      plt.legend()
      plt.grid(True)
      plt.tight_layout()
      plt.savefig(os.path.join(self.plots_dir, "maze_solver_peak_memory_usage.png"))
    
      # --- Maze Solver: Number of Visited Cells ---
      plt.figure(figsize=(12, 6))
      for solver_name in solver_df["Solver"].unique():
          solver_data = solver_df[solver_df["Solver"] == solver_name]
          solver_grouped = solver_data.groupby("Rows").mean(numeric_only=True)
          plt.plot(solver_grouped.index, solver_grouped["num_visited_cells"], marker='s', label=solver_name)
      plt.title("Number of Cells Visited by Each Solver")
      plt.xlabel("Grid Size (N x N)")
      plt.ylabel("Visited Cells")
      plt.legend()
      plt.grid(True)
      plt.tight_layout()
      plt.savefig(os.path.join(self.plots_dir, "maze_solver_visited_cells.png"))  # Save plot