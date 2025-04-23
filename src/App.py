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
from utils.Profiler import Profiler


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
    self.profiler = Profiler()
    self.generator_fn = App.generator_map.get(args.generator, App.generator_map["prim"])
    self.solving_fn = App.solver_map.get(args.solver, App.solver_map["bfs"])
    self.imperfection_rate = args.imperfection_rate if args.imperfection_rate is not None else 0
    args.seed = args.seed if args.seed is not None else 42
    random.seed(args.seed)

    # Grid and solver
    GRID_LENGTH = args.n if args.n is not None else 30
    CELL_SIZE = args.cell_size if args.cell_size is not None else 20 
    CELL_WALL_WIDTH = args.cell_wall_width if args.cell_wall_width is not None else 2

    # If positions are none or out of range, then we'll replace them with default values
    START_POS = None
    END_POS = None
    if (args.start is None) or (args.start[0] < 0 or args.start[0] > GRID_LENGTH - 1) or (args.start[1] < 0 or args.start[1] > GRID_LENGTH - 1):
      START_POS = (0,0)
    else:
      START_POS = (args.start[0], args.start[1])
    if (args.end is None) or (args.end[0] < 0 or args.end[0] > GRID_LENGTH - 1) or (args.end[1] < 0 or args.end[1] > GRID_LENGTH - 1):
      END_POS = (GRID_LENGTH-1, GRID_LENGTH-1)
    else:
      END_POS = (args.end[0], args.end[1])

    # Rendering, logging, saving
    self.animate_generation = None # generation and animate solving have None as a default
    self.animate_solving = None
    self.logging_enabled = args.log 
    self.save_image_output = args.save
    self.screen = None
    self.clock = None
    self.renderer = None
    
    if args.render:
      width = GRID_LENGTH * CELL_SIZE  # should be the same for now
      height = GRID_LENGTH * CELL_SIZE
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

      # Animation can only happen when the maze is rendered on the screen in the first place
      self.animate_generation: bool = args.animate_generation 
      self.animate_solving: bool = args.animate_solving 

    self.grid = Grid(self.renderer, GRID_LENGTH, GRID_LENGTH, START_POS, END_POS)

  def generate_maze(self):
    """Generates the maze using the specified algorithm from the command line arguments."""

    # Sets an animation function if we want to animate.
    animate_fn = None
    if self.animate_generation:
      animate_fn = self.renderer.update_display  

    # If user wants to log the generator execution, we'll do it here; else just run the function
    if self.logging_enabled:
      self.profiler.profile_maze_generation(
        self.generator_fn,
        self.grid,
        animate_fn        
      )
    else:
      self.generator_fn(self.grid, animate_fn)

    # Maze has been generated, add imperfections if needed
    MazeGenerator.add_imperfections(self.grid, self.imperfection_rate, animate_fn)

  def solve_maze(self):
    """Solves the maze using the specified solver from the command line arguments."""
    
    animate_fn = None
    if self.animate_solving:
      animate_fn = self.renderer.update_display
    
    if self.logging_enabled:
      self.profiler.profile_maze_solver(
        self.solving_fn,
        self.grid,
        animate_fn
      )
    else:
      self.solving_fn(
        self.grid,
        update_callback=animate_fn
      )
      
  def run(self):
    """Function involved in the main program loop"""
    # Draw the grid; all cells should be drawn at the time
    # the grid is created. So we just need to request one animation frame to draw it    
    # Generate and solve maze
    self.generate_maze()
    if self.renderer:
      self.renderer.highlight_cells = True
      self.renderer.update_display()
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
      if self.save_image_output:
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
  parser.add_argument("--cell_size", type=int)
  parser.add_argument("--cell_wall_width", type=int)
  parser.add_argument("--start", nargs=2, type=int)
  parser.add_argument("--end", nargs=2, type=int)
  parser.add_argument("--generator", choices=generator_choices)
  parser.add_argument("--solver", choices=solver_choices)
  
  parser.add_argument("--imperfection_rate", type=float, default=0.0, choices=[i / 10 for i in range(11)])

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

