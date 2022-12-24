from pprint import pprint
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Direction(Enum):
  NORTH = 0
  SOUTH = 1
  WEST = 2
  EAST = 3

@dataclass(frozen=True, eq=True)
class Position:
  row: int
  col: int

def north_positions(p: Position) -> set[Position]:
  return {
    Position(row=p.row - 1, col=p.col - 1),
    Position(row=p.row - 1, col=p.col),
    Position(row=p.row - 1, col=p.col + 1)
  }

def west_positions(p: Position) -> set[Position]:
  return {
    Position(row=p.row - 1, col=p.col - 1),
    Position(row=p.row, col=p.col - 1),
    Position(row=p.row + 1, col=p.col - 1)
  }

def south_positions(p: Position) -> set[Position]:
  return {
    Position(row=p.row + 1, col=p.col - 1),
    Position(row=p.row + 1, col=p.col),
    Position(row=p.row + 1, col=p.col + 1),
  }

def east_positions(p: Position) -> set[Position]:
  return {
    Position(row=p.row - 1, col=p.col + 1),
    Position(row=p.row, col=p.col + 1),
    Position(row=p.row + 1, col=p.col + 1),
  }

def adjacent_positions(p: Position) -> set[Position]:
  return {
    *north_positions(p),
    *east_positions(p),
    *west_positions(p),
    *south_positions(p)
  }

def propose_movement(elf_positions: set[Position], elf_position: Position, preferred_direction: Direction) -> Optional[Position]:
  if adjacent_positions(elf_position).isdisjoint(elf_positions):
    return None

  possible_moves: dict[Direction, Optional[Position]] = {
    Direction.NORTH: Position(row=elf_position.row - 1, col=elf_position.col) if north_positions(elf_position).isdisjoint(elf_positions) else None,
    Direction.SOUTH: Position(row=elf_position.row + 1, col=elf_position.col) if south_positions(elf_position).isdisjoint(elf_positions) else None,
    Direction.EAST: Position(row=elf_position.row , col=elf_position.col + 1) if east_positions(elf_position).isdisjoint(elf_positions) else None,
    Direction.WEST: Position(row=elf_position.row, col=elf_position.col - 1) if west_positions(elf_position).isdisjoint(elf_positions) else None,
  }

  for n in range(len(Direction)):
    move = possible_moves.get(Direction((preferred_direction.value + n) % len(Direction)), None)
    if move:
      return move

  return None


def play_round(round_number: int, starting_positions: set[Position]) -> set[Position]:
  preferred_direction = Direction(round_number % len(Direction))
  proposed_movements: dict[Position, Optional[Position]] = {}
  proposed_counts: dict[Position, int] = {}

  for position in starting_positions:
    proposed_movement = propose_movement(starting_positions, position, preferred_direction)
    proposed_movements[position] = proposed_movement
    if proposed_movement:
      proposed_counts[proposed_movement] = proposed_counts.get(proposed_movement,0) + 1
  
  ret = set()

  for old_position, new_position in proposed_movements.items():
    if new_position and proposed_counts[new_position] == 1:
      ret.add(new_position)
    else:
      ret.add(old_position)


  return ret

def print_positions(positions: set[Position]) -> None:
  row_max = max(positions, key=lambda p: p.row).row
  col_max = max(positions, key=lambda p: p.col).col

  row_min = min(positions, key=lambda p: p.row).row
  col_min = min(positions, key=lambda p: p.col).col

  for r in range(row_min, row_max + 1):
    for c in range(col_min, col_max + 1):
      if Position(row = r, col = c) in positions:
        print('#', end ='')
      else:
        print('.', end = '')
    print('')


def parse_input(map: str) -> set[Position]:
  ret = set()
  for row, line in enumerate(map.splitlines()):
    for col, char in enumerate(line):
      if char == '#':
        ret.add(Position(row=row, col=col))
  return ret


def p1():
  input = open("input.txt", "r").read()
  positions = parse_input(input)

  for round_number in range(10):
    positions = play_round(round_number, positions)

  row_max = max(positions, key=lambda p: p.row).row
  col_max = max(positions, key=lambda p: p.col).col

  row_min = min(positions, key=lambda p: p.row).row
  col_min = min(positions, key=lambda p: p.col).col

  return sum(int(Position(row, col) not in positions) for row in range(row_min, row_max + 1) for col in range(col_min, col_max + 1))


def p2():
  input = open("input.txt", "r").read()
  old_positions = None
  positions = parse_input(input)

  round_count = 0

  while old_positions != positions:
    old_positions = positions
    positions = play_round(round_count, positions)
    round_count += 1

  return round_count


pprint(p1())
print(p2())