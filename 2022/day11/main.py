from dataclasses import dataclass
from functools import reduce

@dataclass
class Monkey:
  items: list[int]
  operation: str # requires variable 'old' in scope
  divisor: int
  true_index: int
  false_index: int

  def inspect(self, old: int, worry_modifier: int) -> int: # return the new worry level of the item
    return eval(self.operation) // worry_modifier

  def decide_throw(self, item: int) -> int: # return the index to throw to
    return self.true_index if (item % self.divisor == 0) else self.false_index


def process_monkey_definition(paragraph: str) -> Monkey:
  lines = paragraph.splitlines()
  items = list(map(lambda n: int(n.strip()), lines[1].split(":")[1].split(",")))
  operation = lines[2].split("=")[1].strip()
  divisor = int(lines[3].split(" ")[-1])
  true_index = int(lines[4].split(" ")[-1])
  false_index = int(lines[5].split(" ")[-1])

  return Monkey(items, operation, divisor, true_index, false_index)

def act(all_monkeys: list[Monkey], monkey: Monkey, worry_modifier: int) -> int: # return number of items inspected
  new_worries = list(map(lambda item: monkey.inspect(item, worry_modifier), monkey.items))
  all_divisor = reduce(lambda a,b: a*b, map(lambda m: m.divisor, all_monkeys))
  throws = list(map(monkey.decide_throw, new_worries))
  for index, throw in enumerate(throws):
    dest_monkey = all_monkeys[throw]
    dest_monkey.items.append(new_worries[index] % all_divisor)
  monkey.items.clear()

  return len(throws)

def round(all_monkeys: list[Monkey], worry_modifier: int) -> dict[int, int]:
  return {index: act(all_monkeys, monkey, worry_modifier) for index, monkey in enumerate(all_monkeys)}

def process(all_monkeys: list[Monkey], rounds: int, worry_modifier: int) -> dict[int,int]:
  ret = {}
  for _ in range(0, rounds):
    round_results = round(all_monkeys, worry_modifier)
    for key, value in round_results.items():
      ret[key] = ret.get(key, 0) + value
  return ret

def determine_monkey_business(aggregation: dict[int,int]) -> int:
  return reduce(lambda a,b: a*b ,sorted(aggregation.values(), reverse=True)[:2])
  

def p1():
  input = open("input.txt", "r").read().split("\n\n")
  monkeys = list(map(process_monkey_definition, input))
  aggregation = process(monkeys, 20, 3)
  return determine_monkey_business(aggregation)

def p2():
  input = open("input.txt", "r").read().split("\n\n")
  monkeys = list(map(process_monkey_definition, input))
  aggregation = process(monkeys, 10000, 1)
  return determine_monkey_business(aggregation)


print(p1())
print(p2())