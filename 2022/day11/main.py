
from dataclasses import dataclass
from functools import reduce
from typing import Callable
from pprint import pprint

@dataclass
class Monkey:
  items: list[int]
  operation: str # requires variables 'new' and 'old' in scope
  test: Callable[[int], int] # given items worry level, return the index of the monkey to throw to

  def inspect(self, old: int) -> int: # return the new worry level of the item
    return eval(self.operation) // 3

  def decide_throw(self, item: int) -> int: # return the index to throw to
    return self.test(item)


def process_monkey_definition(paragraph: str) -> Monkey:
  lines = paragraph.splitlines()
  items = list(map(lambda n: int(n.strip()), lines[1].split(":")[1].split(",")))
  operation = lines[2].split("=")[1].strip()
  divisor = int(lines[3].split(" ")[-1])
  true_index = int(lines[4].split(" ")[-1])
  false_index = int(lines[5].split(" ")[-1])

  return Monkey(items, operation, lambda worry: true_index if (worry % divisor == 0) else false_index)

def act(all_monkeys: list[Monkey], monkey: Monkey) -> int: # return number of items inspected
  new_worries = list(map(monkey.inspect, monkey.items))
  throws = list(map(monkey.decide_throw, new_worries))
  for index, throw in enumerate(throws):
    all_monkeys[throw].items.append(new_worries[index])
  monkey.items.clear()

  return len(throws)

def round(all_monkeys: list[Monkey]) -> dict[int, int]:
  return {index: act(all_monkeys, monkey) for index, monkey in enumerate(all_monkeys)}

def process(all_monkeys: list[Monkey]) -> dict[int,int]:
  ret = {}
  for _ in range(0,20):
    round_results = round(all_monkeys)
    for key, value in round_results.items():
      ret[key] = ret.get(key, 0) + value
  return ret

def determine_monkey_business(aggregation: dict[int,int]) -> int:
  return reduce(lambda a,b: a*b ,sorted(aggregation.values(), reverse=True)[:2])
  

def p1():
  input = open("input.txt", "r").read().split("\n\n")
  monkeys = list(map(process_monkey_definition, input))
  aggregation = process(monkeys)
  return determine_monkey_business(aggregation)

def p2():
  input = open("input.txt", "r")
  return 0


pprint(p1())
print(p2())