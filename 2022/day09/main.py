
from itertools import repeat


def translate(point: tuple[int,int], difference: tuple[int,int]) -> tuple[int,int]:
  return (point[0] + difference[0], point[1] + difference[1])

def movement(head: tuple[int,int], tail: tuple[int,int]) -> tuple[int,int]:
  vert = head[1] - tail[1]
  hor = head[0] - tail[0]
  vert_abs = abs(vert)
  hor_abs = abs(hor)
  abs_total = vert_abs + hor_abs
  vert_move = int(vert / vert_abs) if vert_abs > 1 or abs_total > 2 else 0
  hor_move = int(hor / hor_abs) if hor_abs > 1 or abs_total > 2 else 0

  return (hor_move, vert_move)

def line_to_differences(line: str) -> list[tuple[int,int]]:
  direction, number_str = line.split(" ")
  number = int(number_str)
  difference = (0, 0)
  if direction == "R":
    difference = (1, 0)
  if direction == "L":
    difference = (-1, 0)
  if direction == "D":
    difference = (0, -1)
  if direction == "U":
    difference = (0, 1)
  return list(repeat(difference, number))

def process_pair(difference: tuple[int,int], head: tuple[int,int], tail:tuple[int,int]) -> tuple[tuple[int,int], tuple[int,int]]:
    new_head = translate(head, difference)
    tail_movement = movement(new_head, tail)
    new_tail = translate(tail, tail_movement)

    return new_head, new_tail

def process_line(line: str, knots: list[tuple[int,int]]) -> tuple[set[tuple[int,int]], list[tuple[int,int]]]:
  differences = line_to_differences(line)

  tail_spots = set()

  for difference in differences:
    current_difference = difference
    for index in range(len(knots) - 1):
      knots[index], knots[index + 1] = process_pair(current_difference, knots[index], knots[index + 1])
      current_difference = movement(knots[index], knots[index + 1])

    tail_spots.add(knots[-1])

  return (tail_spots, knots)

def process_lines(lines: list[str], size: int) -> set[tuple[int,int]]:
  knots = list(repeat((0,0), size))
  tail_spots = set()

  for line in lines:
    new_tail_spots, knots = process_line(line, knots)
    tail_spots = tail_spots.union(new_tail_spots)

  return tail_spots


def p1():
  input = open("input.txt", "r").read().split('\n')

  tail_spots = process_lines(input, 2).union({(0,0)})
  return len(tail_spots)

def p2():
  input = open("input.txt", "r").read().split('\n')

  tail_spots = process_lines(input, 10).union({(0,0)})
  return len(tail_spots)


print(p1())
print(p2())