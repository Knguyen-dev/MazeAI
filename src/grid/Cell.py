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
    self.weight = 1 # Default weight

    # The parent or preceding cell; really reusable and memory efficient way 
    # of storing it.
    self.parent = None
    self.is_visited = False
    self.is_in_path = False
    self.walls = {
      Direction.UP: True,
      Direction.DOWN: True,
      Direction.LEFT: True,
      Direction.RIGHT: True,
    }

  def get_wall(self, direction: Direction) -> bool:
    """Gets the status of the wall in a given direction

    Args:
        direction (Direction): Direction of the wall we're checking

    Returns:
        bool: If true, the wall is up.
    """
    return self.walls[direction]

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
