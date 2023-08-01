import re
from collections import namedtuple

MAX_PROBLEMS = 5
ALLOWED_OPERATORS = ["+", "-"]
Problem = namedtuple("Problem", ["operand1", "operator", "operand2"])


def arithmetic_arranger(problems, calc_prob=None):
    if len(problems) > MAX_PROBLEMS:
        return "Error: Too many problems."
    if not is_valid_operators(problems=problems):
        return "Error: Operator must be '+' or '-'."
    if not is_operand_correct(problems=problems):
        return "Error: Numbers must only contain digits."
    if not is_size_of_operand_correct(problems=problems):
        return "Error: Numbers cannot be more than four digits."
    splits = map(split_problem, problems)
    arranged_problems = [
        arrange_problem(split_problem, calc_prob) for split_problem in splits
    ]
    split_lines = [each_line_str.split("\n") for each_line_str in arranged_problems]
    arranged_problems = "\n".join("    ".join(line) for line in zip(*split_lines))

    return arranged_problems


def arrange_problem(split_problem, calc_prob):
    max_len = (
        max([len(x) for x in [split_problem.operand1, split_problem.operand2]]) + 2
    )
    operand1 = int(split_problem.operand1)
    operator = split_problem.operator
    operand2 = int(split_problem.operand2)

    if calc_prob:
        result = eval(f"{operand1} {operator} {operand2}")
        return f"{operand1:>{max_len}}\n{operator}{operand2:>{max_len-1}}\n{'-'*(max_len):<{max_len}}\n{result:>{max_len}}"
    return f"{operand1:>{max_len}}\n{operator}{operand2:>{max_len-1}}\n{'-'*(max_len):<{max_len}}"


def split_problem(problem):
    splits = re.split(r"([+|-])", problem)
    return Problem(
        operand1=splits[0].strip(),
        operator=splits[1].strip(),
        operand2=splits[2].strip(),
    )


def is_valid_operators(problems):
    return all(
        any(each_operator in each_prob for each_operator in ALLOWED_OPERATORS)
        for each_prob in problems
    )


def is_operand_correct(problems):
    pattern = re.compile("^\d+\s?[+|-]\s?\d+$")
    return all(pattern.search(each_prob) for each_prob in problems)


def is_size_of_operand_correct(problems):
    pattern = re.compile("^\d{1,4}\s?[+|-]\s?\d{1,4}$")
    return all(pattern.search(each_prob) for each_prob in problems)
