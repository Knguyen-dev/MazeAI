import heapq
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
            
  @staticmethod
  def depth_first_search(grid: Grid, update_callback=None) -> None:
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
  
  @staticmethod
  def greedy_best_first(grid:Grid, update_callback=None):
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
  
  @staticmethod
  def dijkstra(grid: Grid, update_callback=None):
    """Performs uniform

    Args:
        grid (Grid): _description_
        update_callback (_type_, optional): _description_. Defaults to None.
    """
    '''
    Algorithm:
    1. Initialize start cell and set it to visited (the latter for highlighting purposes); It's marked as visited on the first iteration.
    2. Create a priority queue; list of nodes that need to be expanded or even re-expanded
    3. Create a map "costs" that keeps track of the least cost from start to node n that we've found so far; 
    4. While frontier still has nodes
      a. Obtain the cell with the least cost; pop this from the open set (priority queue); 
      b. Skip the cell if it's already been expanded. Else set the current cell as visited and to be expanded.
      c. If the cell is the goal cell:
        - reconstruct path and end search.
      d. Iterate through unvisited neighbors; we don't want to waste time over already expanded cells:
        - Calculate cost to get to neighbor from the start.
        - If neighbor's cost hasn't been recorded (never in fringe) or the neighbor cost is cheaper than what was previously recorded:
          1. Record the parent of the neighbor
          2. Update the summed cost for the neighbor 
          3. Add neighbor to the heap
          4. If call the update_callback function was defined, call it for animation
    NOTE: When the priorities of two objects are equal then heap will try to do an object comparison. This can cause issues for our implementation
    as we're comparing complex objects. So to avoid this, we'll use an unique ID, an index. Remember the idea with 
    A* is that when we expand a node, we visit it, but we are guaranteed that this is the cheapest cost from start to this node.
    The "optimization" comes in when we expand neighbors, and we find a cheaper path from start to node n.
    '''
    start = grid.get_start_cell()
    costs = {start: 0}
    frontier = []
    heapq.heappush(frontier, (costs[start], grid.get_list_index(start.x, start.y), start)) 
    while frontier:
      cost, _, current = heapq.heappop(frontier)  # Ignore the unique identifier
      if current.get_is_visited():
        continue
      current.set_is_visited(True)
      if grid.is_goal_cell(current):
        MazeSolver.reconstruct_path(current)
        return  
      for neighbor in grid.get_path_neighbors(current):
        if neighbor.get_is_visited():
          continue
        neighbor_cost = costs[current] + neighbor.weight
        '''
        Two cases:
        - Neighbor hasn't been recorded in the fringe, via being tracked by cost.
        - Neighbor is in cost (already visited), but it's cheaper now
        In this case update cost and add it to the fringe.
        '''
        if neighbor not in costs or neighbor_cost < costs[neighbor]:
          neighbor.parent = current
          costs[neighbor] = neighbor_cost
          heapq.heappush(frontier, (neighbor_cost, grid.get_list_index(neighbor.x, neighbor.y), neighbor))  # Add unique identifier
          if (update_callback):
            update_callback()

  @staticmethod
  def a_star(grid:Grid, update_callback=None):
    """Performs A* search on the grid.
    Args:
      grid (Grid): Grid being searched
      update_callback (_type_, optional): Callback to update visualization. Defaults to None.
    """
    start = grid.get_start_cell()
    goal = grid.get_cell(grid.end_pos[0], grid.end_pos[1])
    g_scores = {start: 0}
    f_scores = {start: MazeSolver.manhattan_distance(start, goal)}
    
    # priority queue: (f_score, cell)
    open_set = [(f_scores[start], start)]
    
    # track cells in the open set for O(1) lookups
    open_set_hash = {start}
    
    while open_set:
      open_set.sort(key=lambda x: x[0])
      _, current = open_set.pop(0)
      open_set_hash.remove(current)
      current.set_is_visited(True)
      if grid.is_goal_cell(current):
        MazeSolver.reconstruct_path(current)
        return
      for neighbor in grid.get_path_neighbors(current):
        tentative_g_score = g_scores[current] + neighbor.weight
        # case: path to neighbor is better than any previous one
        if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
          # update neighbor's scores and parent
          neighbor.parent = current
          g_scores[neighbor] = tentative_g_score
          f_scores[neighbor] = tentative_g_score + MazeSolver.manhattan_distance(neighbor, goal)
          if neighbor not in open_set_hash and not neighbor.get_is_visited():
            open_set.append((f_scores[neighbor], neighbor))
            open_set_hash.add(neighbor)
            if update_callback:
              update_callback()

  # Focus on these
  # UCS (Dijkstra)
  # A*
  # JPS (Jump Point Search) (challenge)
  # Optional and for fun:
  # wall following (left or right hand rule), pledge algorithm, tremaux, dead end filling, 
  # bellman-ford