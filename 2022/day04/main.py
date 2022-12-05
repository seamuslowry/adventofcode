
def range_to_set(ran: str) -> set[int]:
  start, end = ran.split("-")
  return set(range(int(start), int(end) + 1))

def line_to_sets(line:str) -> tuple[set[int], set[int]]:
  left, right = line.split(",")
  return (range_to_set(left), range_to_set(right))

def supersets(line:str) -> bool:
  left, right = line_to_sets(line)
  return left.issubset(right) or left.issuperset(right)

def overlaps(line:str) -> bool:
  left, right = line_to_sets(line)
  return bool(left.intersection(right))

def p1():
  input = open("input.txt", "r")

  return len([l for l in input if supersets(l)])

def p2():
  input = open("input.txt", "r")

  return len([l for l in input if overlaps(l)])


print(p1())
print(p2())