
from dataclasses import dataclass, astuple

@dataclass(eq=True, frozen=True)
class Point:
  x: int
  y: int
  z: int

  # def __iter__(self):
  #   return iter(astuple(self))


def parse_input(lines: list[str]) -> set[Point]:
  vals: set[Point] = set()
  for line in lines:
    x,y,z = line.split(",")
    vals.add(Point(int(x),int(y),int(z)))
  return vals

def surface_area(points: set[Point], point: Point) -> int:
  covered = 0
  for adjacent_point in adjacent_points(point):
    covered += int(adjacent_point in points)

  return 6 - covered

def is_enclosed(points: set[Point], point: Point) -> bool: # point passed should be an empty space
  if point in points:
    return False

  current_point = point
  determine_enclosed_points: set[Point] = {current_point}
  visited: set[Point] = {current_point}

  # you know what would be a good idea: not recomputing these all the time
  # oh, well
  x_vals = list(map(lambda p: p.x, points))
  y_vals = list(map(lambda p: p.y, points))
  z_vals = list(map(lambda p: p.z, points))

  x_min = min(x_vals)
  x_max = max(x_vals)
  y_min = min(y_vals)
  y_max = max(y_vals)
  z_min = min(z_vals)
  z_max = max(z_vals)

  while determine_enclosed_points:
    current_point = determine_enclosed_points.pop()
    if current_point.x <= x_min or current_point.x >= x_max or current_point.y <= y_min or current_point.y >= y_max or current_point.z <= z_min or current_point.z >= z_max: # reached border
        return False
    for adjacent_point in adjacent_points(current_point):
      if adjacent_point not in points and adjacent_point not in visited:
        determine_enclosed_points.add(adjacent_point)
        visited.add(adjacent_point)
  return True

def adjacent_points(point: Point):
  return [
    Point(point.x - 1, point.y, point.z),
    Point(point.x + 1, point.y, point.z),
    Point(point.x, point.y - 1, point.z),
    Point(point.x, point.y + 1, point.z),
    Point(point.x, point.y, point.z - 1),
    Point(point.x, point.y, point.z + 1)]

def interior_surface_area(points: set[Point], point: Point) -> int:
  total = 0

  for test_point in adjacent_points(point):
    total += int(is_enclosed(points, test_point))

  return total

def total_surface_area(points: set[Point]) -> int:
  uncovered = 0
  for point in points:
    uncovered += surface_area(points, point)

  return uncovered

def total_interior_surface_area(points: set[Point]) -> int:
  interior = 0
  for point in points:
    interior += interior_surface_area(points, point)

  return interior

def p1():
  input = open("input.txt", "r").read().splitlines()
  return total_surface_area(parse_input(input))

def p2():
  input = open("input.txt", "r").read().splitlines()
  points = parse_input(input)
  total = total_surface_area(points)
  interior = total_interior_surface_area(points)
  return total - interior



print(p1())
print(p2())