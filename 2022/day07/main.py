import pprint

def walk_files(lines: list[str]) -> dict[str,int]:
  current_location = []
  ret = {}

  for line in lines:
    if line == "$ cd ..":
      current_location = current_location[:-1]
    elif line == "$ cd /":
      current_location = ["/"]
    elif line.startswith("$ cd"):
      current_location.append(line.split(" ")[2])
    elif line.startswith("$") or line.startswith("dir"):
      # do nothing for now, don't currently care about ls commands or dir results
      pass
    else:
      # should be the files
      value = int(line.split(" ")[0])
      for index in range(1, len(current_location) + 1):
        path = "/".join(current_location[:index])
        ret[path] = ret.get(path, 0) + value

  return ret

def p1():
  input = open("input.txt", "r").read()
  return sum([v for v in walk_files(input.split("\n")).values() if v < 100000])

def p2():
  input = open("input.txt", "r").read()
  dirs = walk_files(input.split("\n"))

  unused_space = 70000000 - dirs["/"]
  necessary_space = 30000000 - unused_space

  deletion_candidates = [d for d in dirs.values() if d >= necessary_space]
  deletion_candidates.sort()


  return deletion_candidates[0]


pprint.pprint(p1())
print(p2())