from pprint import pprint
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
  NORTH = 0
  SOUTH = 1
  WEST = 2
  EAST = 3

@dataclass(frozen=True, eq=True)
class Position:
  row: int
  col: int

def play_round(round_number: int, starting_positions: set[Position]) -> set[Position]:
  proposal_direction = Direction(round_number % len(Direction))

  return set()

def parse_input(map: str) -> set[Position]:
  ret = set()
  for row, line in enumerate(map.splitlines()):
    for col, char in enumerate(line):
      if char == '#':
        ret.add(Position(row=row, col=col))
  return ret


def p1():
  input = open("input.txt", "r").read()
  return parse_input(input)

def p2():
  input = open("input.txt", "r")
  return 0


pprint(p1())
print(p2())