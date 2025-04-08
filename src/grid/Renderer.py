from collections import deque

import pygame

from grid.Cell import Cell
from utils.Direction import Direction


class Renderer:
  def __init__(self, surface: pygame.Surface, clock: pygame.time.Clock, cell_size: int, cell_wall_width: int, highlight_cells: bool):
    self.surface = surface
    self.clock = clock
    self.cell_size = cell_size
    self.cell_wall_width = cell_wall_width
    self.highlight_cells = highlight_cells

    # This is defined, and maybe w'ere updating the reference?
    self.transparent_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    
    self.changed_cells = deque()

    # Cache of thin semi-transparent surfaces, so it's a map in form {direction: thin_surface}
    self.thin_surface_cache = {}
    
    # For drawing an individual cell
    self.highlight_is_visited_color = (30,144,255)
    self.highlight_is_in_path_color = (178,34,34)
    self.is_visited_src_alpha = 64
    self.is_in_path_src_alpha = 200
    self.background_color = (0, 0, 0)
    self.wall_up_color = (183, 211, 122)
    self.cell_size = cell_size
    self.cell_wall_width = cell_wall_width

  def mark_dirty(self, cell: Cell) -> None:
    # If the given cell is not already in there, then add it to be drawn
    # NOTE: This avoids having the same cell being drawn multiple times
    if cell not in self.changed_cells:
      self.changed_cells.append(cell)

  def render_dirty_cells(self) -> None:
    while self.changed_cells:
      cell = self.changed_cells.popleft()
      self.draw_cell(cell)

  def update_display(self):
    self.render_dirty_cells()
    pygame.display.update()
    self.clock.tick(120)
  
  def handle_highlight_cell(self, cell: Cell):
    """Handles highlighting a square cell

    Args:
        cell (Cell): Cell being highlighted
    """
    # --- Logic for highlighting an entire cell ---
    # NOTE: Only highlight when highlighting is turned on and the cell is either visited or in path.
    if self.highlight_cells and (cell.get_is_in_path() or cell.get_is_visited()):
      if cell.get_is_in_path():
        self.transparent_surface.fill(self.highlight_is_in_path_color)
        self.transparent_surface.set_alpha(self.is_in_path_src_alpha)
      else:
        self.transparent_surface.fill(self.highlight_is_visited_color)
        self.transparent_surface.set_alpha(self.is_visited_src_alpha)
    self.surface.blit(self.transparent_surface, (cell.x * self.cell_size, cell.y * self.cell_size))

  def handle_draw_lines(self, cell: Cell):
    """Handles drawing lines or the absences of lines for a cell.s

    Args:
        cell (Cell): _description_
    """
    x_pixels = cell.x * self.cell_size
    y_pixels = cell.y * self.cell_size
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
      start_pos, end_pos = walls_to_draw[direction]
      pygame.draw.line(
        self.surface, 
        self.wall_up_color if cell.get_wall(direction) else self.background_color,
        start_pos,
        end_pos,
        self.cell_wall_width
      )

  def handle_draw_semitransparent_lines(self, cell: Cell):
    """Handles drawing the semi-transparent lines for highlighted cells

    Args:
        cell (Cell): Cell whose walls we're creating transparent walls for

    """
    # We can only highlight when: self.highlight_cells and (cell.get_is_in_path() or cell.get_is_visited())
    # NOTE: Guard clause here, so if we don't meet that above condition, then stop early since we can't highlight cells.
    if not self.highlight_cells or (not cell.get_is_in_path() and not cell.get_is_visited()):
      return
    
    
    # For each direction, draw a thin semi-transparent wall when necessary
    x_pixel = cell.x * self.cell_size
    y_pixel = cell.y * self.cell_size
    wall_pos = {
      Direction.UP: (x_pixel, y_pixel),
      Direction.DOWN: (x_pixel, y_pixel + self.cell_size),
      Direction.LEFT: (x_pixel, y_pixel),
      Direction.RIGHT: (x_pixel + self.cell_size, y_pixel)
    }
    for direction in Direction:

      # If the cell wall in a given direction is built, then skip it because we only draw 
      # a semitransparent wall when a wall is down 
      if cell.get_wall(direction):
        continue

      '''
      # At this point we're looking at a fallen wall. There are two scenarios:
      # - Check if we already have a reference to this wall in our cache, based on its direction
      # 1. Creating a horizontal wall, which is used to fill in the top and down wall
      # 2. Creating a vertical wall, which is used to fill in the left and right wall
      '''
      thin_surface = None
      if direction in self.thin_surface_cache:
        thin_surface = self.thin_surface_cache[direction]
      else:
        '''
        # - Else it's not in the cache, so create a new wall reference
        # 1. To create a horizontal wall, it just needs to be a surface that stretches as long as a 
        #   cell wall. But it has infinitesimal height.
        # 2. To create a vertical wall, it needs to be a surface with infinitesimal width, but a height that stretches as long as 
        #   an original cell wall.
        # 3. Update to thin_surface to reference the thin transparent surface we have in the cache
        '''
        if direction == Direction.UP or direction == Direction.DOWN:
          self.thin_surface_cache[direction] = pygame.Surface((self.cell_size, self.cell_wall_width), pygame.SRCALPHA)
        else:
          self.thin_surface_cache[direction] = pygame.Surface((self.cell_wall_width, self.cell_size), pygame.SRCALPHA)  
        thin_surface = self.thin_surface_cache[direction]
      
      '''
      # Now we have the semi-transparent surface, we need to draw it in the correct position
      # As well as this, we need to draw it the correct color based on whether it's in path or not
      # NOTE: Remember that at this point we know that it's either in the goal path or it's visited
      '''
      start_pos = wall_pos[direction]
      if cell.get_is_in_path():
        thin_surface.fill(self.highlight_is_in_path_color)
        thin_surface.set_alpha(self.is_in_path_src_alpha)
      else:
        thin_surface.fill(self.highlight_is_visited_color)      
        thin_surface.set_alpha(self.is_visited_src_alpha)
      self.surface.blit(thin_surface, start_pos)

    
  def draw_cell(self, cell: Cell) -> None:
    """Draws a cell and its walls
    Args:
        surface (pygame.Surface): Surface we're drawing on
        cell_size (int): Length=width of the cell
    """
    self.handle_highlight_cell(cell)
    self.handle_draw_lines(cell)
    self.handle_draw_semitransparent_lines(cell)
    