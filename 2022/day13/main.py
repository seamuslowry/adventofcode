from functools import cmp_to_key
PacketPart = int | list['PacketPart']

def lists_sorted(outer_left: list[PacketPart], outer_right: list[PacketPart]) -> int:
  len_left = len(outer_left)
  len_right = len(outer_right)

  for index in range(0, min(len_left, len_right)):
    ret = compare(outer_left[index], outer_right[index])
    if ret:
      return ret
  return len_left - len_right

def compare(left: PacketPart, right: PacketPart) -> int:
  left_int = isinstance(left, int)
  right_int = isinstance(right, int)
  ret = 0

  if left_int and right_int:
    ret = left - right
  if not ret and not left_int and not right_int:
    ret = lists_sorted(left, right)
  if not ret and not left_int and right_int:
    ret = lists_sorted(left, [right])
  if not ret and left_int and not right_int:
    ret = lists_sorted([left], right)
  return ret

def parse_packets(packets: list[str]) -> list[tuple[PacketPart, PacketPart]]:
  return [(eval(split[0].strip()), eval(split[1].strip())) for split in map(lambda p: p.split("\n"), packets)]

def p1():
  input = open("input.txt", "r").read().split('\n\n')
  packets = parse_packets(input)
  comparisons = list(map(lambda packet: compare(packet[0], packet[1]), packets))
  booleans = list(map(lambda c: c<=0, comparisons))
  return sum([(index + 1) for index, value in filter(lambda a:a[1], enumerate(booleans))])

def p2():
  input = open("input.txt", "r").read().split('\n\n')
  packets = parse_packets(input)
  DECODER_ONE: PacketPart = [[2]]
  DECODER_TWO: PacketPart = [[6]]
  packets_needing_sort = list(sum(packets, ())) + [DECODER_ONE,DECODER_TWO]
  sorted_packets = sorted(packets_needing_sort, key=cmp_to_key(compare))
  first_index = sorted_packets.index(DECODER_ONE) + 1
  second_index = sorted_packets.index(DECODER_TWO) + 1
  return first_index * second_index


print(p1())
print(p2())