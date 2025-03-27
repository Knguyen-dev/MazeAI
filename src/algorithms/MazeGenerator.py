import random
import time

from grid.Cell import Cell
from grid.Grid import Grid


class MazeGenerator:

  def __init__(self, delay: float = 0):
    self.delay = delay

  def recursive_backtracker(self, grid: Grid, update_callback=None) -> None:
    """Creates a maze out of a grid using the recursive backtracker algorithm.
    Args:
        grid (Grid): Grid being drawn
        update_callback (Function, optional): Function that allows us to update an animation frame. Defaults to None.

    NOTE: Mazes created with this function need to produce long hallways due ot the depth first nature of the function.
    """
    '''
    Algorithm: 
    1. Let the starting cell be (x,y) = (0,0), and put it into the fringe (stack)
    2. Obtain all unvisited neighbor cells; these represent valid movse
    3. If there are unvisited neighbors:
      a. Choose a random neighbor to expand into; here we do that by choosing its index in the list
      b. Push the current cell back onto the stack. The reason we do this for backtracking reasons. We know that there
      are other unvisited nodes at the current cell, which we'll have to process later, so save the current cell for later processing 
      whlist we expand into a neighbor recursively.
      c. Remove the shared wall between the two cells
      d. Push the chosen neighbor onto the stack as we'll process it in the next iteration.
        Also mark the node as visited so we don't expand into it again. So the only time we would
        come back to the randomly chosen cell is through backtracking.
      e. Assuming "update_callback" was given, we call this to draw the state of the grid exactly after we 
      removed the wall. 
    4. Reset the visited cells. We know we're going to run search algorithms after this, and having nodes listed as 
      already visited would make those algorithms not work as expected.
    '''
    start_cell = grid.get_start_cell()
    stack: list[Cell] = [start_cell]
    while stack:
      current_cell = stack.pop()
      unvisited_neighbors = grid.get_all_unvisited_neighbors(current_cell)
      if unvisited_neighbors:
        neighbor_index = random.randint(0, len(unvisited_neighbors) - 1)
        stack.append(current_cell)
        randomly_chosen_neighbor = unvisited_neighbors[neighbor_index]
        grid.remove_wall(current_cell, randomly_chosen_neighbor)
        randomly_chosen_neighbor.is_visited = True
        stack.append(randomly_chosen_neighbor)
        if update_callback:
          time.sleep(self.delay)
          update_callback()

    # NOTE: It's critical that we reset the is_visited state on each of the cells for our 
    # maze solving algorithms to work. Because if we don't it tells the program that 
    # all the cells are already visited, and that causes problems with the search algorithm to know which 
    # cells should be expanded or added to their respective data structures.
    grid.reset_visited_cells()    

  def randomized_kruskal(self, grid: Grid, update_callback=None):
    """Runs the iterative randomized Kruskal's algorithm (with sets).

    Args:
        grid (Grid): _description_
        update_callback (_type_, optional): _description_. Defaults to None.
    """
    '''
    Algorithm:

    1. Create a list of walls, and create a set for each cell, each containing just that cell.
    2. For each wall, in some random order (iteration):
      a. if the cells divided by this wall belong to distinct sets:
        - Remove the current wall
        - Join the sets of the formerly divided cells.

    My thinking:
    1. list of walls = [ (x_index, y_index, direction), ...] could work. List of valid walls, so just be careful not to include the borders?
    2. For the set of cells
    2. Mix up the list and iterate
      3. 
    '''
    pass

  def randomized_prim(self, grid: Grid, update_callback=None) -> None:
    """Runs the randomized prim's algorithm on a grid. This uses the iterative approach, which allows it to work on large mazes.

    Args:
        grid (Grid): Grid that the algorithm is being run on.
        update_callback (Function, optional): Function that updates the grid dissplay whilst the function is being run.
    """


    '''
    Algorithm:
      1. Pick a cell to start the maze generation from
      2. 

    
    
    '''
    pass

  
  