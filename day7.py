from aocd import get_data, submit
from collections import deque

DAY = 7
YEAR = 2025

def solve_part1(data):
    lines = data.strip().split('\n')
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    # Find starting position S
    start_col = None
    for c in range(cols):
        if grid[0][c] == 'S':
            start_col = c
            break

    # Queue: (start_row, col) - beams moving downward from a specific row
    queue = deque([(0, start_col)])
    visited_beams = set()  # Track (start_row, col) to avoid duplicate beams
    visited_splits = set()  # Track which splitters we've actually triggered
    split_count = 0

    while queue:
        start_row, col = queue.popleft()

        # Skip if we've already processed this beam
        if (start_row, col) in visited_beams:
            continue
        visited_beams.add((start_row, col))

        # Move this beam downward until it hits a splitter or exits
        for row in range(start_row, rows):
            cell = grid[row][col]

            if cell == '^':
                # Hit a splitter - count it only if we haven't counted it before
                if (row, col) not in visited_splits:
                    visited_splits.add((row, col))
                    split_count += 1

                # Create two new beams starting from the next row
                left_col = col - 1
                right_col = col + 1

                if left_col >= 0:
                    queue.append((row + 1, left_col))
                if right_col < cols:
                    queue.append((row + 1, right_col))

                break  # This beam stops

    return split_count

# Test with example
example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

def solve_part2(data):
    lines = data.strip().split('\n')
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    # Find starting position S
    start_col = None
    for c in range(cols):
        if grid[0][c] == 'S':
            start_col = c
            break

    # Use dynamic programming approach
    # dp[row][col] = number of timelines reaching this position
    # Start with 1 timeline at the starting position
    current_row_counts = {start_col: 1}

    for row in range(rows):
        next_row_counts = {}

        for col, count in current_row_counts.items():
            cell = grid[row][col]

            if cell == '^':
                # Split into two timelines
                left_col = col - 1
                right_col = col + 1

                if left_col >= 0:
                    next_row_counts[left_col] = next_row_counts.get(left_col, 0) + count
                if right_col < cols:
                    next_row_counts[right_col] = next_row_counts.get(right_col, 0) + count
            else:
                # Continue downward
                next_row_counts[col] = next_row_counts.get(col, 0) + count

        current_row_counts = next_row_counts

    # Total timelines is the sum of all timelines that exited the manifold
    return sum(current_row_counts.values())

test_result = solve_part1(example)
print(f"Part 1 test result: {test_result} (expected: 21)")

test_result2 = solve_part2(example)
print(f"Part 2 test result: {test_result2} (expected: 40)")

if test_result == 21 and test_result2 == 40:
    # Get real data and solve
    data = get_data(day=DAY, year=YEAR)

    # Part 1
    ans1 = solve_part1(data)
    print(f"Part 1 answer: {ans1}")

    # Part 2
    ans2 = solve_part2(data)
    print(f"Part 2 answer: {ans2}")
    submit(ans2, part="b", day=DAY, year=YEAR)
else:
    print("Test failed!")
