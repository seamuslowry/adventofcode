
def sum_elf(cal_list: str):
  nums = map(int, cal_list.split("\n"))
  return sum(nums)

def totals() -> list[int]:
  input = open("input.txt", "r").read()
  elf_splits = input.split("\n\n")

  totals = [sum_elf(elf_split) for elf_split in elf_splits]
  totals.sort(reverse=True)
  return totals

def p1():
  return totals()[0]

def p2():
  return sum(totals()[:3])


print(p1())
print(p2())