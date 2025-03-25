from enum import Enum


class Direction(Enum):
  UP = (0, -1)
  DOWN = (0, 1)
  LEFT = (-1, 0)
  RIGHT = (1, 0)

  @property
  def opposite(self):
    opposites = {
      Direction.UP: Direction.DOWN,
      Direction.DOWN: Direction.UP,
      Direction.LEFT: Direction.RIGHT,
      Direction.RIGHT: Direction.LEFT,
    }
    return opposites[self]
