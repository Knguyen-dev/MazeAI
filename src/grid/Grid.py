import pygame

from grid.Cell import Cell
from utils.Direction import Direction


class Grid:
  def __init__(self, surface: pygame.Surface, num_rows: int, num_cols: int, cell_size: int, cell_wall_width: int):
    """_summary_

    Args:
        num_rows (int): Number of rows in the grid. This determines the height
        num_cols (int): Number of columns in the grid. This determines the width

    NOTE: While in the real app you're probably going to only use one grid, it's
    helpful to have initialization arguments for testing.
    """
    self.surface = surface
    self.num_rows = num_rows
    self.num_cols = num_cols
    self.cell_size = cell_size
    self.cell_wall_width = cell_wall_width

    # Initialize the matrix of cells
    self.matrix: list[list[Cell]] = []
    for y in range(num_rows):
      cell_row: list[Cell] = []
      for x in range(num_cols):
        cell_row.append(Cell(x, y))
      self.matrix.append(cell_row)

  def draw(self) -> None:
    for row in self.matrix:
      for cell in row:
        cell.draw(
          self.surface,
          self.cell_size,
          self.cell_wall_width
        )

  def get_cell(self, x: int, y: int) -> Cell | None:
    """Gets a cell using its x and y coordinates. Visualize (0,0) as the top left of the grid.

    Args:
        x (int): The column index (horizontal position). Positive means to the right of the grid.
        y (int): The row index (vertical position). Positive means down the grid.

    Returns:
        Cell: The cell at the given coordinates.

    Raises:
        IndexError: If the coordinates are out of bounds.
    """
    if not self.is_valid_position(x, y):
        return None

    return self.matrix[y][x]  # y is row index, x is column index
  
  def is_valid_position(self, x: int, y: int) -> bool:
    # If within horizontal index range AND vertical index range
    return (x >= 0 and x < self.num_cols) and (y >= 0 and y < self.num_rows)

  def get_neighbor(self, cell: Cell, direction: Direction) -> Cell:
    """Gets the neighbor of the the cell in the corresponding direction. E.g. if direction was UP, get the neighbor above `cell`.

    Args:
        cell (Cell): Cell whose neighbor we are getting
        direction (Direction): The direction in which we should fetch the neighbor

    Raises:
      IndexError: When the neighbor's indices are out of range

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

  def get_all_unvisited_neighbors(self, cell: Cell) -> list[Cell]:
    """Gets all unvisited neighbors of a given cell

    Args:
        cell (Cell): _description_

    Returns:
        list[Cell]: _description_
    """
    return list(filter(lambda neighbor: not neighbor.is_visited, self.get_all_neighbors(cell)))

  def remove_wall(self, cell: Cell, neighbor: Cell) -> None:
    """Removes a shared wall between two cells.
    Args:
        cell (Cell): A cell
        neighbor (Cell): The cell's assumed neighbor
    """

    '''
    For each direction:
      a. add the displacement of that direction to the current cell's indices; get the tuple
      b. If indices match, then we can safely say that cell and neighbor are neighbors 
      and we correctly found the direction in which we can move from cell to neighbor.
    '''
    direction_to_neighbor = None
    for direction in Direction:
      change_x, change_y = direction.value
      if (cell.x + change_x == neighbor.x and cell.y + change_y == neighbor.y):
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
        cell.is_visited = False