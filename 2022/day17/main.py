
from dataclasses import dataclass
import time


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


def p1():
  input = open("input.txt", "r").read()
  directions = parse_input(input)
  relevant_settled_rocks: list[Rock] = []
  settled_count = 0
  tick = 0
  falling_rock = create_rock(tick, determine_starting_location(relevant_settled_rocks))

  while settled_count < 2022:
  # while tick < 2:
    # print_simulation(falling_rock, settled_rocks)
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
      falling_rock = create_rock(settled_count, determine_starting_location(relevant_settled_rocks))
    else:
      falling_rock.spots = after_down_move
    tick += 1
  # print_simulation(falling_rock, relevant_settled_rocks)


  return determine_starting_location(relevant_settled_rocks).row - 3

def p2():
  input = open("input.txt", "r")
  return 0

start_time = time.time()
print(p1())
print("--- %s seconds ---" % (time.time() - start_time))
print(p2())