import argparse
import datetime
import os
import random
import sys

import pygame

from algorithms.MazeGenerator import MazeGenerator
from algorithms.MazeSolver import MazeSolver
from grid.Grid import Grid
from grid.Renderer import Renderer

# You can probably create a separate rendering class
from utils.Profiler import profile


class App:
  # Class/static variables to indicate the maze generator and solver functions;
  # this maps command line arguments to algorithms, making it easy to select the appropriate
  # algorithm with a CLI.
  generator_map = {
    "random_dfs": MazeGenerator.recursive_backtracker,
    "prim": MazeGenerator.randomized_prim,
    "kruskal": MazeGenerator.randomized_kruskal,
  }
  solver_map = {
    "astar": MazeSolver.a_star,
    "dijkstra": MazeSolver.dijkstra,
    "dfs": MazeSolver.depth_first_search,
    "bfs": MazeSolver.breadth_first_search,
    "greedy": MazeSolver.greedy_best_first,
  }

  def __init__(self, args):
    """Wait don't delete main.py yet. Sometimes tis class doesn't work as the program just crashes"""
    self.args = args

    # Maze Generation args
    self.args.generator = self.args.generator if self.args.generator else "prim"
    self.args.imperfection_rate = self.args.imperfection_rate if self.args.imperfection_rate is not None else 0
    self.args.seed = self.args.seed if self.args.seed is not None else 42
    random.seed(self.args.seed)

    # Grid and solver
    self.args.solver = self.args.solver if self.args.solver else "astar"
    self.args.n = self.args.n if self.args.n is not None else 30
    self.args.start = self.args.start if self.args.start is not None else (0, 0)
    self.args.end = (
      self.args.end if self.args.end is not None else (self.args.n - 1, self.args.n - 1)
    )

    # Rendering, logging, saving
    self.args.render = self.args.render if self.args.render is not None else False
    self.args.log = self.args.log if self.args.log is not None else False
    self.args.save = self.args.save if self.args.save is not None else False
    self.screen = None
    self.clock = None
    self.renderer = None
    
    if args.render:
      CELL_SIZE = 10
      CELL_WALL_WIDTH = 1 

      width = self.args.n * CELL_SIZE  # should be the same for now
      height = self.args.n * CELL_SIZE
      pygame.init()
      self.screen = pygame.display.set_mode((width, height))
      pygame.display.set_caption("MazeAI")
      self.screen.fill((0,0,0))
      self.clock = pygame.time.Clock()
      self.renderer = Renderer(
        self.screen,
        self.clock,
        CELL_SIZE,
        CELL_WALL_WIDTH,
        # Don't highlight cells during maze generation; this is used for visualization of the maze generation process
        # NOTE: This is due to the rendering process using is_visited to highlight cells, and our
        # maze generation algorithms using the same state to mark cells as visited for some algorithms.
        False,
      )

    self.grid = Grid(self.renderer, self.args.n, self.args.n, self.args.start, self.args.end)

  def generate_maze(self):
    """Generates the maze using the specified algorithm from the command line arguments."""

    # Select maze generator function called on args
    generator_fn = App.generator_map.get(self.args.generator)

    # If both are true, then we'll define an animation function, else it'll be null
    animate_fn = self.renderer.update_display if self.args.render and self.args.animate_generation else None

    # If user wants to log the generator execution, we'll do it here; else just run the function
    if self.args.log:
      profile(
        self.grid.num_rows,
        self.grid.num_cols,
        "generator.csv",
        generator_fn,
        self.grid,
        animate_fn
      )
    else:
      generator_fn(self.grid, animate_fn)

    # Maze has been generated, add imperfections if needed
    MazeGenerator.add_imperfections(self.grid, self.args.imperfection_rate, animate_fn)

  def solve_maze(self):
    """Solves the maze using the specified solver from the command line arguments."""
    
    solver_fn = None
    animate_fn = self.renderer.update_display if self.args.render and self.args.animate_solving else None
    
    if self.args.solver in App.solver_map:
      solver_fn = App.solver_map[self.args.solver] 
    else:
      print(f"Solver arg with name: {self.args.solver}, isn't valid! Skipping it.")
      return

    if self.args.log:
      profile(
        self.grid.num_rows,
        self.grid.num_cols,
        "solver.csv",
        solver_fn,
        self.grid,
        # Only animation the process of solving the maze if the user has specified they want animation; also need rendering on as well.
        update_callback=animate_fn
      )
    else:
      solver_fn(
        self.grid,
        update_callback=animate_fn
      )
      
  def run(self):
    """Function involved in the main program loop"""

    # Draw the grid; all cells should be drawn at the time
    # the grid is created. So we just need to request one animation frame to draw it
    self.renderer.update_display()
    
    # Generate and solve maze
    self.generate_maze()
    if self.renderer:
      self.renderer.highlight_cells = True
    self.solve_maze()

    # If rendering is enabled, have a loop opened to render teh winodw
    if self.renderer:
      running = True
      while running:
        for e in pygame.event.get():
          if e.type == pygame.QUIT:
            running = False
        self.renderer.update_display()
        pygame.display.update()
        self.clock.tick(60)

      # If the user wants to save the image
      if self.args.save:
        output_dir = os.path.join(os.getcwd(), "output_images")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"maze_{timestamp}.png")
        pygame.image.save(self.screen, output_path)

    pygame.quit()
    sys.exit()

def parse_args():
  generator_choices = list(App.generator_map.keys())
  solver_choices = list(App.solver_map.keys())
  parser = argparse.ArgumentParser(description="MazeAI")

  parser.add_argument("--n", type=int)
  parser.add_argument("--start", nargs=2, type=int)
  parser.add_argument("--end", nargs=2, type=int)
  parser.add_argument("--generator", choices=generator_choices)
  parser.add_argument("--solver", choices=solver_choices)
  
  parser.add_argument("--imperfection_rate", type=float, choices=[i / 10 for i in range(11)])

  # Whether the program is going to show the screen at all; this is needed to also have things animate
  parser.add_argument("--render", action="store_true")
  parser.add_argument("--animate_generation", action="store_true")
  parser.add_argument("--animate_solving", action="store_true")

  parser.add_argument("--log", action="store_true")
  parser.add_argument("--save", action="store_true")
  parser.add_argument("--seed", type=int)
  return parser.parse_args()

def main():
  args = parse_args()
  app = App(args)
  app.run()

if __name__ == "__main__":
  main()
