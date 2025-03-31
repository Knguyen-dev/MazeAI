
import pytest

from grid.Cell import Cell
from utils.Direction import Direction


@pytest.fixture
def cell():
  return Cell(0, 0)

def test_initial_flags(cell):
    # Test that all flags are initially unset
    assert not cell.get_is_visited()
    assert not cell.get_in_path()


def test_set_visited(cell):
    # Test setting and clearing the visited flag
    cell.set_is_visited(True)
    assert cell.get_is_visited()
    cell.set_is_visited(False)
    assert not cell.get_is_visited()


def test_set_in_path(cell):
    # Test setting and clearing the in_path flag
    cell.set_in_path(True)
    assert cell.get_in_path()
    cell.set_in_path(False)
    assert not cell.get_in_path()


def test_initial_walls(cell):
    # Test that all walls are initially up
    assert cell.get_wall(Direction.UP)
    assert cell.get_wall(Direction.DOWN)
    assert cell.get_wall(Direction.LEFT)
    assert cell.get_wall(Direction.RIGHT)


def test_set_wall(cell):
    # Test setting and clearing walls
    cell.set_wall(Direction.UP, False)
    assert not cell.get_wall(Direction.UP)

    cell.set_wall(Direction.DOWN, True)
    assert cell.get_wall(Direction.DOWN)

    cell.set_wall(Direction.LEFT, False)
    assert not cell.get_wall(Direction.LEFT)

    cell.set_wall(Direction.RIGHT, True)
    assert cell.get_wall(Direction.RIGHT)