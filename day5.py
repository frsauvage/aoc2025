from aocd import get_data, submit

def solve_part1(data):
    lines = data.strip().split('\n')

    # Find the blank line separating ranges from IDs
    blank_idx = lines.index('')

    # Parse ranges
    ranges = []
    for line in lines[:blank_idx]:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    # Parse ingredient IDs
    ingredient_ids = [int(line) for line in lines[blank_idx + 1:]]

    # Count fresh ingredients
    fresh_count = 0
    for ingredient_id in ingredient_ids:
        for start, end in ranges:
            if start <= ingredient_id <= end:
                fresh_count += 1
                break

    return fresh_count

def solve_part2(data):
    lines = data.strip().split('\n')

    # Find the blank line separating ranges from IDs
    blank_idx = lines.index('')

    # Parse ranges
    ranges = []
    for line in lines[:blank_idx]:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    # Merge overlapping ranges and count total unique IDs
    ranges.sort()
    merged = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            # Overlapping or adjacent - merge
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            # Non-overlapping - add new range
            merged.append((start, end))

    # Count total IDs in merged ranges
    total = 0
    for start, end in merged:
        total += end - start + 1

    return total

if __name__ == "__main__":
    data = get_data(day=5, year=2025)

    # Test with example
    example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

    example_result = solve_part1(example)
    print(f"Example result: {example_result}")
    assert example_result == 3, f"Expected 3, got {example_result}"

    # Solve part 1
    answer1 = solve_part1(data)
    print(f"Part 1: {answer1}")
    # submit(answer1, part="a", day=5, year=2025)  # Already submitted

    # Test part 2 with example
    example_result2 = solve_part2(example)
    print(f"Example Part 2 result: {example_result2}")
    assert example_result2 == 14, f"Expected 14, got {example_result2}"

    # Solve part 2
    answer2 = solve_part2(data)
    print(f"Part 2: {answer2}")
    submit(answer2, part="b", day=5, year=2025)
