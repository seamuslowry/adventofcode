
priority = "?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_priority(char: str) -> int:
  return priority.index(char)

def find_match(rucksack: str) -> str:
  middle = int(len(rucksack)/2)
  left = rucksack[:middle]
  right = rucksack[middle:]
  overlap = [l for l in left if l in right]
  return overlap[0]

def p1():
  input = open("input.txt", "r")
  return sum(get_priority(find_match(l)) for l in input)

def p2():
  return 0

print(p1())
print(p2())