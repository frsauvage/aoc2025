"""
Advent of Code 2025 - Day 6: Trash Compactor (numpy version)

Comparison with vanilla Python version
"""
from aocd import get_data
import numpy as np
from aoc_utils import parse_lines


DAY = 6
YEAR = 2025


def solve_part1_numpy(data):
    """Version avec numpy - utilise np.char pour les strings."""
    lines = parse_lines(data)

    # Pad lines to same length
    max_len = max(len(line) for line in lines)
    lines_padded = [line.ljust(max_len) for line in lines]

    # Create char array and transpose
    grid = np.array([list(line) for line in lines_padded])
    transposed = grid.T  # Simple transpose!

    # Convert back to column strings
    columns = [''.join(col) for col in transposed]

    # Split into problems (same as before)
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

    # Solve each problem (same as before)
    total = 0
    for problem in problems:
        problem_rows = []
        max_height = max(len(col) for col in problem)
        for row_idx in range(max_height):
            row = ''.join(col[row_idx] if row_idx < len(col) else ' ' for col in problem)
            problem_rows.append(row.strip())

        numbers = []
        operation = None

        for row in problem_rows:
            if row in ['+', '*']:
                operation = row
            elif row:
                numbers.append(int(row))

        if operation == '+':
            result = sum(numbers)
        else:
            result = 1
            for num in numbers:
                result *= num

        total += result

    return total


def solve_part1_vanilla(data):
    """Version vanilla Python sans numpy."""
    lines = parse_lines(data)

    # Transpose: convert rows to columns
    max_len = max(len(line) for line in lines)
    columns = []
    for col_idx in range(max_len):
        col = ''.join(line[col_idx] if col_idx < len(line) else ' ' for line in lines)
        columns.append(col)

    # Split into problems
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
        problem_rows = []
        max_height = max(len(col) for col in problem)
        for row_idx in range(max_height):
            row = ''.join(col[row_idx] if row_idx < len(col) else ' ' for col in problem)
            problem_rows.append(row.strip())

        numbers = []
        operation = None

        for row in problem_rows:
            if row in ['+', '*']:
                operation = row
            elif row:
                numbers.append(int(row))

        if operation == '+':
            result = sum(numbers)
        else:
            result = 1
            for num in numbers:
                result *= num

        total += result

    return total


if __name__ == "__main__":
    example = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +"""

    # Compare both versions
    result_numpy = solve_part1_numpy(example)
    result_vanilla = solve_part1_vanilla(example)

    print(f"Numpy version:   {result_numpy}")
    print(f"Vanilla version: {result_vanilla}")
    print(f"Match: {result_numpy == result_vanilla}")

    # Benchmark on real data
    import time

    data = get_data(day=DAY, year=YEAR)

    start = time.time()
    for _ in range(100):
        solve_part1_numpy(data)
    time_numpy = time.time() - start

    start = time.time()
    for _ in range(100):
        solve_part1_vanilla(data)
    time_vanilla = time.time() - start

    print(f"\nBenchmark (100 runs):")
    print(f"Numpy:   {time_numpy:.4f}s")
    print(f"Vanilla: {time_vanilla:.4f}s")
    print(f"Speedup: {time_vanilla/time_numpy:.2f}x")
