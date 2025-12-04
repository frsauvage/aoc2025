"""
Advent of Code 2025 - Day X: [Title]

Algorithms used:
- Part 1: [Algorithm name/technique]
- Part 2: [Algorithm name/technique]
- Data structures: [Key data structures used]
"""
from aocd import get_data, submit
from aoc_utils import fetch_problem_part1, fetch_problem_part2, parse_lines

DAY = X
YEAR = 2025


def solve_part1(data):
    """
    Solve part 1.

    Algorithm: [Brief description]
    - Step 1
    - Step 2

    Complexity: O(?)
    """
    lines = parse_lines(data)
    # TODO: implement logic
    return 0


def solve_part2(data):
    """
    Solve part 2.

    Algorithm: [Brief description]
    - Step 1
    - Step 2

    Complexity: O(?)
    """
    lines = parse_lines(data)
    # TODO: implement logic
    return 0


if __name__ == "__main__":
    # Fetch problem text
    print(fetch_problem_part1(YEAR, DAY))
    print("\n" + "="*80 + "\n")

    # Test with example
    example = """TODO"""
    assert solve_part1(example) == 0  # TODO: expected value

    # Solve part 1
    data = get_data(day=DAY, year=YEAR)
    ans1 = solve_part1(data)
    print(f"Part 1: {ans1}")
    submit(ans1, part="a", day=DAY, year=YEAR)

    # Fetch part 2
    print("\n" + "="*80 + "\n")
    print(fetch_problem_part2(YEAR, DAY))
    print("\n" + "="*80 + "\n")

    # Test part 2 with example
    assert solve_part2(example) == 0  # TODO: expected value

    # Solve part 2
    ans2 = solve_part2(data)
    print(f"Part 2: {ans2}")
    submit(ans2, part="b", day=DAY, year=YEAR)
