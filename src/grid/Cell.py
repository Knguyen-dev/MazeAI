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
    self.weight = 1  # Default weight
    self.parent = None

    """
    Here are the bit definitions:
    1. is_visited
    2. is_in_path
    3. Top wall
    4. Left wall
    5. Right wall
    6. Bottom wall

    NOTE: The is_visited and is_in_path flags are set to false by default. Then 
    the walls are all set to true to indicate they're all up.
    """
    self.flags = 0b001111

  def set_bit(self, bit_index):
    self.flags |= 1 << bit_index

  def clear_bit(self, bit_index):
    self.flags &= ~(1 << bit_index)

  def get_bit(self, bit_index):
    return self.flags & (1 << bit_index)

  def set_is_visited(self, value: bool) -> None:
    """Sets whether or not a cell is visited

    Args:
      value (bool): If true, then cell is visited.
    """
    if value:
      self.set_bit(5)
    else:
      self.clear_bit(5)

  def get_is_visited(self) -> bool:
    """Returns whether the cell has been visited.

    Returns:
        bool: If true, cell is visited
    """
    return bool(self.get_bit(5))

  def set_in_path(self, value: bool) -> None:
    """Sets whether a cell is on the goal path or not
    Args:
        value (bool): If true, cell is on the goal path
    """
    if value:
      self.set_bit(4)
    else:
      self.clear_bit(4)

  def get_in_path(self) -> bool:
    return bool(self.get_bit(4))

  def get_wall(self, direction: Direction) -> bool:
    """Gets the status of the wall in a given direction

    Args:
        direction (Direction): Direction of the wall we're checking

    Returns:
        bool: If true, the wall is up.
    """
    if direction == Direction.UP:
      return bool(self.get_bit(3))
    elif direction == Direction.LEFT:
      return bool(self.get_bit(2))
    elif direction == Direction.RIGHT:
      return bool(self.get_bit(1))
    else:
      return bool(self.get_bit(0))

  def set_wall(self, direction: Direction, is_up: bool) -> None:
    """Sets the status of a wall in a given direction

    Args:
        direction (Direction): The direction of the wall we're modifying. E.g. passing Direction.UP means we're modifying the top wall or border of the cell.
        is_up (bool): A boolean indicating whether a wall is built or not. For example if is_up = True, for the top wall, that makes the agent can't traverse into the cell from the top.

    """
    if direction == Direction.UP:
      if is_up:
        self.set_bit(3)
      else:
        self.clear_bit(3)
    elif direction == Direction.LEFT:
      if is_up:
        self.set_bit(2)
      else:
        self.clear_bit(2)
    elif direction == Direction.RIGHT:
      if is_up:
        self.set_bit(1)
      else:
        self.clear_bit(1)
    else:
      if is_up:
        self.set_bit(0)
      else:
        self.clear_bit(0)

  def reset(self) -> None:
    """Resets the cell to its initial state, useful for re-initializing a cell for another maze solver"""
    self.set_in_path(False)
    self.set_is_visited(False)
    self.parent = None  # Reset the parent reference, allowing the path finding algorithms to re-compute the path from scratch.

  def __repr__(self) -> None:
    return (
      f"Cell(x={self.x}, y={self.y}, weight={self.weight}, is_visited={self.is_visited}, "
      f"walls={{UP: {self.get_wall(Direction.UP)}, DOWN: {self.get_wall(Direction.DOWN)}, "
      f"LEFT: {self.get_wall(Direction.LEFT)}, RIGHT: {self.get_wall(Direction.RIGHT)}}})"
    )
