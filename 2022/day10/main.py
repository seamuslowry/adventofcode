import pprint

def noop(current_value: int, current_cycle: int) -> tuple[int, dict[int,int]]:
  return (current_value, cycles(1, current_value, current_cycle))

def addx(amount: int, current_value: int, current_cycle: int) -> tuple[int,dict[int,int]]:
  return (current_value + amount, cycles(2, current_value, current_cycle))

def cycles(num: int, current_value: int, current_cycle: int) -> dict[int,int]:
  return {cycle: current_value for cycle in range(current_cycle, current_cycle + num)}

def parse_line(line: str, current_value: int, current_cycle: int) -> tuple[int, dict[int,int]]:
  if line == "noop":
    return noop(current_value, current_cycle)
  _, value = line.split(" ")
  return addx(int(value), current_value, current_cycle)

def parse_lines(lines: list[str]) -> tuple[int, dict[int,int]]:
  current_value = 1
  cycles = {}
  for line in lines:
    current_value, new_cycles = parse_line(line, current_value, len(cycles) + 1)
    cycles = cycles | new_cycles
  return (current_value, cycles)

def sum_interesting(cycles: dict[int,int]) -> int:
  return sum(map(lambda n: cycles.get(n, 0) * n, [20, 60, 100, 140, 180, 220]))


def p1():
  input = open("input.txt", "r").read().split('\n')
  _, cycles = parse_lines(input)
  return sum_interesting(cycles)

def p2():
  input = open("input.txt", "r")
  return 0


print(p1())
print(p2())