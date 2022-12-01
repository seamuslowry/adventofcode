
def sum_elf(cal_list: str):
  nums = map(int, cal_list.split("\n"))
  return sum(nums)


input = open("input.txt", "r").read()

elf_splits = input.split("\n\n")

totals = [sum_elf(elf_split) for elf_split in elf_splits]

max_elf = max(totals)
max_elf_index = totals.index(max_elf)

print((max_elf_index, max_elf))