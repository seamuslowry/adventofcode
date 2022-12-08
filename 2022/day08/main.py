
def read_input(lines: list[str]) -> list[list[int]]:
  return [list(map(int, [*line])) for line in lines]

def outer_visible(grid: list[list[int]]) -> int:
  return 2 * len(grid) + 2*len(grid[0]) - 4

def inner_visible(grid: list[list[int]]) -> int:
  total = 0
  for y in range(1, len(grid) - 1):
    for x in range(1, len(grid[0]) - 1):
      total = total + bool(any(check_inner_visible(grid, x ,y)))
  return total

def check_inner_visible(grid: list[list[int]], x: int, y: int) -> list[bool]:
  val = grid[x][y]

  top = all(grid[x][check_y] < val for check_y in range(0, y))
  bottom = all(grid[x][check_y] < val for check_y in range(y + 1, len(grid)))
  left = all(grid[check_x][y] < val for check_x in range(0, x))
  right = all(grid[check_x][y] < val for check_x in range(x + 1, len(grid[0])))
  return [top, bottom, left, right]

def inner_visiblity(grid: list[list[int]]) -> int:
  most = 0
  for y in range(1, len(grid) - 1):
    for x in range(1, len(grid[0]) - 1):
      most = max(most, check_inner_visiblity(grid, x ,y))
  return most

def check_inner_visiblity(grid: list[list[int]], row: int, col: int) -> int:
  val = grid[row][col]

  left = min((col - check_col for check_col in range(0, col) if grid[row][check_col] >= val), default=col)
  right = min((check_col - col for check_col in range(col + 1, len(grid[row])) if grid[row][check_col] >= val), default=len(grid[row]) - col - 1)
  top = min((row - check_row for check_row in range(0, row) if grid[check_row][col] >= val), default=row)
  bottom = min((check_row - row for check_row in range(row + 1, len(grid)) if grid[check_row][col] >= val), default=len(grid) - row - 1)
  mult = top * bottom * left * right

  print(f'row: {row}, col: {col}, val: {val} top: {top}, bottom: {bottom}, left: {left}, right: {right}, mult: {mult}')

  return mult

def p1():
  input = open("input.txt", "r").read().split("\n")
  grid = read_input(input)
  return outer_visible(grid) + inner_visible(grid)

def p2():
  input = open("input.txt", "r").read().split("\n")
  grid = read_input(input)
  return inner_visiblity(grid)


print(p1())
print(p2())