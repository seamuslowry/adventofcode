
priority = "?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_priority(char: str) -> int:
  return priority.index(char)

def find_match(rucksack: str) -> str:
  middle = int(len(rucksack)/2)
  left = rucksack[:middle]
  right = rucksack[middle:]
  overlap = [l for l in left if l in right]
  return overlap[0]

def find_badge(rucksacks: list[str]) -> str:
  overlap = [l for l in rucksacks[0] if l in rucksacks[1] and l in rucksacks[2]]
  return overlap[0]

def p1():
  input = open("input.txt", "r")
  return sum(get_priority(find_match(l)) for l in input)

def p2():
  input = open("input.txt", "r").read()
  sacks = input.split("\n")
  badges = []
  for index in range(0, len(sacks), 3):
    badges.append((find_badge(l[index:index+3])) for l in input)
  return sum(badges)

print(p1())
print(p2())