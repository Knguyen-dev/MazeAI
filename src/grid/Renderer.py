import numpy as np
import pygame

from grid.Cell import Cell
from grid.Grid import Grid
from utils.constants import YELLOW
from utils.Direction import Direction


class Renderer:
  def __init__(self, surface: pygame.Surface, clock: pygame.time.Clock, grid: Grid, cell_size: int, cell_wall_width: int, highlight_cells: bool):
    self.surface = surface
    self.clock = clock
    self.grid =  grid
    self.cell_size = cell_size
    self.cell_wall_width = cell_wall_width
    self.highlight_cells = highlight_cells
    self.transparent_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    self.transparent_surface.set_alpha(64)
                      
  def update_display(self):
    self.surface.fill((0, 0, 0))  # Clear the screen to black
    self.draw_grid()
    pygame.display.update()
    self.clock.tick(120)

  def draw_cell(self, cell: Cell) -> None:
    """Draws a cell and its walls
    Args:
        surface (pygame.Surface): Surface we're drawing on
        cell_size (int): Length=width of the cell
    """
    x_pixels = cell.x * self.cell_size
    y_pixels = cell.y * self.cell_size

    # If we have highlight mode on and teh cell has been visited or it's in the goal path, then highlight it.
    if self.highlight_cells and (cell.get_is_visited() or cell.get_in_path()):
      if cell.get_in_path():
        self.transparent_surface.fill((255,0,0))
      else:
        self.transparent_surface.fill((200,200,0))
      self.surface.blit(self.transparent_surface, (x_pixels, y_pixels))

    # For each direction, check to see if it's wall is up, if so draw it 
    walls_to_draw = {
      Direction.UP: ((x_pixels, y_pixels), (x_pixels + self.cell_size, y_pixels)),
      Direction.DOWN: (
        (x_pixels, y_pixels + self.cell_size),
        (x_pixels + self.cell_size, y_pixels + self.cell_size),
      ),
      Direction.LEFT: ((x_pixels, y_pixels), (x_pixels, y_pixels + self.cell_size)),
      Direction.RIGHT: (
        (x_pixels + self.cell_size, y_pixels),
        (x_pixels + self.cell_size, y_pixels + self.cell_size),
      ),
    }

    for direction in walls_to_draw:
      if cell.get_wall(direction):
        start_pos, end_pos = walls_to_draw[direction]
        pygame.draw.line(
          self.surface, 
          YELLOW,
          start_pos,
          end_pos,
          self.cell_wall_width
        )

  def draw_grid(self) -> None:
    """Iterate through all cells in the grid and draw each one"""
    for y in range(self.grid.num_rows):
      for x in range(self.grid.num_cols):
        cell = self.grid.get_cell(x,y)
        self.draw_cell(cell)
