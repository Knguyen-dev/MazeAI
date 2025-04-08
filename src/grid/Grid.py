import numpy as np

from grid.Cell import Cell
from utils.Direction import Direction


class Grid:
  def __init__(
    self,
    num_rows: int,
    num_cols: int,
    start_pos: tuple[int, int] = (0, 0),
    end_pos: tuple[int, int] = None,
  ):
    """Creates a grid object used to represent the maze.

    Args:
        surface (pygame.Surface): Surface we're drawing the grid on
        num_rows (int): Number of rows in the grid
        num_cols (int): Number of columns in the grid
        start_pos (tuple[int, int], optional): Start position (0-index) of the search within a grid. Defaults to (0,0).
        end_pos (tuple[int, int], optional): End position (0-indexed) of a search within a grid. Defaults to the bottom right corner of the grid.
    """
    self.num_rows = num_rows
    self.num_cols = num_cols

    # Initialize start and end positions
    self.start_pos = start_pos
    self.end_pos = end_pos if end_pos else (num_cols - 1, num_rows - 1)

    # Ensure the start and end positions are valid
    if not self.is_valid_position(self.start_pos[0], self.start_pos[1]):
      raise ValueError("Start position must be in range")
    if not self.is_valid_position(self.end_pos[0], self.end_pos[1]):
      raise ValueError("End position must be in range")

    """
    Index position of the agent drawing the maze or agent solving the maze
    NOTE: I don't know if all functions will use this
    """
    self.agent_pos: tuple[int, int] = (0, 0)
    self.is_agent_visible: bool = False

    # Initialize the matrix of cells
    self.matrix = np.empty((num_rows, num_cols), dtype=object)
    for y in range(num_rows):
      for x in range(num_cols):
        self.matrix[y, x] = Cell(x, y)

  def set_agent_pos(self, pos: tuple[int, int]):
    self.agent_pos = pos

  def set_agent_visibility(self, is_agent_visible: bool):
    self.is_agent_visible = is_agent_visible

  def get_cell(self, x: int, y: int) -> Cell | None:
    """Gets a cell using its x and y coordinates. Visualize (0,0) as the top left of the grid.

    Args:
        x (int): The column index (horizontal position). Positive means to the right of the grid.
        y (int): The row index (vertical position). Positive means down the grid.

    Returns:
        Cell | None: The cell at the given coordinates.
    """
    if not self.is_valid_position(x, y):
      return None

    return self.matrix[y][x]  # y is row index, x is column index

  def get_start_cell(self) -> Cell:
    """Returns the starting cell

    Raises:
      RuntimeError: When starting cell doesn't exist

    Returns:
        Cel: The starting cell. If shouldn't return None unless the Grid class's `start_pos` attribute was modified erroneously.
    """
    start_cell = self.get_cell(self.start_pos[0], self.start_pos[1])
    if not start_cell:
      raise RuntimeError(
        "Start cell does not exist. Ensure grid.start_pos isn't modified after Grid class instantiation!"
      )

    return start_cell

  def get_goal_cell(self) -> Cell:
    """Returns the goal cell

    Raises:
      RuntimeError: When goal cell doesn't exist

    Returns:
        Cel: The goal cell.
    """
    goal_cell = self.get_cell(self.end_pos[0], self.end_pos[1])
    if not goal_cell:
      raise RuntimeError(
        "Goal cell does not exist. Ensure grid.start_pos isn't modified after Grid class instantiation!"
      )

    return goal_cell

  def is_goal_cell(self, cell: Cell) -> bool:
    """Returns whether or not a given cell is the goal or end cell

    Args:
        cell (Cell): Cell being compared

    Returns:
        bool: If true, then cell is the goal cell.
    """
    return cell.x == self.end_pos[0] and cell.y == self.end_pos[1]

  def is_valid_position(self, x: int, y: int) -> bool:
    # If within horizontal index range AND vertical index range
    return (x >= 0 and x < self.num_cols) and (y >= 0 and y < self.num_rows)

  def get_neighbor(self, cell: Cell, direction: Direction):
    """Gets the neighbor of the the cell in the corresponding direction. E.g. if direction was UP, get the neighbor above `cell`.

    Args:
        cell (Cell): Cell whose neighbor we are getting
        direction (Direction): The direction in which we should fetch the neighbor

    Returns:
      Cell: The neighbor in the direction of the cell that was passed.

    NOTE: The only way this will return None is if you pick a cell on the edge and
    purposely try to access it. Though for that case I'm just going to throw an error because
    that simply shouldn't be happening in the app.
    """

    change_x, change_y = direction.value
    new_x = cell.x + change_x
    new_y = cell.y + change_y
    return self.get_cell(new_x, new_y)

  def get_all_neighbors(self, cell: Cell) -> list[Cell]:
    """Return all neighbor for a given cell

    Args:
        cell (Cell): Cell whose neighbors we are calculating

    Returns:
        list[Cell]: List of neighbors
    """

    # For every possible direction, extract the change in index, and calculate
    # the index the neighbors would be at. After validating that they are valid positions
    # (meaning the neighbors should be there), add the neighbors at those indices to our list of neighbors to return.
    neighbors: list[Cell] = []
    for direction in Direction:
      change_x, change_y = direction.value
      new_x = cell.x + change_x
      new_y = cell.y + change_y
      if self.is_valid_position(new_x, new_y):
        neighbors.append(self.get_cell(new_x, new_y))

    return neighbors

  def get_path_neighbors(self, cell: Cell) -> list[Cell]:
    """Given a cell, return a list of neighboring cells that have their walls down.

    Args:
        cell (Cell): _description_

    Returns:
        list[Cell]: _description_

    NOTE: You can assume that you only need to check if the wall in the direction
    of the current cell is down, rather than needing to check both cell walls.
    """

    """
    Iterate through all directions:
      1. If the cell's wall in that direction is down, then that 
      means that the cell in that direction cna be traversed to.
      2. Add this neighbor cell to our list
    """
    path_neighbors = []
    for dir in Direction:
      if not cell.get_wall(dir):
        path_neighbors.append(self.get_neighbor(cell, dir))

    return path_neighbors

  def remove_wall(self, cell: Cell, neighbor: Cell) -> None:
    """Removes a shared wall between two cells.
    Args:
        cell (Cell): A cell
        neighbor (Cell): The cell's assumed neighbor
    """

    """
    For each direction:
      a. add the displacement of that direction to the current cell's indices; get the tuple
      b. If indices match, then we can safely say that cell and neighbor are neighbors 
      and we correctly found the direction in which we can move from cell to neighbor.
    """
    direction_to_neighbor = None
    for direction in Direction:
      change_x, change_y = direction.value
      if cell.x + change_x == neighbor.x and cell.y + change_y == neighbor.y:
        direction_to_neighbor = direction

    if direction_to_neighbor is None:
      raise ValueError(f"Failed to determine the direction from {cell} to {neighbor}!")

    direction_from_neighbor = direction_to_neighbor.opposite

    # Mark these as false, on the next render, the wall won't be drawn
    cell.set_wall(direction_to_neighbor, False)
    neighbor.set_wall(direction_from_neighbor, False)

  def reset_visited_cells(self):
    """Sets the visited status of all nodes to false. This is here to help with maze generation algorithms since
    many of them use a visited list, and it's convenient for them to use the is_visited property"""
    for x in range(self.num_cols):
      for y in range(self.num_rows):
        cell = self.get_cell(x, y)
        cell.set_is_visited(False)

  def get_list_index(self, cell: Cell) -> int:
    """Gets the list index for a given set of coordinates

    Args:
        x (int): Column index
        y (int): Row index

    Returns:
        int: The list index for a cell in that position.

    NOTE: If the matrix were flatten down into a giant list, this function maps an x-y index coordinate
    into an index for that giant list. (x,y) -> x. This can be used as a unique identifier for the given cell.
    """
    return cell.y * self.num_cols + cell.x

  def get_cell_walls(self, cell: Cell):
    """Gets all valid walls of a given cell.

    Args:
        cell (Cell): The cell whose walls we are fetching.

    Returns:
        list[tuple[Cell, Direction]]: A list of tuples, where each tuple contains:
            - The neighboring cell on the other side of the wall.
            - The direction of the wall.
    """
    walls = []
    for direction in Direction:
      neighbor = self.get_neighbor(cell, direction)
      if neighbor and cell.get_wall(direction):  # Wall is "up" and neighbor exists
        walls.append((cell, neighbor, direction))
    return walls

  def get_all_walls(self) -> list[tuple[Cell, Cell, Direction]]:
    """Returns a list of all walls in a maze

    Returns:
        list[tuple[Cell, Cell, Direction]]: A list of walls, where each wall is represented as a tuple
        (cell1, cell2, direction), with cell1 being the starting cell, cell2 being the neighboring cell,
        and direction being the direction from cell1 to cell2.
    """
    walls = []
    for y in range(self.num_rows):
      for x in range(self.num_cols):
        cell = self.get_cell(x, y)
        # For each cell, check each direction to see if there's a built wall that's shared by 2 cells;
        # If so, then add it to our array.
        for direction in Direction:
          neighbor = self.get_neighbor(cell, direction)
          if neighbor and cell.get_wall(direction):
            walls.append((cell, neighbor, direction))
    return walls

  def reset_solved_state(self):
    """Resets the path for all cells in the grid.

    This is useful for algorithms that need to re-calculate paths without needing to create a new instance of the grid.
    """
    for y in range(self.num_rows):
      for x in range(self.num_cols):
        cell = self.get_cell(x, y)
        cell.reset()
