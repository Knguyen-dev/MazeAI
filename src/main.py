import random
import sys

import pygame

from algorithms.MazeGenerator import MazeGenerator
from App import App
from grid.Grid import Grid
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


def main():
  app = App()
  app.run()
  # pygame.init()
  # screen = pygame.display.set_mode((WIDTH, HEIGHT))
  # clock = pygame.time.Clock()

  # pygame.display.set_caption("MazeAI")
  # screen.fill(BLACK)
  # random.seed(RANDOM_SEED)

  # # Before we begin let's pass everything through maze to keep things organized 
  # grid = Grid(screen, ROWS, COLS, CELL_SIZE, CELL_WALL_WIDTH)
  # mazeGenerator = MazeGenerator(delay=0.10)

  # def update_display():
  #   screen.fill(BLACK)
  #   grid.draw()
  #   pygame.display.update()
  #   clock.tick(60)

  # mazeGenerator.recursive_backtracker(grid, update_display)
  
  # while True:
  #   for e in pygame.event.get():
  #     if e.type == pygame.QUIT:
  #       pygame.quit()
  #       sys.exit()
  #   pygame.display.update()
  #   clock.tick(60)


if __name__ == "__main__":
  main()
