
OPPONENT_ROCK = "A"
OPPONENT_PAPER = "B"
OPPONENT_SCISSORS = "C"
SELF_ROCK = "X"
SELF_PAPER = "Y"
SELF_SCISSORS = "Z"

ROUNDS_TO_RESULTS = {
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

input = open("input.txt", "r")

score = 0

for line in input:
  score += ROUNDS_TO_RESULTS[line[:3]]


print(score)