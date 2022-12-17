
from dataclasses import dataclass

ASSUMED_MIN_CYCLE_LENGTH = 2000 # lower this if no cycles are being found

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

def find_cycles(settled: list[Rock], max: int) -> tuple[int,int]:
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
  
  for x in range(len(strs) // 2):
    for y in range(x + ASSUMED_MIN_CYCLE_LENGTH, (len(strs) - x) // 2):
      sublist = strs[x:y]
      next_sublist = strs[y:2* y - x]
      if sublist == next_sublist:
        return (x,y)
  return (-1,-1)


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


def simulate(count: int, directions: list[Direction], remove_unnecessary: bool = True) -> tuple[dict[int,int],list[Rock]]:
  relevant_settled_rocks: list[Rock] = []
  settled_count = 0
  tick = 0
  falling_rock = create_rock(tick, determine_starting_location(relevant_settled_rocks))

  rocks_to_height: dict[int,int] = {}

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

      if remove_unnecessary:
        # prune now unhelpful rocks
        all_spots = settled_spots.union(falling_rock.spots)
        for row in falling_rock.rows:
          row_spots = list(spot for spot in all_spots if spot.row == row)
          if len(row_spots) == 7:
            relevant_settled_rocks = list(filter(lambda l:l.highest_row >= row - 4, relevant_settled_rocks))

      # create the next falling rock
      starting_location = determine_starting_location(relevant_settled_rocks)
      falling_rock = create_rock(settled_count, starting_location)
      rocks_to_height[settled_count] = starting_location.row -3
    else:
      falling_rock.spots = after_down_move
    tick += 1

  return rocks_to_height, relevant_settled_rocks

def calculate_height(count: int, directions: list[Direction]) -> int:
  # eat the performance hit every time; cry about it, I am
  cycle_max_rocks = min(count, 5000)
  big_list, settled_rocks = simulate(cycle_max_rocks, directions, False)
  cycle_max_height = max(big_list.values())
  start_cycle, end_cycle = find_cycles(settled_rocks, cycle_max_height)

  height_before_cycles = start_cycle
  height_of_cycle = end_cycle - start_cycle
  rocks_before_cycles = 0
  rocks_in_cycle = 0

  rocks_at_cycle_start = [r for r,height in big_list.items() if height == start_cycle]
  rocks_at_cycle_end = [r for r,height in big_list.items() if height == end_cycle]

  for start_rock in rocks_at_cycle_start:
    for end_rock in rocks_at_cycle_end:
      rocks_in_cycle_test = end_rock - start_rock
      start = big_list[start_rock]
      first_difference = big_list[start_rock + rocks_in_cycle_test]
      second_difference = big_list[start_rock + rocks_in_cycle_test * 2]
      if first_difference - start == second_difference - first_difference:
        rocks_before_cycles = start_rock
        rocks_in_cycle = rocks_in_cycle_test

  if count in big_list:
    return big_list[count]
  else:
    remainder_analogous_rocks = ((count - rocks_before_cycles) % rocks_in_cycle) + rocks_before_cycles
    remainder_height = max(simulate(remainder_analogous_rocks, directions)[0].values()) - height_before_cycles

    return height_before_cycles + (height_of_cycle * ((count - rocks_before_cycles) // rocks_in_cycle)) + remainder_height


def p1():
  input = open("input.txt", "r").read()
  return calculate_height(2022, parse_input(input))

def p2():
  input = open("input.txt", "r").read()
  return calculate_height(1000000000000, parse_input(input))

print(p1())
print(p2())