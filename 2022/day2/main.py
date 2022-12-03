
P1_ROUNDS_TO_RESULTS = {
  "A X": 1 + 3,
  "A Y": 2 + 6,
  "A Z": 3 + 0,
  "B X": 1 + 0,
  "B Y": 2 + 3,
  "B Z": 3 + 6,
  "C X": 1 + 6,
  "C Y": 2 + 0,
  "C Z": 3 + 3
}

P2_ROUNDS_TO_RESULTS = {
  "A X": 3 + 0,
  "A Y": 1 + 3,
  "A Z": 2 + 6,
  "B X": 1 + 0,
  "B Y": 2 + 3,
  "B Z": 3 + 6,
  "C X": 2 + 0,
  "C Y": 3 + 3,
  "C Z": 1 + 6
}

def score_input(result_map: dict[str, int]) -> int:
  input = open("input.txt", "r")
  score = 0
  for line in input:
    score += result_map[line[:3]]
  return score

def p1():
  return score_input(P1_ROUNDS_TO_RESULTS)

def p2():
  return score_input(P2_ROUNDS_TO_RESULTS)


print(p1())
print(p2())
