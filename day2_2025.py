"""
Advent of Code 2025 - Day 2: Gift Shop
Solution for identifying invalid product IDs.
"""

from aocd.models import Puzzle
from typing import List, Tuple
from functools import lru_cache
from aoc_utils import fetch_problem_part1, fetch_problem_part2, fetch_problem_text


@lru_cache(maxsize=10000)
def is_invalid_id(num: int) -> bool:
    """
    Check if a product ID is invalid (made of a repeated sequence).

    An ID is invalid if it consists of some sequence of digits repeated exactly twice.
    Examples: 55 (5 repeated), 6464 (64 repeated), 123123 (123 repeated)

    Args:
        num: The product ID to check

    Returns:
        True if the ID is invalid, False otherwise
    """
    # Convert to string to analyze digit pattern
    s = str(num)
    length = len(s)

    # Must have even length to be split in half
    if length % 2 != 0:
        return False

    # Split in half and compare
    mid = length // 2
    first_half = s[:mid]
    second_half = s[mid:]

    return first_half == second_half


@lru_cache(maxsize=10000)
def is_invalid_id_part2(num: int) -> bool:
    """
    Check if a product ID is invalid using Part 2 rules.

    An ID is invalid if it consists of some sequence of digits repeated at least twice.
    Examples:
    - 12341234 (1234 repeated 2 times)
    - 123123123 (123 repeated 3 times)
    - 1212121212 (12 repeated 5 times)
    - 1111111 (1 repeated 7 times)

    Args:
        num: The product ID to check

    Returns:
        True if the ID is invalid, False otherwise
    """
    s = str(num)
    length = len(s)

    # Try all possible pattern lengths (from 1 to length//2)
    # Pattern must repeat at least twice, so max pattern length is length//2
    for pattern_len in range(1, length // 2 + 1):
        # Check if length is divisible by pattern length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            repetitions = length // pattern_len

            # Need at least 2 repetitions
            if repetitions >= 2:
                # Check if the entire string is this pattern repeated
                if pattern * repetitions == s:
                    return True

    return False


def parse_ranges(input_data: str) -> List[Tuple[int, int]]:
    """
    Parse the input data containing product ID ranges.

    Args:
        input_data: String containing comma-separated ranges (e.g., "11-22,95-115")

    Returns:
        List of tuples representing (start, end) ranges
    """
    ranges = []
    for range_str in input_data.strip().split(','):
        start, end = map(int, range_str.split('-'))
        ranges.append((start, end))
    return ranges


def find_invalid_ids_in_range(start: int, end: int, part2: bool = False) -> List[int]:
    """
    Find all invalid IDs within a given range.

    Args:
        start: Start of the range (inclusive)
        end: End of the range (inclusive)
        part2: If True, use Part 2 rules (at least 2 repetitions), else Part 1 (exactly 2)

    Returns:
        List of invalid IDs in the range
    """
    invalid_ids = []
    check_func = is_invalid_id_part2 if part2 else is_invalid_id

    for num in range(start, end + 1):
        if check_func(num):
            invalid_ids.append(num)

    return invalid_ids


def solve_part1(input_data: str) -> int:
    """
    Solve Part 1: Sum all invalid product IDs across all ranges.

    Args:
        input_data: String containing comma-separated ranges

    Returns:
        Sum of all invalid product IDs
    """
    ranges = parse_ranges(input_data)
    total_sum = 0

    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end)
        total_sum += sum(invalid_ids)

    return total_sum


def solve_part2(input_data: str) -> int:
    """
    Solve Part 2: Sum all invalid product IDs using new rules.

    New rules: An ID is invalid if it consists of some sequence repeated at least twice
    (not just exactly twice as in Part 1).

    Args:
        input_data: String containing comma-separated ranges

    Returns:
        Sum of all invalid product IDs using Part 2 rules
    """
    ranges = parse_ranges(input_data)
    total_sum = 0

    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end, part2=True)
        total_sum += sum(invalid_ids)

    return total_sum


def main():
    """Main function to solve the puzzle."""
    # Fetch and display problem text
    print("=== Récupération du texte du problème ===\n")
    try:
        problem_text = fetch_problem_text(year=2025, day=2)
        print(problem_text)
        print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Erreur lors de la récupération du texte: {e}\n")

    # Fetch puzzle input
    puzzle = Puzzle(year=2025, day=2)
    data = puzzle.input_data

    # Solve part 1
    answer1 = solve_part1(data)
    print(f"Part 1: Sum of invalid IDs = {answer1}")

    # Submit the answer for Part 1
    try:
        puzzle.answer_a = answer1
        print("Part 1 answer submitted successfully!")
    except Exception as e:
        print(f"Error submitting Part 1: {e}")

    # Solve part 2
    answer2 = solve_part2(data)
    print(f"Part 2: Sum of invalid IDs (at least 2 reps) = {answer2}")

    # Submit the answer for Part 2
    try:
        puzzle.answer_b = answer2
        print("Part 2 answer submitted successfully!")
    except Exception as e:
        print(f"Error submitting Part 2: {e}")

def test_examples():
    """Test with the provided examples."""
    print("=== Testing Examples ===\n")

    # Test individual invalid ID detection - Part 1
    test_cases_part1 = [
        (55, True, "55 is '5' repeated twice"),
        (6464, True, "6464 is '64' repeated twice"),
        (123123, True, "123123 is '123' repeated twice"),
        (11, True, "11 is '1' repeated twice"),
        (22, True, "22 is '2' repeated twice"),
        (99, True, "99 is '9' repeated twice"),
        (1010, True, "1010 is '10' repeated twice"),
        (12, False, "12 cannot be split into identical halves"),
        (123, False, "123 has odd length"),
        (1234, False, "1234 is not '12' repeated twice"),
    ]

    print("=== Part 1 Testing ===")
    print("Testing invalid ID detection (exactly 2 repetitions):")
    all_passed = True
    for num, expected, description in test_cases_part1:
        result = is_invalid_id(num)
        status = "[PASS]" if result == expected else "[FAIL]"
        print(f"{status} {num}: {result} (expected {expected}) - {description}")
        if result != expected:
            all_passed = False

    if all_passed:
        print("\n[PASS] All Part 1 ID detection tests passed!\n")
    else:
        print("\n[FAIL] Some Part 1 tests failed!\n")

    # Test Part 2 - at least 2 repetitions
    test_cases_part2 = [
        (111, True, "111 is '1' repeated 3 times"),
        (999, True, "999 is '9' repeated 3 times"),
        (12341234, True, "12341234 is '1234' repeated 2 times"),
        (123123123, True, "123123123 is '123' repeated 3 times"),
        (1212121212, True, "1212121212 is '12' repeated 5 times"),
        (1111111, True, "1111111 is '1' repeated 7 times"),
        (565656, True, "565656 is '56' repeated 3 times"),
        (824824824, True, "824824824 is '824' repeated 3 times"),
        (2121212121, True, "2121212121 is '21212' repeated 2 times"),
        (11, True, "11 is still invalid (2 repetitions)"),
        (123, False, "123 cannot be decomposed into repetitions"),
        (1234, False, "1234 cannot be decomposed into repetitions"),
    ]

    print("=== Part 2 Testing ===")
    print("Testing invalid ID detection (at least 2 repetitions):")
    all_passed_p2 = True
    for num, expected, description in test_cases_part2:
        result = is_invalid_id_part2(num)
        status = "[PASS]" if result == expected else "[FAIL]"
        print(f"{status} {num}: {result} (expected {expected}) - {description}")
        if result != expected:
            all_passed_p2 = False

    if all_passed_p2:
        print("\n[PASS] All Part 2 ID detection tests passed!\n")
    else:
        print("\n[FAIL] Some Part 2 tests failed!\n")

    # Test the full example - Part 1
    example_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

    print("Testing full example - Part 1:")
    print(f"Input: {example_input}\n")

    # Analyze each range
    ranges = parse_ranges(example_input)
    total = 0

    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end, part2=False)
        range_sum = sum(invalid_ids)
        total += range_sum
        print(f"Range {start}-{end}: invalid IDs = {invalid_ids}, sum = {range_sum}")

    print(f"\nPart 1 Total sum: {total}")
    print(f"Expected: 1227775554")

    if total == 1227775554:
        print("[PASS] Part 1 example test passed!")
    else:
        print(f"[FAIL] Part 1 example test failed! Got {total}, expected 1227775554")

    # Test the full example - Part 2
    print("\n" + "="*50)
    print("\nTesting full example - Part 2:")
    print(f"Input: {example_input}\n")

    total_p2 = 0

    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end, part2=True)
        range_sum = sum(invalid_ids)
        total_p2 += range_sum
        print(f"Range {start}-{end}: invalid IDs = {invalid_ids}, sum = {range_sum}")

    print(f"\nPart 2 Total sum: {total_p2}")
    print(f"Expected: 4174379265")

    if total_p2 == 4174379265:
        print("[PASS] Part 2 example test passed!")
    else:
        print(f"[FAIL] Part 2 example test failed! Got {total_p2}, expected 4174379265")


if __name__ == "__main__":
    # Run the example tests first
    test_examples()
    print("\n" + "="*50 + "\n")

    # Solve the actual puzzle
    main()
