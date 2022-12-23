
from dataclasses import dataclass
import sys
from typing import Union
from copy import deepcopy

@dataclass
class Dependency:
  left: str
  right: str
  operator: str

def parse_line(line: str) -> tuple[str, Union[int, Dependency]]:
  splits = line.split(" ")
  id = splits[0].strip(":")

  if len(splits) == 2:
    return id, int(splits[-1])
  return id, Dependency(splits[1], splits[3], splits[2])

def parse_input(lines: list[str]) -> tuple[dict[str, int], dict[str, Dependency]]:
  known_monkeys: dict[str,int] = {}
  unknown_monkeys: dict[str,Dependency] = {}

  for line in lines:
    id, value = parse_line(line)
    if isinstance(value, Dependency):
      unknown_monkeys[id] = value
    else:
      known_monkeys[id] = value

  return (known_monkeys, unknown_monkeys)

def evaluate(known: dict[str,int], unknown: dict[str, Dependency], key: str = 'root') -> int:
  current_known = deepcopy(known)
  current_unknown = deepcopy(unknown)

  while key in current_unknown:
    initial_unknown = deepcopy(current_unknown)
    for unknown_key, dependency in initial_unknown.items():
      l = current_known.get(dependency.left, None)
      r = current_known.get(dependency.right, None)
      if l is not None and r is not None:
        new_value = eval(f'{l} {dependency.operator} {r}')
        current_known[unknown_key] = new_value
        del current_unknown[unknown_key]

  return current_known.get(key, 0)

def p1():
  input = open("input.txt", "r").read().splitlines()
  known, unknown = parse_input(input)

  return int(evaluate(known, unknown))

def p2():
  input = open("input.txt", "r").read().splitlines()
  known, unknown = parse_input(input)
  root_dependency = unknown['root']
  difference = 1
  max_number = sys.maxsize // 2
  min_number = -sys.maxsize // 2 - 1
  current_number = 1

  # get an idea of how changing humn affects the relationship between left and right
  known['humn'] = 1
  d1 = evaluate(known, unknown, root_dependency.right) - evaluate(known, unknown, root_dependency.left)
  known['humn'] = 2
  d2 = evaluate(known, unknown, root_dependency.right) - evaluate(known, unknown, root_dependency.left)

  less = lambda r: r < 0
  more = lambda r: r > 0

  # assign the correct operators to binary search for the humn value based on how humn affects the result
  check_one, check_two = (less,more) if d1 < d2 else (more,less)


  while difference != 0:
    known['humn'] = current_number
    r_left = evaluate(known, unknown, root_dependency.left)
    r_right = evaluate(known, unknown, root_dependency.right)
    difference = r_right - r_left

    if check_one(difference):
      min_number = current_number
    if check_two(difference):
      max_number = current_number

    current_number = min_number + (max_number - min_number) // 2

  return current_number


print(p1())
print(p2())