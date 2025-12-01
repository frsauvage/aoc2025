"""
Advent of Code 2025 - Day 1: Safe Cracking
Solution for the dial rotation problem.
"""

from aocd.models import Puzzle


def solve_part1(rotations: list[str]) -> int:
    """
    Simulate the dial rotations and count how many times it points at 0.

    Args:
        rotations: List of rotation instructions (e.g., "L68", "R48")

    Returns:
        Number of times the dial points at 0 after any rotation
    """
    position = 50  # Starting position
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'L':
            # Left rotation: subtract and wrap with modulo
            position = (position - distance) % 100
        else:  # direction == 'R'
            # Right rotation: add and wrap with modulo
            position = (position + distance) % 100

        # Check if dial points at 0 after this rotation
        if position == 0:
            zero_count += 1

    return zero_count


def solve_part2(rotations: list[str]) -> int:
    """
    Count all times the dial passes through 0 during any rotation.

    This includes both:
    - Landing on 0 at the end of a rotation
    - Passing through 0 during a rotation

    Args:
        rotations: List of rotation instructions (e.g., "L68", "R48")

    Returns:
        Total number of times the dial points at 0 during all rotations
    """
    position = 50  # Starting position
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'R':
            # Right rotation: count how many times we pass through or land on 0
            # When rotating right from position by distance clicks
            # We pass through 0 at clicks: (100 - position), (100 - position) + 100, etc.
            # Number of times = distance // (100 - position) if we start before crossing
            # Actually: we cross 0 every 100 clicks starting from (100 - position)
            # Simpler: count = floor((position + distance) / 100) - floor(position / 100)
            # This counts complete cycles through 0
            # But we need to check if we land exactly on 0 or pass through it

            # Count how many times we hit 0 (including landing on it)
            # We hit 0 at absolute positions: 100, 200, 300, etc.
            # Starting from position, we're at absolute position 'position'
            # After distance clicks, we're at absolute position 'position + distance'
            # Count multiples of 100 in range (position, position + distance]

            # IMPORTANT: If position is 0, we don't count it - we start FROM 0
            # The first click takes us to 1, not 0
            if position == 0:
                # Starting from 0, going right
                # We hit 0 again at click 100, 200, 300, ...
                zeros_crossed = distance // 100
            else:
                # Normal case: count multiples of 100 we cross
                zeros_crossed = (position + distance) // 100 - position // 100

            zero_count += zeros_crossed
            position = (position + distance) % 100
        else:  # direction == 'L'
            # Left rotation: count how many times we pass through or land on 0
            # When rotating left from position by distance clicks
            # Going left means decreasing: position, position-1, position-2, ...
            # We hit 0 when we go from position down by position clicks
            # Then we hit 0 again every 100 clicks
            # So we hit 0 at clicks: position, position + 100, position + 200, etc.
            # Count how many of these are <= distance

            # IMPORTANT: If position is 0, we don't count it - we start FROM 0
            # The first click takes us to 99, not 0
            if position == 0:
                # Starting from 0, going left
                # We hit 0 again at click 100, 200, 300, ...
                zeros_crossed = distance // 100
            elif distance >= position:
                # We definitely hit 0 at least once
                # First hit at click number 'position' (when we reach 0)
                # Subsequent hits every 100 clicks: position, position+100, position+200, ...
                # Count = floor((distance - position) / 100) + 1
                zeros_crossed = (distance - position) // 100 + 1
            else:
                # We don't reach 0
                zeros_crossed = 0

            zero_count += zeros_crossed
            position = (position - distance) % 100

    return zero_count


def main():
    """Main function to solve the puzzle."""
    # Fetch puzzle input
    puzzle = Puzzle(year=2025, day=1)
    data = puzzle.input_data

    # Parse the rotations
    rotations = data.strip().split('\n')

    # Solve part 1
    answer1 = solve_part1(rotations)
    print(f"Part 1: The password is {answer1}")

    # Solve part 2
    answer2 = solve_part2(rotations)
    print(f"Part 2: The password is {answer2}")

    # Submit the answers
    puzzle.answer_a = answer1
    puzzle.answer_b = answer2


def test_example():
    """Test with the provided example."""
    example_rotations = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82"
    ]

    print("=== Part 1 Test ===")
    position = 50
    positions = [position]

    for rotation in example_rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100

        positions.append(position)

    print("Example trace:")
    print(f"Start: 50")

    example_labels = [
        "L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"
    ]

    for i, (label, pos) in enumerate(zip(example_labels, positions[1:]), 1):
        marker = " <- Zero!" if pos == 0 else ""
        print(f"{label}: {pos}{marker}")

    result1 = solve_part1(example_rotations)
    print(f"\nPart 1 - Zero count: {result1}")
    assert result1 == 3, f"Expected 3, got {result1}"
    print("Part 1 test passed!")

    print("\n=== Part 2 Test ===")
    # Detailed trace for Part 2
    position = 50
    total_zeros = 0

    print(f"Start: {position}")

    for rotation in example_rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'R':
            if position == 0:
                zeros_in_rotation = distance // 100
            else:
                zeros_in_rotation = (position + distance) // 100 - position // 100
            new_position = (position + distance) % 100
        else:  # L
            if position == 0:
                zeros_in_rotation = distance // 100
            elif distance >= position:
                zeros_in_rotation = (distance - position) // 100 + 1
            else:
                zeros_in_rotation = 0
            new_position = (position - distance) % 100

        total_zeros += zeros_in_rotation

        during_marker = f" (hits 0 {zeros_in_rotation} time(s))" if zeros_in_rotation > 0 else ""
        print(f"{rotation}: {position} -> {new_position}{during_marker}")

        position = new_position

    result2 = solve_part2(example_rotations)
    print(f"\nPart 2 - Total zero count: {result2}")
    assert result2 == 6, f"Expected 6, got {result2}"
    print("Part 2 test passed!")


if __name__ == "__main__":
    # Run the example test first
    test_example()
    print("\n" + "="*50 + "\n")

    # Solve the actual puzzle
    main()
