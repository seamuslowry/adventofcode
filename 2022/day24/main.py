from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3
  NONE = 4

@dataclass
class Movement:
  dr: int
  dc: int

MOVEMENTS = {
  Direction.UP: Movement(dr=-1,dc=0),
  Direction.DOWN: Movement(dr=1,dc=0),
  Direction.LEFT: Movement(dr=0,dc=-1),
  Direction.RIGHT: Movement(dr=0,dc=1),
  Direction.NONE: Movement(dr=0,dc=0)
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
      print_char = '.'
      if position in rocks:
        print_char += '#'
      if Hurricane(position=position, direction=Direction.UP) in hurricanes:
        print_char += '^'
      if Hurricane(position=position, direction=Direction.RIGHT) in hurricanes:
        print_char += '>'
      if Hurricane(position=position, direction=Direction.LEFT) in hurricanes:
        print_char += '<'
      if Hurricane(position=position, direction=Direction.DOWN) in hurricanes:
        print_char += 'v'
      print(print_char[-1] if len(print_char) <= 2 else len(print_char) - 1, end='')
    print('')

def shortest_path(current_position: Position, desired_position: Position, hurricanes: set[Hurricane], rocks: set[Position], max_row: int, max_col: int, first_step: int) -> int:
  current_step = first_step
  current_possibilities = {current_position}


  while desired_position not in current_possibilities:
    current_step += 1
    current_hurricane_positions = set(map(lambda h: h.position, hurricanes_at_step(current_step, hurricanes, max_row=max_row, max_col=max_col)))
    all_possibilities = { Position(row = position.row + movement.dr, col = position.col + movement.dc) for movement in MOVEMENTS.values() for position in current_possibilities }
    current_possibilities = all_possibilities - rocks - current_hurricane_positions

  return current_step

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

  return shortest_path(start_position, end_position, hurricanes, rocks, max_row, max_col, 0)

def p2():
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

  first_trip = shortest_path(start_position, end_position, hurricanes, rocks, max_row, max_col, 0)
  second_trip = shortest_path(end_position, start_position, hurricanes, rocks, max_row, max_col, first_trip)
  return shortest_path(start_position, end_position, hurricanes, rocks, max_row, max_col, second_trip)

print(p1())
print(p2())