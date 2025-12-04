"""
Advent of Code 2025 - Day 4: Visual Demonstration
Shows the step-by-step removal process with visual grids.
"""

from aocd import get_data

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

def print_grid(rolls, accessible=None, removed=None, rows=10, cols=10):
    """
    Print a visual representation of the grid.

    Args:
        rolls: Set of current roll positions
        accessible: Set of accessible rolls to highlight (optional)
        removed: Set of just-removed rolls to show (optional)
        rows, cols: Grid dimensions
    """
    for r in range(rows):
        line = ""
        for c in range(cols):
            pos = (r, c)
            if removed and pos in removed:
                line += "."  # Recently removed (shown as empty)
            elif accessible and pos in accessible:
                line += "x"  # Accessible (will be removed)
            elif pos in rolls:
                line += "@"  # Current roll
            else:
                line += "."  # Empty space
        print(line)

def print_neighbor_counts(rolls, rows=10, cols=10):
    """Print grid showing neighbor counts for each roll."""
    for r in range(rows):
        line = ""
        for c in range(cols):
            pos = (r, c)
            if pos in rolls:
                neighbors = count_neighbors(pos, rolls)
                line += str(neighbors)
            else:
                line += "."
        print(line)

def visualize_part1(data):
    """Visualize Part 1: Show which rolls are accessible."""
    print("=" * 60)
    print("PART 1: Identifying Accessible Rolls")
    print("=" * 60)

    rolls = parse_rolls(data)
    accessible = find_accessible(rolls)

    lines = data.strip().split('\n')
    rows, cols = len(lines), len(lines[0])

    print(f"\nTotal rolls: {len(rolls)}")
    print(f"Accessible rolls (< 4 neighbors): {len(accessible)}")

    print("\n--- Original Grid ---")
    print_grid(rolls, rows=rows, cols=cols)

    print("\n--- Neighbor Counts ---")
    print_neighbor_counts(rolls, rows=rows, cols=cols)

    print("\n--- Accessible Rolls (marked with 'x') ---")
    print_grid(rolls, accessible=accessible, rows=rows, cols=cols)

    print("\n--- Examples ---")
    # Show some specific examples
    example_positions = list(accessible)[:5]
    for pos in example_positions:
        r, c = pos
        neighbors = count_neighbors(pos, rolls)
        print(f"  Position ({r},{c}): {neighbors} neighbors -> accessible [YES]")

    non_accessible = list(rolls - accessible)[:3]
    for pos in non_accessible:
        r, c = pos
        neighbors = count_neighbors(pos, rolls)
        print(f"  Position ({r},{c}): {neighbors} neighbors -> NOT accessible [NO]")

def visualize_part2(data):
    """Visualize Part 2: Show iterative removal process."""
    print("\n" + "=" * 60)
    print("PART 2: Iterative Removal Process")
    print("=" * 60)

    rolls = parse_rolls(data)
    lines = data.strip().split('\n')
    rows, cols = len(lines), len(lines[0])

    total_removed = 0
    round_num = 0

    print(f"\nInitial state: {len(rolls)} rolls")
    print_grid(rolls, rows=rows, cols=cols)

    # Track removal history
    removal_history = []

    while True:
        accessible = find_accessible(rolls)
        if not accessible:
            break

        round_num += 1
        removal_history.append(len(accessible))

        print(f"\n{'-' * 60}")
        print(f"ROUND {round_num}: Found {len(accessible)} accessible rolls")
        print(f"{'-' * 60}")

        # Show which rolls will be removed
        print("\n--- Rolls to Remove (marked with 'x') ---")
        print_grid(rolls, accessible=accessible, rows=rows, cols=cols)

        # Remove them
        removed_this_round = accessible.copy()
        rolls -= accessible
        total_removed += len(accessible)

        # Show grid after removal
        print("\n--- After Removal ---")
        print_grid(rolls, removed=removed_this_round, rows=rows, cols=cols)
        print(f"Remaining rolls: {len(rolls)}")
        print(f"Total removed so far: {total_removed}")

    print(f"\n{'=' * 60}")
    print("FINAL RESULTS")
    print(f"{'=' * 60}")
    print(f"\nTotal rounds: {round_num}")
    print(f"Total removed: {total_removed}")
    print(f"Remaining rolls: {len(rolls)} (all with >= 4 neighbors)")

    print("\n--- Removal History ---")
    for i, count in enumerate(removal_history, 1):
        print(f"  Round {i}: removed {count} rolls")

    print("\n--- Final Grid ---")
    print_grid(rolls, rows=rows, cols=cols)

    if len(rolls) > 0:
        print("\n--- Final Neighbor Counts ---")
        print_neighbor_counts(rolls, rows=rows, cols=cols)
        print("\nAll remaining rolls have >= 4 neighbors (dense cluster)")

if __name__ == "__main__":
    # Use example data for clear visualization
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

    print("ADVENT OF CODE 2025 - DAY 4")
    print("Visual Demonstration with Example Data")
    print()

    visualize_part1(example)
    visualize_part2(example)

    # Optionally run with real data (commented out for brevity)
    # print("\n\n" + "=" * 60)
    # print("RUNNING WITH REAL INPUT DATA")
    # print("=" * 60)
    # data = get_data(day=4, year=2025)
    # visualize_part1(data)
    # visualize_part2(data)
