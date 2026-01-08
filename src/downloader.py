import requests
import sys

cookie = sys.argv[1]
cj = {"session": cookie}

year=2023
num_puzzles=25
for day in range(1, num_puzzles+1):
    req = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cj)
    with open(f"../inputs/{day}.txt", "w") as f:
        f.write(req.text)