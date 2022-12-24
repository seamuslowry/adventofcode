from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3

@dataclass
class Movement:
  dr: int
  dc: int

MOVEMENTS = {
  Direction.UP: Movement(dr=-1,dc=0),
  Direction.DOWN: Movement(dr=1,dc=0),
  Direction.LEFT: Movement(dr=0,dc=-1),
  Direction.RIGHT: Movement(dr=0,dc=1),
}

@dataclass(eq=True, frozen=True)
class Position:
  row: int
  col: int

@dataclass(eq=True, frozen=True)
class Hurricane:
  position: Position
  direction: Direction

def parse_input(lines: list[str]) -> tuple[set[Hurricane], set[Position]]:
  rocks = set()
  hurricanes = set()

  for row, line in enumerate(lines):
    for col, char in enumerate(line):
      position = Position(row=row,col=col)
      if char == '#':
        rocks.add(position)
      if char == '>':
        hurricanes.add(Hurricane(position=position,direction=Direction.RIGHT))
      if char == '^':
        hurricanes.add(Hurricane(position=position,direction=Direction.UP))
      if char == '<':
        hurricanes.add(Hurricane(position=position,direction=Direction.LEFT))
      if char == 'v':
        hurricanes.add(Hurricane(position=position,direction=Direction.DOWN))

  return (hurricanes,rocks)

def hurricane_at_step(step: int, hurricane: Hurricane, max_row: int, max_col: int, min_row: int = 1, min_col: int = 1) -> Hurricane:
  movement = MOVEMENTS[hurricane.direction]

  new_row = (((hurricane.position.row - min_row) + movement.dr * step) % (max_row - min_row)) + min_row
  new_col = (((hurricane.position.col - min_col) + movement.dc * step) % (max_col - min_col)) + min_col

  return Hurricane(position = Position(row = new_row, col = new_col), direction=hurricane.direction)

def hurricanes_at_step(step: int, hurricanes: set[Hurricane], max_row: int, max_col: int, min_row: int = 1, min_col: int = 1) -> set[Hurricane]:
  return set(hurricane_at_step(step, h, max_row, max_col, min_row, min_col) for h in hurricanes)

def print_map(hurricanes: set[Hurricane], rocks: set[Position], max_row: int, max_col: int):
  for row in range(max_row + 1):
    for col in range(max_col + 1):
      position = Position(row=row, col=col)
      if position in rocks:
        print('#', end='')
      elif Hurricane(position=position, direction=Direction.UP) in hurricanes:
        print('^', end='')
      elif Hurricane(position=position, direction=Direction.RIGHT) in hurricanes:
        print('>', end='')
      elif Hurricane(position=position, direction=Direction.LEFT) in hurricanes:
        print('<', end='')
      elif Hurricane(position=position, direction=Direction.DOWN) in hurricanes:
        print('v', end='')
      else:
        print('.', end='')
    print('')

def p1():
  input = open("input.txt", "r").read().splitlines()
  hurricanes, initial_rocks = parse_input(input)

  start_position = Position(row=0,col=1)
  end_position = Position(row=len(input) - 1, col = len(input[0]) - 2)

  # ensure you can't move up past the start or down past the end by blocking them with rocks
  rocks = initial_rocks.union({
    Position(row=start_position.row - 1, col=start_position.col),
    Position(row=end_position.row + 1, col=end_position.col)
  })

  max_row = max(initial_rocks, key=lambda r: r.row).row
  max_col = max(initial_rocks, key=lambda r: r.col).col

  for step in range(10):
    print(f'at step {step}')
    print_map(hurricanes_at_step(step, hurricanes, max_row=max_row, max_col=max_col), rocks, max_row=max_row, max_col=max_col)
    print('\n')


  return 0

def p2():
  input = open("input.txt", "r")
  return 0


print(p1())
print(p2())