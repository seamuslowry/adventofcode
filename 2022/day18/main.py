
from dataclasses import dataclass, astuple


@dataclass(eq=True, frozen=True)
class Point:
  x: int
  y: int
  z: int

  def __iter__(self):
    return iter(astuple(self))


def parse_input(lines: list[str]) -> set[Point]:
  vals: set[Point] = set()
  for line in lines:
    x,y,z = line.split(",")
    vals.add(Point(int(x),int(y),int(z)))
  return vals

def uncovered_sides(points: set[Point], point: Point):
  covered = 0
  for mod in [-1,1]:
    covered += int(Point(point.x + mod, point.y, point.z) in points)
    covered += int(Point(point.x, point.y + mod, point.z) in points)
    covered += int(Point(point.x, point.y, point.z + mod) in points)

  return 6 - covered

def total_uncovered_sides(points: set[Point]):
  uncovered = 0
  for point in points:
    uncovered += uncovered_sides(points, point)

  return uncovered

def p1():
  input = open("input.txt", "r").read().splitlines()
  return total_uncovered_sides(parse_input(input))

def p2():
  input = open("input.txt", "r")
  return 0


print(p1())
print(p2())