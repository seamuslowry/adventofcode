
from functools import reduce
from enum import Enum
import copy
import time

class Space(Enum):
  ROCK = 1
  SAND = 2

Spaces = dict[int, dict[int, Space]]

def over_abyss(spaces: Spaces, point: tuple[int,int]) -> bool:
  row, col = point
  column_dict = spaces.get(row, {})
  possible_hits = {k for k in column_dict.keys() if k > col}
  return len(possible_hits) == 0

def sand_step(spaces: Spaces, start: tuple[int,int]) -> tuple[int,int]:
  start_x, start_y = start
  down = (start_x, start_y + 1)
  dl = (start_x - 1, start_y + 1)
  dr = (start_x + 1, start_y + 1)

  for point in [down, dl, dr]:
    contents = spaces.get(point[0], {}).get(point[1], None)
    if not contents:
      return point

  return start

def add_sand(spaces: Spaces, added: tuple[int,int]) -> Spaces:
  current_spot = added
  last_spot = None
  ret = copy.deepcopy(spaces)
  while current_spot != last_spot:
    last_spot = current_spot
    current_spot = sand_step(spaces, current_spot)
    if over_abyss(spaces, current_spot):
      return spaces

  final_x, final_y = current_spot
  ret[final_x] = ret.get(final_x, {}) | {final_y: Space.SAND}

  return ret

def merge_dicts(dict_a: Spaces, dict_b: Spaces) -> dict[int,dict[int, Space]]:
  new_dict = {}
  for d in [dict_a, dict_b]:    
    for key,value in d.items():
      new_dict[key] = new_dict.get(key, {}) | value

  return new_dict

def pair_to_dict(a: tuple[int,int], b: tuple[int,int]) -> Spaces:
  ret = {}
  a_x, a_y = a
  b_x, b_y = b

  for x in range(min(a_x, b_x), max(a_x, b_x) + 1):
    for y in range(min(a_y, b_y), max(a_y, b_y) + 1):
      ret[x] = ret.get(x,{}) | { y: Space.ROCK }

  return ret

def points_to_dicts(points: list[tuple[int,int]]) -> Spaces:
  ret = {}
  for index in range(len(points) - 1):
    ret = merge_dicts(ret, pair_to_dict(points[index], points[index + 1]))
  return ret

def parse_line_points(line: str) -> list[tuple[int,int]]:
  parts = line.split(" -> ")
  return [(int(part.split(',')[0]), int(part.split(',')[1])) for part in parts]

def parse_input(lines: list[str]) -> Spaces:
  point_lines = [parse_line_points(l) for l in lines]
  point_dicts = [points_to_dicts(points) for points in point_lines]


  return reduce(lambda acc, curr: merge_dicts(acc, curr), point_dicts)

def max_cols(spaces: Spaces) -> int:
  return max([col for col_dict in spaces.values() for col in col_dict.keys()])

def min_cols(spaces: Spaces) -> int:
  return 0

def max_rows(spaces: Spaces) -> int:
  return max(spaces.keys())

def min_rows(spaces: Spaces) -> int:
  return min(spaces.keys())

def dimensions(spaces: Spaces) -> tuple[int,int,int,int]:
  return (min_rows(spaces),max_rows(spaces),min_cols(spaces),max_cols(spaces))

def print_spaces(spaces: Spaces) -> None:
  min_x, max_x, min_y, max_y = dimensions(spaces)

  for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
      content = spaces.get(x, {}).get(y, None)
      print_char = '.'
      if content == Space.ROCK:
        print_char = 'R'
      elif content == Space.SAND:
        print_char = 'S'
      print(print_char, end="")
    print('')


def p1():
  input = open("input.txt", "r").read().splitlines()
  current_spaces = parse_input(input)
  old_spaces = None

  steps = 0

  while current_spaces != old_spaces:
    old_spaces = current_spaces
    current_spaces = add_sand(current_spaces, (500,0))
    steps +=1

  return steps - 1 # the last step with no change will get counted

def p2():
  input = open("input.txt", "r").read().splitlines()
  last_spaces = None
  spaces = parse_input(input)
  min_x, max_x, _, max_y = dimensions(spaces)

  buffer = max_y

  entry_point = (500,0)

  for x in range(min_x - buffer, max_x + buffer):
    spaces[x] = spaces.get(x, {}) | {max_y + 2: Space.ROCK}

  steps = 0

  # for the real input, this takes a LONG time, but it produces the right answer in not TOO long (about 3.5 minutes for me)
  while spaces != last_spaces and not spaces.get(entry_point[0], {}).get(entry_point[1], None):
    last_spaces = spaces
    spaces = add_sand(spaces, entry_point)
    steps +=1

  return steps


print(p1())
print(p2())