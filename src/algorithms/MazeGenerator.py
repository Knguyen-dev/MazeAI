import random
import time

from grid.Cell import Cell
from grid.Grid import Grid


class MazeGenerator:

  def __init__(self, delay: float = 0):
    self.delay = delay
  
  def test_draw_pattern(self, grid: Grid, update_callback=None):
    # Alternate between removing the top and bottom
    for y in range(grid.num_rows):
      for x in range(grid.num_cols):
        # For all diagonal cells remove their walls. To achieve this, you need to 
        # set the boolean walls of the said diagonal to false, and then also set 
        # the neighboring walls to have their booleans (for the shared wall) to false
        if x == y:
          cell = grid.get_cell(x,y)
          neighbors = grid.get_all_neighbors(cell)
          # Then for each neighbor, remove the shared wall it has with the given diagonal
          for n in neighbors:
            grid.remove_wall(cell, n)
            # You removed a wall, update the drawing of the screen
            if update_callback:
              update_callback()
              time.sleep(self.delay)
    print("Completed test draw pattern")

  def recursive_backtracker(self, grid: Grid, update_callback=None):
    """Creates a maze out of a grid using the recursive backtracker algorithm.
    Args:
        grid (Grid): Grid being drawn
        update_callback (Function, optional): Function that allows us to update an animation frame. Defaults to None.
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
      already bisited would make those algorithms not work as expected.
    '''
    stack: list[Cell] = [grid.get_cell(0, 0)]
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
    grid.reset_visited_cells()    
  
  def randomized_prim(self, grid: Grid, update_callback=None):
    pass

  def randomized_kruskal(self, grid: Grid, update_callback=None):
    pass
  