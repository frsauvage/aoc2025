from aocd import get_data, submit

DAY = 1
YEAR = 2020

def solve_part1(data):
    """
    Find two numbers that sum to 2020 and return their product.
    Use a set for O(n) lookup - for each number, check if (2020 - number) exists.
    """
    numbers = [int(line) for line in data.strip().split('\n')]
    seen = set()

    for num in numbers:
        complement = 2020 - num
        if complement in seen:
            return num * complement
        seen.add(num)

    return None

def solve_part2(data):
    """
    Find three numbers that sum to 2020 and return their product.
    Use nested loop with set lookup - for each pair, check if (2020 - sum) exists.
    """
    numbers = [int(line) for line in data.strip().split('\n')]
    num_set = set(numbers)

    for i, num1 in enumerate(numbers):
        for num2 in numbers[i+1:]:
            complement = 2020 - num1 - num2
            if complement in num_set and complement != num1 and complement != num2:
                return num1 * num2 * complement

    return None

if __name__ == "__main__":
    # Test with example
    example = """1721
979
366
299
675
1456"""

    test_result = solve_part1(example)
    print(f"Part 1 Test: {test_result} (expected 514579)")
    assert test_result == 514579, f"Test failed: got {test_result}"

    # Get real data and solve part 1
    data = get_data(day=DAY, year=YEAR)
    ans1 = solve_part1(data)
    print(f"Part 1 Answer: {ans1}")
    # submit(ans1, part="a", day=DAY, year=YEAR)  # Already submitted

    # Test part 2
    test_result2 = solve_part2(example)
    print(f"Part 2 Test: {test_result2} (expected 241861950)")
    assert test_result2 == 241861950, f"Test failed: got {test_result2}"

    # Solve part 2
    ans2 = solve_part2(data)
    print(f"Part 2 Answer: {ans2}")
    submit(ans2, part="b", day=DAY, year=YEAR)
