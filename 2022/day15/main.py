
from dataclasses import dataclass
from typing import Optional
import time

@dataclass(order=True, eq=True, frozen=True)
class Point:
  row: int
  col: int

  def manhattan_distance(self, p2: 'Point') -> int:
    return abs(self.row - p2.row) + abs(self.col - p2.col)


@dataclass
class Connection:
  beacon: Point
  sensor: Point

  @property
  def distance(self):
    return self.beacon.manhattan_distance(self.sensor)


def parse_line(line: str) -> Connection:
  tokens = line.replace(",", "").replace(":", "").split(" ")
  sx = int(tokens[2].split("=")[1])
  sy = int(tokens[3].split("=")[1])
  bx = int(tokens[8].split("=")[1])
  by = int(tokens[9].split("=")[1])

  return Connection(Point(col = bx, row = by), Point(col = sx, row = sy))

def covering_in_row_range(connection: Connection, row: int) -> Optional[tuple[Point, Point]]:
  row_distance = abs(row - connection.sensor.row)

  remaining = connection.distance - row_distance

  if remaining > 0:
    return (Point(col = connection.sensor.col - remaining, row = row), Point(col = connection.sensor.col + remaining, row = row))
  return None

def find_uncovered_in_range(connections: list[Connection], min: int = 0, max: int = 4000000) -> Point:
  for row in range(min,max):
    intervals = intervals_covering_in_row(connections, row)
    intervals_in_range = list(filter(lambda i: i[1].col > min and i[0].col < max, intervals))
    if len(intervals_in_range) > 1:
      return Point(row=row, col=intervals_in_range[0][1].col + 1)

  return Point(-1,-1)

def intervals_covering_in_row(connections: list[Connection], row: int) -> list[tuple[Point,Point]]:
  beacons = list(set(filter(lambda b: b.row == row, (map(lambda c: c.beacon, connections)))))
  sensors = list(set(filter(lambda b: b.row == row, (map(lambda c: c.sensor, connections)))))

  intervals = list(map(lambda b: (b,b), beacons)) + list(map(lambda s: (s,s), sensors))

  for connection in connections:
    new_range = covering_in_row_range(connection, row)
    if new_range:
      intervals = merge_intervals([*intervals, new_range])
  
  return intervals


def quick_covering_in_row(connections: list[Connection], row: int) -> int:
  intervals = intervals_covering_in_row(connections, row)

  total = 0

  for i in intervals:
    total += abs(i[1].col - i[0].col)

  return total

# merge solution taken from https://www.geeksforgeeks.org/merging-intervals/
def merge_intervals(unsorted_intervals: list[tuple[Point,Point]]) -> list[tuple[Point,Point]]:
  # Sort the array on the basis of start values of intervals.
  intervals: list[tuple[Point,Point]] = sorted(unsorted_intervals, key=lambda i: i[0].col)

  stack: list[tuple[Point,Point]] = []
  # insert first interval into stack
  stack.append(intervals[0])
  for i in intervals[1:]:
    # Check for overlapping interval,
    # if interval overlap
    if stack[-1][0].col <= i[0].col <= stack[-1][-1].col + 1:
      stack[-1] = (stack[-1][0], max(stack[-1][-1], i[-1]))
    else:
      stack.append(i)

  return stack

def p1():
  input = open("input.txt", "r").read().splitlines()
  connections = list(map(lambda l: parse_line(l), input))
  return quick_covering_in_row(connections, 2000000)

def p2():
  input = open("input.txt", "r").read().splitlines()
  connections = list(map(lambda l: parse_line(l), input))
  uncovered_point = find_uncovered_in_range(connections, 0, 4000000)

  return uncovered_point.col * 4000000 + uncovered_point.row


print(p1())
print(p2())