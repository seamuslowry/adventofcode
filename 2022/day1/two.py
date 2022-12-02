
def sum_elf(cal_list: str):
  nums = map(int, cal_list.split("\n"))
  return sum(nums)


input = open("input.txt", "r").read()

elf_splits = input.split("\n\n")

totals = [sum_elf(elf_split) for elf_split in elf_splits]

totals.sort(reverse=True)

top_three_elves = totals[:3]

print(sum(top_three_elves))