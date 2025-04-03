import random

from algorithms.UnionFind import UnionFind
from grid.Cell import Cell
from grid.Grid import Grid


class MazeGenerator:

  @staticmethod
  def add_imperfections(grid: Grid, imperfection_rate: float, update_callback=None) -> None:
        """Adds imperfections to a perfect maze by randomly removing walls.

        Args:
            grid (Grid): The grid representing the maze.
            imperfection_rate (float): A value between 0 and 1 indicating the percentage of walls to remove.
            update_callback (callable, optional): Function to update the visualization. Defaults to None.
        """
        # Calculate the total number of walls in the grid and number of walls to remove
        # Collect all possible walls;; if there aren't any early return
        possible_walls = grid.get_all_walls()
        if not possible_walls:
           return
        
        # From the number of possible walls we have; find the percentage to remove
        walls_to_remove = int(len(possible_walls) * imperfection_rate)

        # Randomly remove walls; 
        random.shuffle(possible_walls)
        for _ in range(walls_to_remove):
            cell, neighbor, direction = possible_walls.pop()
            grid.remove_wall(cell, neighbor)
            if update_callback:
                update_callback()
  
  @staticmethod
  def recursive_backtracker(grid: Grid, update_callback=None) -> None:
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
        filter(lambda neighbor: not neighbor.get_is_visited(), grid.get_all_neighbors(current_cell))
      )

      if unvisited_neighbors:
        neighbor_index = random.randint(0, len(unvisited_neighbors) - 1)
        stack.append(current_cell)
        randomly_chosen_neighbor = unvisited_neighbors[neighbor_index]
        grid.remove_wall(current_cell, randomly_chosen_neighbor)

        randomly_chosen_neighbor.set_is_visited(True) 
        stack.append(randomly_chosen_neighbor)
        if update_callback:
          update_callback()

    # NOTE: It's critical that we reset the is_visited state on each of the cells for our 
    # maze solving algorithms to work. Because if we don't it tells the program that 
    # all the cells are already visited, and that causes problems with the search algorithm to know which 
    # cells should be expanded or added to their respective data structures.
    grid.reset_visited_cells()    

  @staticmethod
  def randomized_kruskal(grid: Grid, update_callback=None):
    """Runs the iterative randomized Kruskal's algorithm (with sets).

    Args:
        grid (Grid): _description_
        update_callback (_type_, optional): _description_. Defaults to None.
    """
    '''
    Algorithm:
    1. Create a list of walls; 
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
    walls = grid.get_all_walls()
    if not walls:
       print("Hey no walls to do maze generation on")
       return
    
    random.shuffle(walls)
    for wall in walls:
       cell_index = grid.get_list_index(wall[0].x, wall[0].y)
       neighbor_index = grid.get_list_index(wall[1].x, wall[1].y)
       if not unionFind.connected(cell_index, neighbor_index):
          grid.remove_wall(wall[0], wall[1])
          unionFind.unionByRank(cell_index, neighbor_index)
          if update_callback:
             update_callback()

  @staticmethod
  def randomized_prim(grid: Grid, update_callback=None) -> None:
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
    if not walls:
       return

    while walls:
        wall_index = random.randint(0, len(walls) - 1)
        cell, neighbor, direction = walls.pop(wall_index)
        if not neighbor.get_is_visited():
            grid.remove_wall(cell, neighbor)
            neighbor.set_is_visited(True)
            walls.extend(grid.get_cell_walls(neighbor))
            if update_callback:
                update_callback()

    grid.reset_visited_cells()  