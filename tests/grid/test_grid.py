from grid.Grid import Grid
from utils.Direction import Direction


# ----------------------------
# testing is_valid_position
# ----------------------------
def test_is_valid_position():
  grid = Grid(5, 5)

  # Test all positions that should be valid
  # rowIndex in range = [0, 4]
  # colIndex in range = [0, 4]
  for rowIndex in range(5):
    for colIndex in range(5):
      assert grid.is_valid_position(colIndex, rowIndex)

  # Invalid positions
  assert not grid.is_valid_position(-1, 0)  # out of bounds (negative x)
  assert not grid.is_valid_position(0, -1)  # out of bounds (negative y)
  assert not grid.is_valid_position(5, 5)  # out of bounds (x and y > max)

# ----------------------------
# testing get_neighbor
# ----------------------------
def test_get_neighbor_center():
  grid = Grid(5, 5)
  cell = grid.get_cell(2, 2)

  # Test getting neighbors in each direction
  up_neighbor = grid.get_neighbor(cell, Direction.UP)
  down_neighbor = grid.get_neighbor(cell, Direction.DOWN)
  left_neighbor = grid.get_neighbor(cell, Direction.LEFT)
  right_neighbor = grid.get_neighbor(cell, Direction.RIGHT)

  # Check neighbor positions
  assert up_neighbor.x == 2 and up_neighbor.y == 1
  assert down_neighbor.x == 2 and down_neighbor.y == 3
  assert left_neighbor.x == 1 and left_neighbor.y == 2
  assert right_neighbor.x == 3 and right_neighbor.y == 2

def test_get_neighbor_top_left():
  grid = Grid(5, 5)
  cell = grid.get_cell(0,0)

  # The top-left corner should only have right and down neighbors
  right_neighbor = grid.get_neighbor(cell, Direction.RIGHT)
  down_neighbor = grid.get_neighbor(cell, Direction.DOWN)

  assert right_neighbor.x == 1 and right_neighbor.y == 0
  assert down_neighbor.x == 0 and down_neighbor.y == 1

def test_get_neighbor_top_middle():
  grid = Grid(5, 5)

  cell = grid.get_cell(2, 0) # Middle of the top row

  right_neighbor = grid.get_neighbor(cell, Direction.RIGHT)
  down_neighbor = grid.get_neighbor(cell, Direction.DOWN)
  left_neighbor = grid.get_neighbor(cell, Direction.LEFT)

  assert right_neighbor.x == 3 and right_neighbor.y == 0
  assert down_neighbor.x == 2 and down_neighbor.y == 1
  assert left_neighbor.x == 1 and left_neighbor.y == 0

def test_get_neighbor_bottom_right():
  grid = Grid(5, 5)
  cell = grid.get_cell(4,4) # Bottom-right corner
  up_neighbor = grid.get_neighbor(cell, Direction.UP)
  left_neighbor = grid.get_neighbor(cell, Direction.LEFT)

  assert up_neighbor.x == 4 and up_neighbor.y == 3
  assert left_neighbor.x == 3 and left_neighbor.y == 4

def test_get_neighbor_bottom_middle():
  grid = Grid(5, 5)
  cell = grid.get_cell(2, 4) # Middle of the bottom row
  up_neighbor = grid.get_neighbor(cell, Direction.UP)
  left_neighbor = grid.get_neighbor(cell, Direction.LEFT)
  right_neighbor = grid.get_neighbor(cell, Direction.RIGHT)

  assert up_neighbor.x == 2 and up_neighbor.y == 3
  assert left_neighbor.x == 1 and left_neighbor.y == 4
  assert right_neighbor.x == 3 and right_neighbor.y == 4

# ----------------------------
# testing get_all_neighbors
# ----------------------------
def test_get_all_neighbors_center():
  grid = Grid(5, 5)
  cell = grid.get_cell(2, 2)  # Center cell
  neighbors = grid.get_all_neighbors(cell)

  # Expect 4 neighbors (up, down, left, right)
  assert len(neighbors) == 4

  # Check for up: x = 2 and y = 1
  assert any(n.x == 2 and n.y == 1 for n in neighbors)

  # Check for down: x = 2 and y = 3
  assert any(n.x == 2 and n.y == 3 for n in neighbors)  # DOWN

  # Check for left x = 1 and y = 2
  assert any(n.x == 1 and n.y == 2 for n in neighbors)  # LEFT

  # Check for right x = 3 and y = 2
  assert any(n.x == 3 and n.y == 2 for n in neighbors)  # RIGHT

def test_get_all_neighbors_corner():
  grid = Grid(5, 5)
  cell = grid.get_cell(0, 0) # Top left
  
  neighbors = grid.get_all_neighbors(cell)

  # expect only two neighbors: bottom and right
  assert len(neighbors) == 2

  # Check for bottom neighbor
  assert any(n.x == 0 and n.y == 1 for n in neighbors)

  # Check for right neighbor
  assert any(n.x == 1 and n.y == 0 for n in neighbors)

def test_get_all_neighbors_left_mid():
  grid = Grid(5,5)
  cell = grid.get_cell(0, 2)
  neighbors = grid.get_all_neighbors(cell)
  assert(len(neighbors) == 3)

  # Check for up
  assert any(n.x == 0 and n.y == 1 for n in neighbors)

  # Check for right
  assert any(n.x == 1 and n.y == 2 for n in neighbors)

  # Check for down
  assert any(n.x == 0 and n.y == 3 for n in neighbors)

# ----------------------------
# testing remove_wall_helper
# ----------------------------
def test_remove_wall_helper_vertical():
  grid = Grid(5,5)
  
  # Get the cell and its neighbor below
  cell = grid.get_cell(0, 2) 
  neighbor = grid.get_cell(0, 3)

  # remove the wall between them
  grid.remove_wall(cell, neighbor)

  # Check that the cell's down wall is false
  assert cell.walls[Direction.DOWN] is False

  # Check that the neighbor's top wall is false
  assert neighbor.walls[Direction.UP] is False


def test_remove_wall_helper_horizontal():
  grid = Grid(5,5)
  
  # Get the cell and its neighbor below
  cell = grid.get_cell(1, 1) 
  neighbor = grid.get_cell(2, 1)

  # remove the wall between them
  grid.remove_wall(cell, neighbor)

  # Check that the cell's down wall is false
  assert cell.walls[Direction.RIGHT] is False

  # Check that the neighbor's top wall is false
  assert neighbor.walls[Direction.LEFT] is False

  