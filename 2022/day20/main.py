from typing import Optional

def decrypt(original_list: list[tuple[int,int]], current_decryption: Optional[list[tuple[int,int]]] = None) -> list[tuple[int,int]]:
  new_list = [*(current_decryption or original_list)]
  length = len(original_list)

  for index, number in original_list:
    current_index = new_list.index((index,number))

    diff = number % (length - 1)

    naive_next_index = current_index + diff
    # each time you move past an end of the list, you need to adjust
    naive_next_index = naive_next_index + (naive_next_index // length)
    next_index = naive_next_index % length
    new_list.insert(next_index, new_list.pop(current_index))

  return new_list


def parse_input(input: str) -> list[int]:
  return list(map(int, input.splitlines()))

def p1():
  input = open("input.txt", "r").read()
  numbers = parse_input(input)
  decrypted = list(map(lambda t: t[1], decrypt(list(enumerate(numbers)))))
  zero_index = decrypted.index(0)
  return sum([decrypted[(zero_index + x * 1000) % len(decrypted)] for x in [1,2,3]])

def p2():
  input = open("input.txt", "r").read()
  decryption_key = 811589153
  unmodified_numbers = parse_input(input)
  numbers = list(map(lambda n: n*decryption_key, unmodified_numbers))
  decrypted_tuples = []
  for _ in range(10):
    decrypted_tuples = decrypt(list(enumerate(numbers)), decrypted_tuples)
  decrypted = list(map(lambda t: t[1], decrypted_tuples))
  zero_index = decrypted.index(0)
  return sum([decrypted[(zero_index + x * 1000) % len(decrypted)] for x in [1,2,3]])


print(p1())
print(p2())