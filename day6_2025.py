"""
Advent of Code 2025 - Day 6: Trash Compactor

Algorithms used:
- Part 1: Grid transposition + column parsing (vertical number reading)
- Part 2: Grid transposition + right-to-left reading (digit position interpretation)
- Data structures: List of strings (columns), string parsing for multi-digit numbers
"""
from aocd import get_data, submit
from aoc_utils import fetch_problem_part1, fetch_problem_part2, parse_lines

DAY = 6
YEAR = 2025


def solve_part1(data):
    """
    Solve vertical math problems (reading top-to-bottom).

    Algorithm: Transpose grid and parse column groups
    - Transpose rows into columns
    - Split by all-space columns to identify problems
    - For each problem, read rows top-to-bottom to get multi-digit numbers
    - Apply operation (+/*) and sum results

    Complexity: O(n * m) where n = rows, m = columns
    """
    lines = parse_lines(data)

    # Transpose: convert rows to columns
    max_len = max(len(line) for line in lines)
    columns = []
    for col_idx in range(max_len):
        col = []
        for line in lines:
            if col_idx < len(line):
                col.append(line[col_idx])
            else:
                col.append(' ')
        columns.append(''.join(col))

    # Split into problems (separated by all-space columns)
    problems = []
    current_problem = []

    for col in columns:
        if col.strip() == '':
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            current_problem.append(col)

    if current_problem:
        problems.append(current_problem)

    # Solve each problem
    total = 0
    for problem in problems:
        # Each problem is list of columns, need to read rows to get multi-digit numbers
        # Reconstruct the vertical problem
        problem_rows = []
        max_height = max(len(col) for col in problem)
        for row_idx in range(max_height):
            row = ''
            for col in problem:
                if row_idx < len(col):
                    row += col[row_idx]
                else:
                    row += ' '
            problem_rows.append(row.strip())

        # Parse numbers and operation
        numbers = []
        operation = None

        for row in problem_rows:
            if row in ['+', '*']:
                operation = row
            elif row:  # not empty
                numbers.append(int(row))

        # Apply operation
        if operation == '+':
            result = sum(numbers)
        else:  # '*'
            result = 1
            for num in numbers:
                result *= num

        total += result

    return total


def solve_part2(data):
    """
    Solve vertical math problems (reading right-to-left).

    Algorithm: Transpose grid and reverse column order
    - Transpose rows into columns
    - Split by all-space columns to identify problems
    - Reverse each problem (right-to-left reading)
    - Each column = one number (read top-to-bottom for digits)
    - Apply operation (+/*) and sum results

    Complexity: O(n * m) where n = rows, m = columns
    """
    lines = parse_lines(data)

    # Transpose: convert rows to columns
    max_len = max(len(line) for line in lines)
    columns = []
    for col_idx in range(max_len):
        col = []
        for line in lines:
            if col_idx < len(line):
                col.append(line[col_idx])
            else:
                col.append(' ')
        columns.append(''.join(col))

    # Split into problems (separated by all-space columns)
    problems = []
    current_problem = []

    for col in columns:
        if col.strip() == '':
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            current_problem.append(col)

    if current_problem:
        problems.append(current_problem)

    # Solve each problem
    total = 0
    for problem in problems:
        # Reverse problem to read right-to-left
        problem = problem[::-1]

        # Find operation - it's in the last row of any column
        operation = None
        for col in problem:
            for char in col:
                if char in ['+', '*']:
                    operation = char
                    break
            if operation:
                break

        if not operation:
            continue

        # Each column represents one number (read top to bottom)
        # Numbers are the columns, digits are rows
        numbers = []

        for col in problem:
            # Read this column top-to-bottom to form a number
            num_str = ''
            for char in col:
                if char.isdigit():
                    num_str += char

            if num_str:
                numbers.append(int(num_str))

        # Apply operation
        if operation == '+':
            result = sum(numbers)
        else:  # '*'
            result = 1
            for num in numbers:
                result *= num

        total += result

    return total


if __name__ == "__main__":
    # Test with example
    example = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +"""

    # Part 1 tests
    result = solve_part1(example)
    print(f"Part 1 example: {result} (expected: 4277556)")
    assert result == 4277556

    # Part 2 tests
    result2 = solve_part2(example)
    print(f"Part 2 example: {result2} (expected: 3263827)")
    assert result2 == 3263827

    # Solve actual puzzle
    data = get_data(day=DAY, year=YEAR)

    answer1 = solve_part1(data)
    print(f"\nPart 1 answer: {answer1}")
    # submit(answer1, part="a", day=DAY, year=YEAR)  # Already submitted

    answer2 = solve_part2(data)
    print(f"Part 2 answer: {answer2}")
    # submit(answer2, part="b", day=DAY, year=YEAR)  # Already submitted
