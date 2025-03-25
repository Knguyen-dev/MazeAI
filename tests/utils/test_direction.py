from utils.Direction import Direction


def test_direction_values():
  assert Direction.UP.value == (0, -1)
  assert Direction.DOWN.value == (0, 1)
  assert Direction.LEFT.value == (-1, 0)
  assert Direction.RIGHT.value == (1, 0)

def test_opposite_directions():
  assert Direction.UP.opposite == Direction.DOWN
  assert Direction.DOWN.opposite == Direction.UP
  assert Direction.LEFT.opposite == Direction.RIGHT
  assert Direction.RIGHT.opposite == Direction.LEFT
