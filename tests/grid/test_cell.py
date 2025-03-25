
import pytest

from grid.Cell import Cell
from utils.Direction import Direction


@pytest.fixture
def cell():
  return Cell(0, 0)

def test_initial_walls(cell):
  assert cell.walls[Direction.UP]
  assert cell.walls[Direction.DOWN]
  assert cell.walls[Direction.LEFT]
  assert cell.walls[Direction.RIGHT]

def test_set_wall(cell):
  cell.set_wall(Direction.UP, False)
  assert not cell.walls[Direction.UP]
  cell.set_wall(Direction.DOWN, True)
  assert cell.walls[Direction.DOWN]
