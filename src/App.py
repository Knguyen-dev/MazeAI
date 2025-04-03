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
from utils.constants import (
  BLACK,
  CELL_SIZE,
  CELL_WALL_WIDTH,
  COLS,
  HEIGHT,
  RANDOM_SEED,
  ROWS,
  WIDTH,
)
from utils.Profiler import profile


class App:
  def __init__(self):
    """Wait don't delete main.py yet. Sometimes tis class doesn't work as the program just crashes"""

    # Pygame setup
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    self.clock = pygame.time.Clock()
    pygame.display.set_caption("MazeAI")
    self.screen.fill(BLACK)

    # Our setup
    random.seed(RANDOM_SEED)
    self.grid = Grid(ROWS, COLS, (0, 0), (COLS - 1, ROWS - 1))
    self.maze_generator = MazeGenerator()
    self.maze_solver = MazeSolver()
    self.renderer = Renderer(
      self.screen,
      self.clock,
      self.grid,
      CELL_SIZE,
      CELL_WALL_WIDTH,
      False,  # Generate the maze; ensure the renderer doesn't highlight the cells it visits when creating the maze
    )

  def run(self):
    """Function involved in the main program loop"""

    profile(
      self.maze_generator.randomized_prim,
      self.grid,
      update_callback=self.renderer.update_display,
    )

    self.maze_generator.add_imperfections(
      self.grid, imperfection_rate=0.1, update_callback=self.renderer.update_display
    )

    # For maze solving, make sure the renderer highlights the cells being visited
    self.renderer.highlight_cells = True

    profile(
      self.maze_solver.a_star, self.grid, update_callback=self.renderer.update_display
    )

    is_running = True
    while is_running:
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          is_running = False
      self.renderer.update_display()
      pygame.display.update()
      self.clock.tick(60)

    # Ensure an output directory for images exists
    output_dir = os.path.join(os.getcwd(), "output_images")
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename, then save the file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"maze_{timestamp}.png")
    pygame.image.save(self.screen, output_path)

    pygame.quit()
    sys.exit()


def main():
  app = App()
  app.run()


if __name__ == "__main__":
  main()
