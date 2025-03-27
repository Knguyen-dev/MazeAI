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
  
  def update_display(self):
    self.surface.fill((0, 0, 0))  # Clear the screen to black
    self.draw_grid()
    pygame.display.update()
    self.clock.tick(60)

  def draw_cell(self, cell: Cell) -> None:
    """Draws a cell and its walls
    Args:
        surface (pygame.Surface): Surface we're drawing on
        cell_size (int): Length=width of the cell
    """
    x_pixels = cell.x * self.cell_size
    y_pixels = cell.y * self.cell_size

    '''
    If either the cell is visited or is a path cell, then we'll color it accordingly. 
    You should note that when the search algorithm finds the goal path, the nodes in the goal path 
    will be both visited and in the path. However we want to render only one color for this, so for
    nodes in the goal path, we'll color them with red only.

    Explaining set_alpha:
    First we created a pygame surface that uses source alpha values.
    This just basically means that we can color the surface, and apply a uniform layer 
    of transparency over each pixel in the surface. As a result, we can achieve an effect 
    that looks like we "highlight" a cell, when it becomes visited.                          
    '''
    transparent_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
    if self.highlight_cells and (cell.is_visited or cell.is_in_path):
      if cell.is_in_path:
        transparent_surface.fill(
          (255, 0, 0))  
        pygame.Surface.set_alpha(transparent_surface, 64)
        self.surface.blit(transparent_surface, (x_pixels, y_pixels))
      else:
        transparent_surface.fill((200,200,0))     
        pygame.Surface.set_alpha(transparent_surface, 64)
        self.surface.blit(transparent_surface, (x_pixels, y_pixels))  

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
      if cell.walls[direction]:
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
