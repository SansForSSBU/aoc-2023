import pytest
import importlib
import json

def test_solutions():
    with open("tests/my_inputs/answers.txt", "r") as f:
        answers = json.load(f)
    for puzzle_num in range(1, len(answers)+1):
        module_name = f"solutions.puzzle{puzzle_num}.solution"
        solution = importlib.import_module(module_name)
        input_path = f"tests/my_inputs/{puzzle_num}.txt"
        with open(input_path, "r") as f:
            input_text = f.read()
        answer = solution.main(input_text)
        assert answer == tuple(answers[str(puzzle_num)])