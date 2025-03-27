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
  DELAY,
  HEIGHT,
  RANDOM_SEED,
  ROWS,
  WIDTH,
)


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
    self.grid = Grid(ROWS, COLS, (0,0), (COLS-1,ROWS-1))
    self.maze_generator = MazeGenerator(delay=0)
    self.maze_solver = MazeSolver(DELAY)
    self.renderer = Renderer(
      self.screen,
      self.clock,
      self.grid,
      CELL_SIZE,
      CELL_WALL_WIDTH,
      False # Generate the maze; ensure the renderer doesn't highlight the cells it visits when creating the maze
    )

  def run(self):
    """Function involved in the main program loop"""
    self.maze_generator.recursive_backtracker(
      self.grid, 
      update_callback=self.renderer.update_display
    )

    # For maze solving, make sure the renderer highlights the cells being visited
    self.renderer.highlight_cells = True
    self.maze_solver.breadth_first_search(
      self.grid,
      update_callback=self.renderer.update_display
    )
    
    is_running = True
    while is_running:
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          is_running = False
      self.renderer.update_display()
      pygame.display.update()
      self.clock.tick(60)
    
    pygame.quit()
    sys.exit()


def main():
  app = App()
  app.run()

if __name__ == "__main__":
  main()