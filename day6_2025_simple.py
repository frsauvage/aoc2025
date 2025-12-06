"""
Advent of Code 2025 - Day 6: Version simplifiée avec itertools.groupby
"""
from aocd import get_data, submit
from itertools import groupby
from functools import reduce
from operator import mul
from aoc_utils import parse_lines

DAY = 6
YEAR = 2025


def transpose(lines):
    """Transpose grid into columns."""
    max_len = max(len(line) for line in lines)
    return [''.join(line[i] if i < len(line) else ' ' for line in lines)
            for i in range(max_len)]


def split_problems(columns):
    """Split columns into problems separated by spaces."""
    return [list(group) for is_space, group in groupby(columns, key=lambda c: c.strip() == '')
            if not is_space]


def parse_problem(problem_cols):
    """Parse one problem and return (numbers, operation)."""
    # Reconstruct rows
    height = max(len(col) for col in problem_cols)
    rows = [''.join(col[i] if i < len(col) else ' ' for col in problem_cols).strip()
            for i in range(height)]

    # Separate numbers from operation
    operation = next((r for r in rows if r in ['+', '*']), None)
    numbers = [int(r) for r in rows if r and r not in ['+', '*']]

    return numbers, operation


def calculate(numbers, operation):
    """Apply operation to numbers."""
    return sum(numbers) if operation == '+' else reduce(mul, numbers, 1)


def solve_part1(data):
    """Solve part 1 with functional approach."""
    columns = transpose(parse_lines(data))
    problems = split_problems(columns)
    return sum(calculate(*parse_problem(p)) for p in problems)


def solve_part2(data):
    """Solve part 2 - each column is one number (RTL reading)."""
    columns = transpose(parse_lines(data))
    problems = split_problems(columns)

    total = 0
    for problem in problems:
        # Reverse for RTL reading
        problem = problem[::-1]

        # Find operation
        operation = next((char for col in problem for char in col if char in ['+', '*']), None)

        # Each column = one number
        numbers = [int(''.join(c for c in col if c.isdigit()))
                   for col in problem if any(c.isdigit() for c in col)]

        total += calculate(numbers, operation)

    return total


if __name__ == "__main__":
    example = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +"""

    assert solve_part1(example) == 4277556
    assert solve_part2(example) == 3263827
    print("Examples passed!")

    data = get_data(day=DAY, year=YEAR)
    print(f"Part 1: {solve_part1(data)}")
    print(f"Part 2: {solve_part2(data)}")
