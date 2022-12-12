from dataclasses import dataclass, field
from typing import Callable, Optional

heights = "abcdefghijklmnopqrstuvwxyz"

START = 'S'
END = 'E'

HEIGHTS_BY_POINT = {
  START: 0,
  END: 25
}

@dataclass
class Node:
  value: int = field(compare=False)
  row: int
  col: int
  char: str = field(compare=False)
  edges: list['Node'] = field(compare=False)

# solution taken from https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
def dijkstra_algorithm(all_nodes: list[Node], start_node: Node):
  unvisited_nodes = list(all_nodes)
  # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
  shortest_path: dict[tuple[int,int], int] = {}
  # We'll use this dict to save the shortest known path to a node found so far
  previous_nodes: dict[tuple[int,int], Node] = {}

  # We'll use 1000 to initialize the "infinity" value of the unvisited nodes   
  max_value = 1000
  for node in unvisited_nodes:
      shortest_path[(node.row,node.col)] = max_value
  # However, we initialize the starting node's value with 0   
  shortest_path[(start_node.row, start_node.col)] = 0

  # The algorithm executes until we visit all nodes
  while unvisited_nodes:
    # The code block below finds the node with the lowest score
    current_min_node = min(unvisited_nodes, key=lambda n: shortest_path[(n.row, n.col)])

    # The code block below retrieves the current node's neighbors and updates their distances
    neighbors = current_min_node.edges
    for neighbor in neighbors:
        tentative_value = shortest_path[(current_min_node.row, current_min_node.col)] + 1
        if tentative_value < shortest_path[(neighbor.row, neighbor.col)]:
          shortest_path[(neighbor.row, neighbor.col)] = tentative_value
          # We also update the best path to the current node
          previous_nodes[(neighbor.row, neighbor.col)] = current_min_node

    # After visiting its neighbors, we mark the node as "visited"
    unvisited_nodes.remove(current_min_node)
    
  return previous_nodes, shortest_path

def find_node(nodes: list[Node], row: int, col: int) -> Node:
  node = find_optional_node(nodes, row, col)
  if not node:
    raise RuntimeError("node must exist here")
  return node

def find_optional_node(nodes: list[Node], row: int, col: int) -> Optional[Node]:
  return next((n for n in nodes if n.row == row and n.col == col), None)


def parse_input(input: str, filter: Callable[[Node,Node], bool]) -> list[Node]:
  nodes: list[Node] = []

  chars = [[*line] for line in input.splitlines()]

  for row in range(len(chars)):
    for col in range(len(chars[row])):
      char = chars[row][col]
      height_by_point = HEIGHTS_BY_POINT.get(char, -1)
      height = height_by_point if height_by_point >= 0 else heights.index(char)
      nodes.append(Node(height, row, col, char, []))

  for row in range(len(chars)):
    for col in range(len(chars[row])):
      node = find_node(nodes, row, col)

      #N
      n_node = find_optional_node(nodes, row-1, col)
      #E
      e_node = find_optional_node(nodes, row, col+1)
      #S
      s_node = find_optional_node(nodes, row+1, col)
      #W
      w_node = find_optional_node(nodes, row, col-1)

      neighbors = [
        n_node,
        e_node,
        s_node,
        w_node
      ]

      node.edges = [n for n in neighbors if n is not None and filter(node, n)]

  return nodes

def p1():
  input = open("input.txt", "r").read()
  nodes = parse_input(input, lambda node, neigbor: neigbor.value - node.value <= 1)
  end_node = [n for n in nodes if n.char == END][0]
  start_node = [n for n in nodes if n.char == START][0]
  _, shortest = dijkstra_algorithm(nodes, start_node)
  return shortest[(end_node.row, end_node.col)]

def p2():
  input = open("input.txt", "r").read()
  nodes = parse_input(input, lambda node, neigbor: node.value - neigbor.value <= 1)
  possible_ends = list(filter(lambda n: n.value == 0,nodes))
  start_node = [n for n in nodes if n.char == END][0]
  _, shortest = dijkstra_algorithm(nodes, start_node)

  return min(map(lambda n: shortest[(n.row, n.col)], possible_ends))


print(p1())
print(p2())