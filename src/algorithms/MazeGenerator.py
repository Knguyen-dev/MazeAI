import random
import time

from algorithms.UnionFind import UnionFind
from grid.Cell import Cell
from grid.Grid import Grid
from utils.Direction import Direction


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
    2. Obtain all unvisited neighbor cells; these represent valid moves
    3. If there are unvisited neighbors:
      a. Choose a random neighbor to expand into; here we do that by choosing its index in the list
      b. Push the current cell back onto the stack. The reason we do this for backtracking reasons. We know that there
      are other unvisited nodes at the current cell, which we'll have to process later, so save the current cell for later processing 
      whilst we expand into a neighbor recursively.
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
      
      unvisited_neighbors = list(
        filter(lambda neighbor: not neighbor.get_is_visited(), self.get_all_neighbors(current_cell))
      )

      if unvisited_neighbors:
        neighbor_index = random.randint(0, len(unvisited_neighbors) - 1)
        stack.append(current_cell)
        randomly_chosen_neighbor = unvisited_neighbors[neighbor_index]
        grid.remove_wall(current_cell, randomly_chosen_neighbor)

        randomly_chosen_neighbor.set_is_visited(True) 
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
    1. Create a list of walls; we've done this through a for loop that has 2 conditions; each wall is in form (x_index,y_index, direction)
    2. Create a set for each cell, each containing just that set. Well use a disjoint set data structure for this.
    3. Randomize the list of walls
    4. For each wall (iteration):
      a. Get the cells that are divided by this wall.
      c. if these cells belong to distinct sets:
        - Remove the current wall
        - Join the sets of the formerly divided cells.

    NOTE: We're going to map each cell to a unique index in range [0, num_cols*num_rows-1]. This allows us to 
    associate a cell with a given node in the UnionFind. 
    '''
    unionFind = UnionFind(grid.num_cols * grid.num_rows)
    walls = []
    for x in range(grid.num_cols):
      for y in range(grid.num_rows):

        # Add the right wall if not on the last column
        if x < grid.num_cols - 1:
          walls.append((x,y,Direction.RIGHT)) 

        # Add the bottom wall if not on the last row
        if y < grid.num_rows - 1:
          walls.append((x,y,Direction.DOWN))

    random.shuffle(walls)

    for wall in walls:
      cell = grid.get_cell(wall[0], wall[1])
      neighbor = grid.get_neighbor(cell, wall[2])
      cell_index = grid.get_list_index(cell.x, cell.y)
      neighbor_index = grid.get_list_index(neighbor.x, neighbor.y)
      if not unionFind.connected(cell_index, neighbor_index):
        grid.remove_wall(cell, neighbor)
        unionFind.unionByRank(cell_index, neighbor_index)
        if update_callback:
          time.sleep(self.delay)
          update_callback()

  def randomized_prim(self, grid: Grid, update_callback=None) -> None:
    """Runs the randomized prim's algorithm on a grid. This uses the iterative approach, which allows it to work on large mazes.

    Args:
        grid (Grid): Grid that the algorithm is being run on.
        update_callback (Function, optional): Function that updates the grid display whilst the function is being run.
    """
    '''
    Algorithm:
    1. Pick a cell to start the maze generation from; mark the cell as visited and add its walls (add valid walls only) a wall list
    2. Randomly pick a wall.
    3. If the neighbor (some cell) is not visited 
      a. Remove the wall between that cell and neighbor
      b. Mark the neighbor as visited
      c. Add all the walls of the neighbor to the walls list
      d. Update the animation frame
    '''
    start_cell = grid.get_start_cell()
    start_cell.set_is_visited(True)
    walls = grid.get_cell_walls(start_cell)
    while walls:
        wall_index = random.randint(0, len(walls) - 1)
        cell, neighbor, direction = walls.pop(wall_index)
        if not neighbor.get_is_visited():
            grid.remove_wall(cell, neighbor)
            neighbor.set_is_visited(True)
            walls.extend(grid.get_cell_walls(neighbor))
            if update_callback:
                time.sleep(self.delay)
                update_callback()

    grid.reset_visited_cells()
    

  
  