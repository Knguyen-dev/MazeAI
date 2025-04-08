import heapq
import math
from collections import deque

from grid.Cell import Cell
from grid.Grid import Grid


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
    goal = grid.get_goal_cell()
    start.set_is_visited(True)
    queue = []
    heapq.heappush(queue, (MazeSolver.manhattan_distance(start, goal), grid.get_list_index(start.x, start.y), start))  # Add unique identifier
    while queue:
      
      distance, index, current_node = heapq.heappop(queue)
      
      if grid.is_goal_cell(current_node):
        MazeSolver.reconstruct_path(current_node)
        return
      for neighbor in grid.get_path_neighbors(current_node):
        if not neighbor.get_is_visited():
          neighbor.set_is_visited(True)
          neighbor.parent = current_node
          
          # add to queue with its heuristic value
          heuristic = MazeSolver.manhattan_distance(neighbor, goal)
          heapq.heappush(queue, (heuristic, grid.get_list_index(neighbor.x, neighbor.y), neighbor)) 
          if update_callback:
            update_callback()
  
  @staticmethod
  def dijkstra(grid: Grid, update_callback=None):
    """Performs uniform

    Args:
        grid (Grid): _description_
        update_callback (_type_, optional): _description_. Defaults to None.
    NOTE: Algorithm is the same as A*, except we're not going to use heuristics. Dijkstra ends up exploring the entire graph most of 
    the time being it has no idea where the goal is, and so it constantly expands. Since we're basically in a uniform weight graph, it's going to
    expand in all directions instead of towards some region.
    """
    start = grid.get_start_cell()
    start_index = grid.get_list_index(start.x, start.y)
    costs = {start_index: 0}

    open_set = []
    heapq.heappush(open_set, (costs[start_index], start_index, start)) 
    open_set_hash = {start_index}

    while open_set:
      g_score, current_index, current_node = heapq.heappop(open_set)
      open_set_hash.remove(current_index)
      current_node.set_is_visited(True)

      if grid.is_goal_cell(current_node):
        MazeSolver.reconstruct_path(current_node)
        return

      for neighbor in grid.get_path_neighbors(current_node):
        tentative_g_score = costs[current_index] + neighbor.weight
        neighbor_index = grid.get_list_index(neighbor.x, neighbor.y)

        # Case: If the neighbor hasn't been seen before, or the current path from start to neighbor is cheapest than the previous one found
        # In this case, update scores, and add neighbor to visited list if it's not there already.
        if neighbor_index not in costs or tentative_g_score < costs[neighbor_index]:
          neighbor.parent = current_node
          costs[neighbor_index] = tentative_g_score
          
          if neighbor_index not in open_set_hash:
            heapq.heappush(open_set, (costs[neighbor_index], neighbor_index, neighbor))
            open_set_hash.add(neighbor_index)
            if update_callback:
              update_callback()

  @staticmethod
  def a_star(grid:Grid, update_callback=None):
    """Performs A* search on the grid.
    Args:
      grid (Grid): Grid being searched
      update_callback (_type_, optional): Callback to update visualization. Defaults to None.
    """
    start = grid.get_start_cell()
    start_index = grid.get_list_index(start.x, start.y) 
    goal = grid.get_goal_cell()
    g_scores = {start_index: 0}
    f_scores = {start_index: MazeSolver.manhattan_distance(start, goal)}
    
    # priority queue: (f_score, cell)
    open_set = []
    heapq.heappush(open_set, (f_scores[start_index], start_index, start)) 
    
    # track cells in the open set for O(1) lookups
    open_set_hash = {start_index}
    
    while open_set:
      # Pop node with smallest f_score from open_set, mark it as visited and remove it from open set (both the heap and map)
      f_score, current_index, current_node = heapq.heappop(open_set)
      open_set_hash.remove(current_index)
      current_node.set_is_visited(True)
      
      if grid.is_goal_cell(current_node):
        MazeSolver.reconstruct_path(current_node)
        return
      
      for neighbor in grid.get_path_neighbors(current_node):
        tentative_g_score = g_scores[current_index] + neighbor.weight
        neighbor_index = grid.get_list_index(neighbor.x, neighbor.y)

        # Case: If the neighbor hasn't been seen before, or the current path from start to neighbor is cheapest than the previous one found
        # In this case, update scores, and add neighbor to visited list if it's not there already.
        if neighbor_index not in g_scores or tentative_g_score < g_scores[neighbor_index]:
          neighbor.parent = current_node
          g_scores[neighbor_index] = tentative_g_score
          f_scores[neighbor_index] = tentative_g_score + MazeSolver.manhattan_distance(neighbor, goal)
          if neighbor_index not in open_set_hash:
            heapq.heappush(open_set, (f_scores[neighbor_index], neighbor_index, neighbor))
            open_set_hash.add(neighbor_index)
            if update_callback:
              update_callback()

  
  # JPS (Jump Point Search) (challenge)
  