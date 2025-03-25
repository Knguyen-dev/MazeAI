import random
import sys

import pygame

from algorithms.MazeGenerator import MazeGenerator
from grid.Grid import Grid

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
    """Wait don't delete main.py yet. Sometimes this class doesn't work as the program just crashes"""

    # Pygame setup
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    self.clock = pygame.time.Clock()
    pygame.display.set_caption("MazeAI")
    self.screen.fill(BLACK)

    # Our setup
    random.seed(RANDOM_SEED)
    self.grid = Grid(self.screen, ROWS, COLS, CELL_SIZE, CELL_WALL_WIDTH)
    self.maze_generator = MazeGenerator(delay=DELAY)

  def update_display(self):
    self.screen.fill(BLACK) 
    self.grid.draw()
    pygame.display.update()
    self.clock.tick(60)

  def run(self):
    """The game loop"""
    self.maze_generator.recursive_backtracker(self.grid, update_callback=self.update_display)
    while True:
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      pygame.display.update()
      self.clock.tick(60)
