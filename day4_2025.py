"""
Advent of Code 2025 - Day 4: Printing Department

Algorithms used:
- Part 1: Grid traversal + neighbor counting (8-directional adjacency)
- Part 2: Iterative simulation (cellular automaton-like removal)
- Data structures: Set for O(1) lookup, coordinate-based grid representation
"""

from aocd import get_data, submit

DIRECTIONS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def parse_rolls(data):
    """Parse grid and extract all paper roll positions."""
    lines = data.strip().split('\n')
    return {(r, c) for r, line in enumerate(lines)
            for c, char in enumerate(line) if char == '@'}

def count_neighbors(pos, rolls):
    """Count how many neighbors a position has."""
    r, c = pos
    return sum(1 for dr, dc in DIRECTIONS if (r + dr, c + dc) in rolls)

def find_accessible(rolls):
    """Find all rolls with fewer than 4 neighbors."""
    return {pos for pos in rolls if count_neighbors(pos, rolls) < 4}

def solve_part1(data):
    """
    Count paper rolls with fewer than 4 adjacent rolls.

    Algorithm: Grid neighbor counting
    - Parse grid into set of coordinates
    - For each position, count 8-directional neighbors
    - Count positions with < 4 neighbors

    Complexity: O(n) where n = number of rolls
    """
    rolls = parse_rolls(data)
    return len(find_accessible(rolls))

def solve_part2(data):
    """
    Remove all accessible rolls iteratively until none remain.

    Algorithm: Iterative simulation (similar to cellular automaton)
    - Repeatedly find all rolls with < 4 neighbors
    - Remove them simultaneously
    - Recalculate neighbors for remaining rolls
    - Continue until no more can be removed

    Complexity: O(k * n) where k = number of iterations, n = number of rolls
    """
    rolls = parse_rolls(data)
    total_removed = 0

    while True:
        accessible = find_accessible(rolls)
        if not accessible:
            break

        rolls -= accessible
        total_removed += len(accessible)

    return total_removed


# Test with example
example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

test_result1 = solve_part1(example)
print(f"Part 1 example: {test_result1} (expected: 13)")

test_result2 = solve_part2(example)
print(f"Part 2 example: {test_result2} (expected: 43)")

# Solve part 1
data = get_data(day=4, year=2025)
answer1 = solve_part1(data)
print(f"\nPart 1 answer: {answer1}")
# submit(answer1, part="a", day=4, year=2025)  # Already submitted

# Solve part 2
answer2 = solve_part2(data)
print(f"Part 2 answer: {answer2}")
submit(answer2, part="b", day=4, year=2025)
