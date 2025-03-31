from collections import deque

from grid.Cell import Cell
from grid.Grid import Grid
from grid.Renderer import Renderer
import math

class MazeSolver:
  
  @staticmethod
  def manhattan_distance(cell1: Cell, cell2: Cell) -> int:
    """Calculates the manhattan distance between two cells

    Args:
        cell1 (Cell): The first cell
        cell2 (Cell): The second cell

    Returns:
        int: Returns a 2D tuple containing the x and y delta
    
    NOTE: Maybe put this in the MazeSolver class 
    """
    # def abs(x, y):
    #   if (x-y < 0):
    #     return -(x-y)
    #   else:
    #     return x-y

    x_change = abs(cell1.x - cell2.x)
    y_change = abs(cell1.y - cell2.y)
    return x_change + y_change

  @staticmethod
  def euclidean_distance(cell1: Cell, cell2: Cell) -> float:
    """Calculates the euclidean distance between two cells.

    Args:
        cell1 (Cell): First cell
        cell2 (Cell): Second cell
    
    Returns:
      float: The euclidean distance between the two cells
    """
    def sqrt(x):
      return x ** 0.5
    return sqrt((cell1.x - cell2.x)**2 + (cell1.y - cell2.y)**2) 

  @staticmethod
  def reconstruct_path(cell: Cell) -> list[Cell]:
    """Reconstructs the path that leads to cell.

    Args:
        cell (Cell): End node on a given pat 

    Returns:
      list[Cell]: A list of cells that were in the start path to get to the current cell.
    """
    path = []
    while cell:
      path.insert(0, cell)
      cell.set_in_path(True)
      cell = cell.parent
    return path

  @staticmethod
  def breadth_first_search(grid: Grid, update_callback=None) -> None: 
    """Performs a breadth first search on the grid.

    Args:
        grid (Grid): Grid being searched
        update_callback (_type_, optional): _description_. Defaults to None.

    NOTE: With bfs, a cell is considered visited when it is added to the queue. The term visited depends on 
    the search algorithm.
    """
    '''
    Algorithm:
      1. Let Q be a queue
      2. Get the starting node and label it as explored. You can reason that it's also going to be in the path.
      3. Put the root in the node.
      4. While Q is not empty:
        a. Let current, a node from a queue
        b. If current is the goal node:
          - Return the path leading to current from start.
        c. Iterate through all unvisited neighbors:
          - label neighbor as explored
          - neighbor.parent = current
          - Enqueue neighbor
          - If update_callback exists, then call it with the delay. 
    
    NOTE: We're assuming there does exist a path from start to goal
    '''
    start = grid.get_start_cell()
    start.set_is_visited(True)

    queue = deque([start])
    while queue:
      current = queue.popleft()
      if grid.is_goal_cell(current):
        # realistically break out of the loop and in the final ends of the function run one last frame to render goal nodes
        MazeSolver.reconstruct_path(current)
        return
      for neighbor in grid.get_path_neighbors(current):
        if not neighbor.get_is_visited():
          neighbor.set_is_visited(True)
          neighbor.parent = current
          queue.append(neighbor)
          
          if update_callback:
            update_callback()
            
  def depth_first_search(self, grid: Grid, update_callback=None) -> None:
    """Performs a depth first search on the grid.

    Args:
      grid (Grid): Grid being searched
      update_callback (_type_, optional): Callback to update visualization. Defaults to None.

    """
    start = grid.get_start_cell()
    start.set_is_visited(True)
    stack = [start]
    
    while stack:
      current = stack.pop()  # pop from the end (lifo)
      if grid.is_goal_cell(current):
        MazeSolver.reconstruct_path(current)
        return
      
      for neighbor in grid.get_path_neighbors(current):
        if not neighbor.get_is_visited():
          neighbor.set_is_visited(True)
          neighbor.parent = current
          stack.append(neighbor)
          if update_callback:
            update_callback()
  
  def greedy_best_first(self, grid:Grid, update_callback=None):
    """
    Performs a greedy best first search on the grid.
    
    Args:
      grid (Grid): Grid being searched
      update_callback (_type_, optional): Callback to update visualization. Defaults to None.
    """
    start = grid.get_start_cell()
    goal = grid.get_cell(grid.end_pos[0], grid.end_pos[1])
    
    start.set_is_visited(True)
    
    # each element is a tuple of (heuristic_value, cell)
    queue = [(MazeSolver.manhattan_distance(start, goal), start)]
    
    while queue:
      # sort queue by heuristic value (lowest first)
      queue.sort(key=lambda x: x[0])
      
      _, current = queue.pop(0)
      
      if grid.is_goal_cell(current):
        MazeSolver.reconstruct_path(current)
        return
      
      for neighbor in grid.get_path_neighbors(current):
        if not neighbor.get_is_visited():
          neighbor.set_is_visited(True)
          neighbor.parent = current
          
          # add to queue with its heuristic value
          heuristic = MazeSolver.manhattan_distance(neighbor, goal)
          queue.append((heuristic, neighbor))
          
          if update_callback:
            update_callback()


  # Focus on these
  # UCS (Dijkstra)
  # A*
  # JPS (Jump Point Search) (challenge)
  # Optional and for fun:
  # wall following (left or right hand rule), pledge algorithm, tremaux, dead end filling, 
  # bellman-ford