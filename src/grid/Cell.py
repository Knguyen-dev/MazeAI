import pygame

from utils.constants import YELLOW
from utils.Direction import Direction


class Cell:
  def __init__(self, x: int, y: int):
    """Initializes a cell

    Args:
        x (int): col (horizontal) index of the cell
        y (int): row (vertical) index of the cell
    """
    self.x = x
    self.y = y
    self.weight = 0
    self.is_visited = False
    self.walls = {
      Direction.UP: True,
      Direction.DOWN: True,
      Direction.LEFT: True,
      Direction.RIGHT: True,
    }

  def draw(self, surface: pygame.Surface, cell_size: int, cell_wall_width: int):
    """Draws a cell and its walls
    Args:
        surface (pygame.Surface): Surface we're drawing on
        cell_size (int): Length=width of the cell
    """
    x_pixels = self.x * cell_size
    y_pixels = self.y * cell_size

    '''
    Walls:
    - Top wall: top left to top right
    - Bottom wall: Bottom left to bottom right
    - Left wall: Top left to bottom left
    - Right wall: top right to bottom right
    '''
    walls_to_draw = {
      Direction.UP: ((x_pixels, y_pixels), (x_pixels + cell_size, y_pixels)),
      Direction.DOWN: (
        (x_pixels, y_pixels + cell_size),
        (x_pixels + cell_size, y_pixels + cell_size),
      ),
      Direction.LEFT: ((x_pixels, y_pixels), (x_pixels, y_pixels + cell_size)),
      Direction.RIGHT: (
        (x_pixels + cell_size, y_pixels),
        (x_pixels + cell_size, y_pixels + cell_size),
      ),
    }

    # For each direction, check to see if it's wall is up, if so draw it
    for direction in walls_to_draw:
      if self.walls[direction]:
        start_pos, end_pos = walls_to_draw[direction]
        pygame.draw.line(
          surface, 
          YELLOW,
          start_pos,
          end_pos,
          cell_wall_width
        )

  def set_wall(self, direction: Direction, is_up: bool) -> None:
    """Sets the status of a wall in a given direction

    Args:
        direction (Direction): The direction of the wall we're modifying. E.g. passing Direction.UP means we're modifying the top wall or border of the cell.
        is_up (bool): A boolean indicating whether a wall is built or not. For example if is_up = True, for the top wall, that makes the agent can't traverse into the cell from the top.

    NOTE: Make sure that after you modify the current wall, you
    """
    self.walls[direction] = is_up

  def __repr__(self) -> None:
    return (
      f"Cell(x={self.x}, y={self.y}, weight={self.weight}, is_visited={self.is_visited}, "
      f"walls={{UP: {self.walls[Direction.UP]}, DOWN: {self.walls[Direction.DOWN]}, "
      f"LEFT: {self.walls[Direction.LEFT]}, RIGHT: {self.walls[Direction.RIGHT]}}})"
    )
