from dataclasses import dataclass
from itertools import product

@dataclass
class Valve:
  identifier: str
  release: int
  tunnels: list[tuple[str,int]]    



known_solutions: dict[tuple[str, str, str, int], int] = {}

def valves_to_str(o: set[str]) -> str:
  return "".join(sorted(o))

def depth_limited_search(valves: dict[str, Valve], opened: set[str], current: str, time_remaining: int, responsibilities: set[str]) -> int:
  existing_solution = known_solutions.get((current, valves_to_str(opened), valves_to_str(responsibilities), time_remaining), None)
  if (not responsibilities):
    return 0
  if (existing_solution):
    return existing_solution
  if (time_remaining <= 0):
    return 0


  valve = valves[current]

  released = sum(map(lambda o: valves[o].release, opened))

  if (responsibilities == opened):
    return released*time_remaining

  child_open_total = 0

  if current not in opened and current in responsibilities:
    child_open_total = depth_limited_search(valves, opened.union({current}), current, time_remaining - 1, responsibilities)

  child_leave_total = 0

  for identifier, weight in valve.tunnels:
    if time_remaining - weight <= 0:
      child_leave_total = max((time_remaining - 1) * released, child_leave_total)
    else:
      child_leave_total = max(released * (weight - 1) + depth_limited_search(valves, opened, identifier, time_remaining - weight, responsibilities), child_leave_total)

  child_val = max(child_open_total, child_leave_total)
  ret = released + child_val
  known_solutions[(current, valves_to_str(opened), valves_to_str(responsibilities), time_remaining)] = ret
  return ret

def parse_line(l: str) -> Valve:
  valves = l.replace("valve ","valves ").split(" valves ")[1].replace(" ", "")
  tokens = l.replace(",", "").replace(";","").split(" ")
  connections = list(map(lambda c: (c, 1), valves.split(",")))

  return Valve(tokens[1], int(tokens[4].split("=")[1]), connections)

def get_no_flow_nodes(nodes: list[Valve], start_node: str) -> list[Valve]:
  return list(filter(lambda n: n.release == 0 and n.identifier != start_node, nodes))

def parse_input(lines: list[str], start_node: str) -> dict[str,Valve]:
  all_nodes: list[Valve] = []
  for line in lines:
    all_nodes.append(parse_line(line))

  while len(get_no_flow_nodes(all_nodes, start_node)):
    no_flow_node = get_no_flow_nodes(all_nodes, start_node)[0]
    for node in all_nodes:
      if node == no_flow_node:
        continue
      node_connections = list(map(lambda n: n[0], node.tunnels))
      if no_flow_node.identifier in node_connections:
        current_connection = next(n for n in node.tunnels if n[0] == no_flow_node.identifier)
        node.tunnels.remove(current_connection)
        node.tunnels.extend(list(map(lambda t: (t[0], t[1] + current_connection[1]), filter(lambda t: t[0] != node.identifier ,no_flow_node.tunnels))))
    all_nodes.remove(no_flow_node)

  return {node.identifier:node for node in all_nodes}

def p1():
  start_node = "AA"
  input = open("input.txt", "r").read().splitlines()
  valves = parse_input(input, start_node)
  return depth_limited_search(valves, set(), start_node, 30, set(valves.keys()))

# this solution is slow as HELL (1hr+), but it does eventually reach the right answer
def p2():
  start_node = "AA"
  input = open("input.txt", "r").read().splitlines()
  valves = parse_input(input, start_node)

  responsibilities: list[tuple[set[str],set[str]]] = []

  valve_keys = list(filter(lambda k: valves[k].release ,valves.keys()))

  for pattern in product([True,False],repeat=len(valve_keys)):
    responsibilities.append((set(x[1] for x in zip(pattern,valve_keys) if x[0]),set(x[1] for x in zip(pattern,valve_keys) if not x[0])))

  maximum = 0

  total_resps = len(responsibilities)

  for index, grouping in enumerate(responsibilities):
    my_responsibilities, elephant_responsibilities = grouping
    print(f'{index} / {total_resps}: {index / total_resps * 100}%')
    known_solutions.clear()
    my_best = depth_limited_search(valves, set(), start_node, 26, my_responsibilities)
    elephant_best = depth_limited_search(valves, set(), start_node, 26, elephant_responsibilities)
    maximum = max(maximum, my_best + elephant_best)

  return maximum

print(p1())
print(p2())