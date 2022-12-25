
UNADJUSTED_SNAFU = {
  '=': -2,
  '-': -1,
  '0': 0,
  '1': 1,
  '2': 2
}

ADJUSTED_SNAFU = {
  0: '0',
  1: '1',
  2: '2',
  3: '=',
  4: '-'
}

def snafu_to_decimal(num: str) -> int:
  ret = 0
  for index, char in enumerate(reversed(num)):
    ret += UNADJUSTED_SNAFU[char] * 5**index

  return ret

def decimal_to_snafu(original_num: int) -> str:
  if original_num == 0:
    return '0'

  current_num = original_num
  ret = ""
  current_index = 0

  while current_num > 0:
    ret += ADJUSTED_SNAFU[current_num % 5]
    current_index += 1
    current_num = (current_num + 2) // 5

  return ret[::-1]

def p1():
  input = open("input.txt", "r").read().splitlines()
  dec_sum = sum(snafu_to_decimal(l) for l in input)
  return decimal_to_snafu(dec_sum)


print(p1())