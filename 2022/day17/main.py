
from dataclasses import dataclass
import time
from itertools import groupby
from pprint import pprint


@dataclass(frozen=True,eq=True)
class Location:
  row: int
  col: int

@dataclass(frozen=True,eq=True)
class Direction:
  dr: int
  dc: int

@dataclass
class Rock:
  spots: set[Location]

  @property
  def highest_row(self) -> int:
    return max(map(lambda s: s.row, self.spots))

  @property
  def rows(self) -> list[int]:
    return list(map(lambda s: s.row, self.spots))

  def after_move(self, direction: Direction) -> set[Location]:
    return set(map(lambda s: Location(row=s.row + direction.dr,col=s.col + direction.dc), self.spots))

# starting locations should be the bottom left most position of the rock
def create_rock(index: int, starting_location: Location) -> Rock:
  mod_index = index % 5 # five is max number of rocks
  if mod_index == 0:
    return Rock(spots={
      Location(row=starting_location.row, col=starting_location.col),
      Location(row=starting_location.row, col=starting_location.col + 1),
      Location(row=starting_location.row, col=starting_location.col + 2),
      Location(row=starting_location.row, col=starting_location.col + 3)
    })
  if mod_index == 1:
    return Rock(spots={
      Location(row=starting_location.row, col=starting_location.col + 1),
      Location(row=starting_location.row + 1, col=starting_location.col),
      Location(row=starting_location.row + 1, col=starting_location.col + 1),
      Location(row=starting_location.row + 1, col=starting_location.col + 2),
      Location(row=starting_location.row + 2, col=starting_location.col + 1)
    })
  if mod_index == 2:
    return Rock(spots={
      Location(row=starting_location.row, col=starting_location.col),
      Location(row=starting_location.row, col=starting_location.col + 1),
      Location(row=starting_location.row, col=starting_location.col + 2),
      Location(row=starting_location.row + 1, col=starting_location.col + 2),
      Location(row=starting_location.row + 2, col=starting_location.col + 2)
    })
  if mod_index == 3:
    return Rock(spots={
      Location(row=starting_location.row, col=starting_location.col),
      Location(row=starting_location.row + 1, col=starting_location.col),
      Location(row=starting_location.row + 2, col=starting_location.col),
      Location(row=starting_location.row + 3, col=starting_location.col)
    })
  else:
    return Rock(spots={
      Location(row=starting_location.row, col=starting_location.col),
      Location(row=starting_location.row , col=starting_location.col + 1),
      Location(row=starting_location.row + 1, col=starting_location.col),
      Location(row=starting_location.row + 1, col=starting_location.col + 1)
    })

def char_to_direction(c: str) -> Direction:
  if c == "<":
    return Direction(dr=0, dc=-1)
  return Direction(dr=0, dc=1)

def parse_input(line: str) -> list[Direction]:
  return [char_to_direction(c) for c in line]

def determine_starting_location(settled: list[Rock]) -> Location:
  max_row = max(map(lambda r: r.highest_row + 1, settled), default=0)
  return Location(row=max_row + 3, col=2)

def find_cycles(settled: list[Rock], max: int):
  strs: list[str] = []
  settled_spots: set[Location] = set(spot for rock in settled for spot in rock.spots)
  for row in range(max):
    tmp_str = ''
    for col in range(7):
      loc = Location(row=row,col=col)
      if loc in settled_spots:
        tmp_str += 'S'
      else:
        tmp_str += '.'
    strs.append(tmp_str)
  
  for x in range(len(strs)):
    for y in range(x + 2022, (len(strs) - x) // 2):
      sublist = strs[x:y]
      next_sublist = strs[y:2* y - x]
      if sublist == next_sublist:
        print(f'cycle found at x: {x} y: {y}')


def print_simulation(falling_rock: Rock, settled: list[Rock]) -> None:
  max_row = falling_rock.highest_row + 1
  settled_spots: set[Location] = set(spot for rock in settled for spot in rock.spots)
  falling_spots = falling_rock.spots

  for row in range(max_row, -1, -1):
    print(f"{row}".ljust(4) + "|", end="")
    for col in range(7):
      loc = Location(row,col)
      print_char = '.'
      if loc in settled_spots and loc in falling_spots:
        # this is an error
        print_char = 'X'
      elif loc in settled_spots:
        print_char = 'S'
      elif loc in falling_spots:
        print_char = 'F'
      print(print_char, end='')
    print('|')
  print("    ---------")


def simulate(count: int, directions: list[Direction]) -> int:
  relevant_settled_rocks: list[Rock] = []
  settled_count = 0
  tick = 0
  falling_rock = create_rock(tick, determine_starting_location(relevant_settled_rocks))

  while settled_count < count:
    settled_spots: set[Location] = set(spot for rock in relevant_settled_rocks for spot in rock.spots)

    jet_direction = directions[tick % len(directions)]

    # move from the jet
    after_jet_move = falling_rock.after_move(jet_direction)
    after_jet_cols = sorted(map(lambda a:a.col, after_jet_move))
    # determine if the rock can move from the jet
    if after_jet_move.isdisjoint(settled_spots) and after_jet_cols[0] >= 0 and after_jet_cols[-1] < 7:
      falling_rock.spots = after_jet_move
    
    # move down
    after_down_move = falling_rock.after_move(Direction(dr=-1, dc=0))
    after_down_rows = sorted(map(lambda a:a.row, after_down_move))
    # determine if the rock is settled
    if after_down_rows[0] < 0 or not after_down_move.isdisjoint(settled_spots):
      relevant_settled_rocks.append(falling_rock)
      settled_count += 1

      # prune now unhelpful rocks
      all_spots = settled_spots.union(falling_rock.spots)
      for row in falling_rock.rows:
        row_spots = list(spot for spot in all_spots if spot.row == row)
        if len(row_spots) == 7:
          relevant_settled_rocks = list(filter(lambda l:l.highest_row >= row - 4, relevant_settled_rocks))
          pass

      # create the next falling rock
      falling_rock = create_rock(settled_count, determine_starting_location(relevant_settled_rocks))

      # print(f'{settled_count}/{count} : {settled_count/count*100}%')


    else:
      falling_rock.spots = after_down_move
    tick += 1
  # print_simulation(falling_rock, relevant_settled_rocks)

  # print(f'{settled_count - len(relevant_settled_rocks)} pruned')

  # find_cycles(relevant_settled_rocks, determine_starting_location(relevant_settled_rocks).row)

  return determine_starting_location(relevant_settled_rocks).row - 3


def test():
  input = open("input.txt", "r").read()
  # answer = 0
  # rocks = 2008
  # while answer < 3047:
  #   rocks += 1
  #   answer =  simulate(rocks, parse_input(input))
  #   print(f'{rocks}: {answer}')

  
  parsed = parse_input(input)
  for n in range(3000, 3010):
    simulated = simulate(n, parsed)
    calculated = calculate_height(n, parsed)
    if simulated != calculated:
      print(f'n {n}, simulated {simulated}, calculated: {calculated}')
    else:
      print(f'{n}: successful calculation')
    # print(f'{n}: {simulate(n, parse_input(input))}')

def calculate_height(count: int, directions: list[Direction]) -> int:
  if count < 305:
    return simulate(count, directions)
  else:
    # these numbers were calculated on pen and paper after some work to find cycles within the stacking programatically
    # I don't know _exactly_ how to calculate them for generic input

    # process to get them was essentially
    # 1. generate string representations of each row up to several thousand rocks
    # 2. search that list of row strings for two consecutive sublists with length greater than ~1000 that are exactly equal (should be a cycle)
    # 3. with knowledge of at what height a cycle starts and ends, can figure out the rest

    height_before_cycles = 465
    rocks_before_cycles = 305
    rocks_in_cycle = 1705
    height_of_cycle = 2582

    remainder_analogous_rocks = ((count - rocks_before_cycles) % rocks_in_cycle) + rocks_before_cycles
    remainder_height = simulate(remainder_analogous_rocks, directions) - height_before_cycles

    return height_before_cycles + (height_of_cycle * ((count - rocks_before_cycles) // rocks_in_cycle)) + remainder_height


def p1():
  input = open("input.txt", "r").read()
  return calculate_height(2022, parse_input(input))

def p2():
  input = open("input.txt", "r").read()
  return calculate_height(1000000000000, parse_input(input))

print(p1())
print(p2())