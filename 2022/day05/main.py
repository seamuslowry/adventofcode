def parse_crates(s: str) -> dict[str, list[str]]:
  lines = s.split('\n')
  lines.reverse()
  ret = {}
  for l in lines[1:]:
    for index in range(0, len(l), 4):
        s_index = str(int(index/4) + 1)
        c = l[index:index+3]
        if not c.isspace():
          ret[s_index] = ret.get(s_index, []) + [c]      
  return ret

def parse_moves(s: str) -> list[tuple[int,str,str]]:
  lines = s.split('\n')
  ret = []
  for l in lines:
    bits = l.split(" ")
    ret.append((int(bits[1]), bits[3], bits[-1]))
  return ret

def enact_moves_p1(crates: dict[str, list[str]], moves: list[tuple[int,str,str]]):
  for move in moves:
    amount, src, dest = move
    for c in reversed(crates[src][-amount:]):
      crates[dest].append(c)
    crates[src] = crates[src][:-amount]

def enact_moves_p2(crates: dict[str, list[str]], moves: list[tuple[int,str,str]]):
  for move in moves:
    amount, src, dest = move
    crates[dest].extend(crates[src][-amount:])
    crates[src] = crates[src][:-amount]

def p1():
  input = open("input.txt", "r").read()
  crates, moves = input.split('\n\n')

  crate_dict = parse_crates(crates)
  move_list = parse_moves(moves)

  enact_moves_p1(crate_dict, move_list)

  lasts = list(map(lambda l: l[-1], crate_dict.values()))

  return "".join(lasts).replace("[","").replace("]","")

def p2():
  input = open("input.txt", "r").read()
  crates, moves = input.split('\n\n')

  crate_dict = parse_crates(crates)
  move_list = parse_moves(moves)

  enact_moves_p2(crate_dict, move_list)

  lasts = list(map(lambda l: l[-1], crate_dict.values()))

  return "".join(lasts).replace("[","").replace("]","")


print(p1())
print(p2())