from aocd import get_data, submit
from itertools import combinations

def solve_part1(data):
    """Find maximum joltage from each battery bank by picking 2 batteries."""
    return sum(
        max(int(bank[i] + bank[j]) for i, j in combinations(range(len(bank)), 2))
        for bank in data.strip().split('\n')
    )

def solve_part2(data, k=12):
    """Find maximum joltage by picking k batteries from each bank."""
    total = 0
    for bank in data.strip().split('\n'):
        n = len(bank)
        result = []
        start = 0

        for pos in range(k):
            remaining_needed = k - pos
            max_end = n - remaining_needed + 1

            # Find position of max digit in valid range
            valid_range = bank[start:max_end]
            best_digit = max(valid_range)
            best_pos = start + valid_range.index(best_digit)

            result.append(best_digit)
            start = best_pos + 1

        total += int(''.join(result))

    return total

# Test with example
example = """987654321111111
811111111111119
234234234234278
818181911112111"""

result = solve_part1(example)
print(f"Part 1 example: {result}")
assert result == 357, f"Expected 357, got {result}"

result2 = solve_part2(example, k=12)
print(f"Part 2 example: {result2}")
assert result2 == 3121910778619, f"Expected 3121910778619, got {result2}"

# Solve with real input
data = get_data(day=3, year=2025)

answer2 = solve_part2(data, k=12)
print(f"Part 2 answer: {answer2}")

# Submit part 2
submit(answer2, part="b", day=3, year=2025)
