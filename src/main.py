import sys
import importlib

def my_main():
    puzzle_num = sys.argv[1]
    module_name = f"solutions.puzzle{puzzle_num}.solution"
    try:
        solution = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Puzzle {puzzle_num} does not exist")

    with open(f"inputs/{puzzle_num}.txt", "r") as f:
        input_file = f.read()

    answers = solution.main(input_file)
    for idx, answer in enumerate(answers):
        print(f"Part {idx+1} answer: {answer}")

if __name__ == "__main__":
    my_main()