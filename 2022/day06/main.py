
def find_first_distinct_of_length(s: str, l: int) -> int:
  for index in range(l, len(s)):
    if len(set([*s[index-l:index]])) == l:
      return index
  return -1

def p1():
  input = open("input.txt", "r").read()
  return find_first_distinct_of_length(input, 4)

def p2():
  input = open("input.txt", "r").read()
  return find_first_distinct_of_length(input, 14)


print(p1())
print(p2())