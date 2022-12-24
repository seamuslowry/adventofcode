from dataclasses import dataclass, field
from enum import Enum, IntEnum
import re
from typing import Optional


@dataclass
class Movement:
  dr: int
  dc: int

class Direction(IntEnum):
  RIGHT = 0
  DOWN = 1
  LEFT = 2
  UP = 3

MOVEMENTS = {
  Direction.UP: Movement(dr = -1, dc=0),
  Direction.DOWN: Movement(dr = 1, dc=0),
  Direction.LEFT: Movement(dr = 0, dc=-1),
  Direction.RIGHT: Movement(dr = 0, dc=1)
}

@dataclass(eq=True,frozen=True)
class EdgePoint:
  row: int
  col: int

@dataclass(eq=True,frozen=True)
class Position:
  row: int
  col: int
  direction: Direction

class TileType(Enum):
  VOID = 0
  ROCK = 1
  OPEN = 2

class Instruction:
  pass

@dataclass
class Move(Instruction):
  value: int

@dataclass
class TileMeta:
  min: int
  max: int

@dataclass
class Turn(Instruction):
  direction: int

@dataclass
class FlatMap:
  tiles: list[list[TileType]]
  position: Position
  jump_map: Optional[dict[Position, Position]] = None
  row_meta: dict[int, TileMeta] = field(init=False)
  col_meta: dict[int, TileMeta] = field(init=False)

  def __post_init__(self):
    self.row_meta = {}
    self.col_meta = {}
    for index, row in enumerate(self.tiles):
      non_void_indices = [i for i in range(len(row)) if row[i] != TileType.VOID]
      min_row = non_void_indices[0]
      max_row = non_void_indices[-1]
      self.row_meta[index] = TileMeta(min=min_row, max=max_row)

    for index, col in enumerate(zip(*self.tiles)): 
      non_void_indices = [i for i in range(len(col)) if col[i] != TileType.VOID]
      min_col = non_void_indices[0]
      max_col = non_void_indices[-1]
      self.col_meta[index] = TileMeta(min=min_col, max=max_col)


  def process_instruction(self, i: Instruction) -> None:
    if isinstance(i, Turn):
      self.process_turn(i)
    elif isinstance(i, Move):
      self.process_move(i)

  def process_turn(self, t: Turn) -> None:
    self.position = Position(row=self.position.row, col=self.position.col, direction=Direction((self.position.direction.value + t.direction) % len(Direction)))

  def facing(self) -> Position:
    # if there's a jump from the cube, take it
    jump_value = self.jump_map.get(self.position, None) if self.jump_map else None
    if jump_value:
      return jump_value

    # otherwise wrap like we're flat
    movement = MOVEMENTS[self.position.direction]

    row_meta = self.row_meta[self.position.row]
    col_meta = self.col_meta[self.position.col]


    next_row = self.position.row + movement.dr
    next_col = self.position.col + movement.dc

    if next_row > col_meta.max:
      next_row = col_meta.min
    if next_row < col_meta.min:
      next_row = col_meta.max

    if next_col > row_meta.max:
      next_col = row_meta.min
    if next_col < row_meta.min:
      next_col = row_meta.max

    return Position(next_row, next_col,self.position.direction)

  def process_move(self, m: Move) -> None:
    for _ in range(m.value):
      p = self.facing()
      try:
        tile = self.tiles[p.row][p.col]
        if tile != TileType.ROCK:
          self.position = p
      except:
        pass

def parse_flat_map(lines: list[str]) -> list[list[TileType]]:
  ret = []
  col_length = max(len(l) for l in lines)

  for line in lines:
    current_line = []
    for col in range(col_length):
      c = line[col] if col < len(line) else ' '
      if c == '#':
        current_line.append(TileType.ROCK)
      elif c == '.':
        current_line.append(TileType.OPEN)
      else:
        current_line.append(TileType.VOID)
    ret.append(current_line)

  return ret

def get_face(full_map: list[list[TileType]], tile_row: int, tile_col: int, tile_size: int = 50) -> list[list[TileType]]:
  return list(map(lambda r: r[tile_col * tile_size:(tile_col + 1) * tile_size], full_map[tile_row * tile_size:(tile_row + 1) * tile_size]))

def parse_instructions(instructions: str) -> list[Instruction]:
  split = re.split('(\\d+)',instructions)[1:-1]

  ret = []

  for s in split:
    str_value = str(s)
    if str_value == 'L':
      ret.append(Turn(-1))
    if str_value == 'R':
      ret.append(Turn(1))
    if str_value.isnumeric():
      ret.append(Move(int(str_value)))

  return ret

def opposite(d: Direction) -> Direction:
  return Direction((d.value + len(Direction) // 2) % len(Direction))

def horizontal_edge(row: int, start_col: int, end_col: int) -> list[EdgePoint]:
  return list(EdgePoint(row, col) for col in range(start_col, end_col))

def vertical_edge(col: int, start_row: int, end_row: int) -> list[EdgePoint]:  
  return list(EdgePoint(row, col) for row in range(start_row, end_row))

def edge_map(edge_one: list[EdgePoint], edge_two: list[EdgePoint], directions: tuple[Direction, Direction]) -> dict[Position, Position]:
  assert len(edge_one) == len(edge_two)

  ret: dict[Position, Position] = {}

  for index in range(len(edge_one)):
    point_one = edge_one[index]
    point_two = edge_two[index]
    ret[Position(row = point_one.row, col=point_one.col,direction=directions[0])] = Position(row = point_two.row, col=point_two.col,direction=directions[1])
    ret[Position(row = point_two.row, col=point_two.col,direction=opposite(directions[1]))] = Position(row = point_one.row, col=point_one.col,direction=opposite(directions[0]))


  return ret

def get_edge(row: int, col: int, direction: Direction, edge_size: int = 50) -> list[EdgePoint]:

  if direction == Direction.UP:
    return horizontal_edge(row * edge_size, col * edge_size, (col + 1) * edge_size)
  if direction == Direction.DOWN:
    return horizontal_edge((row + 1) * edge_size - 1, col * edge_size, (col + 1) * edge_size)
  if direction == Direction.LEFT:
    return vertical_edge(col * edge_size, row * edge_size, (row + 1) * edge_size)
  if direction == Direction.RIGHT:
    return vertical_edge((col + 1) * edge_size - 1, row * edge_size, (row + 1) * edge_size)
  return []

def p1():
  input = open("input.txt", "r").read()
  tiles_str, instructions_str = input.split("\n\n")
  tiles, instructions = parse_flat_map(tiles_str.splitlines()), parse_instructions(instructions_str)
  first_tile = tiles[0].index(TileType.OPEN)
  map = FlatMap(tiles, Position(row=0,col=first_tile, direction=Direction.RIGHT))

  for i in instructions:
    map.process_instruction(i)

  return 1000 * (map.position.row + 1) + 4 * (map.position.col + 1) + map.position.direction

def p2():
  input = open("input.txt", "r").read()
  tiles_str, instructions_str = input.split("\n\n")
  tiles, instructions = parse_flat_map(tiles_str.splitlines()), parse_instructions(instructions_str)
  first_tile = tiles[0].index(TileType.OPEN)

  # START NEEDS MODIFICATION BASED ON INPUT (not general)
  # END NEEDS MODIFICATION BASED ON INPUT
  edge_length = 50
  jump_map = {
    # sample rows (not all input, just all that's necessary) edge_length should be 4
    # **edge_map(get_edge(1,2,Direction.RIGHT, edge_length), list(reversed(get_edge(2, 3, Direction.UP, edge_length))), (Direction.RIGHT, Direction.DOWN)),
    # **edge_map(list(reversed(get_edge(1,0,Direction.DOWN, edge_length))), get_edge(2, 2, Direction.DOWN, edge_length), (Direction.DOWN, Direction.UP))
    # _MY_ real read input; edge length should be 50
    **edge_map(get_edge(2,0,Direction.UP, edge_length), get_edge(1, 1, Direction.LEFT, edge_length), (Direction.UP, Direction.RIGHT)),
    **edge_map(get_edge(2,0,Direction.LEFT, edge_length), list(reversed(get_edge(0, 1, Direction.LEFT, edge_length))), (Direction.LEFT, Direction.RIGHT)),
    **edge_map(get_edge(1,1,Direction.RIGHT, edge_length), get_edge(0, 2, Direction.DOWN, edge_length), (Direction.RIGHT, Direction.UP)),
    **edge_map(get_edge(2,1,Direction.RIGHT, edge_length), list(reversed(get_edge(0, 2, Direction.RIGHT, edge_length))), (Direction.RIGHT, Direction.LEFT)),
    **edge_map(get_edge(3,0,Direction.RIGHT, edge_length), get_edge(2, 1, Direction.DOWN, edge_length), (Direction.RIGHT, Direction.UP)),
    **edge_map(get_edge(3,0,Direction.LEFT, edge_length), get_edge(0, 1, Direction.UP, edge_length), (Direction.LEFT, Direction.DOWN)),
    **edge_map(get_edge(3,0,Direction.DOWN, edge_length), get_edge(0, 2, Direction.UP, edge_length), (Direction.DOWN, Direction.DOWN)),
  }

  map = FlatMap(tiles, Position(row=0,col=first_tile, direction=Direction.RIGHT), jump_map)

  for i in instructions:
    map.process_instruction(i)

  return 1000 * (map.position.row + 1) + 4 * (map.position.col + 1) + map.position.direction


print(p1())
print(p2())