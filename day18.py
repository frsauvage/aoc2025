from aocd import get_data, submit
import json
from math import floor, ceil

DAY = 18
YEAR = 2021

def parse_input(data):
    return [json.loads(line) for line in data.strip().split('\n')]

def add_to_left(num, val):
    """Add value to the leftmost regular number"""
    if val is None:
        return num
    if isinstance(num, int):
        return num + val
    return [add_to_left(num[0], val), num[1]]

def add_to_right(num, val):
    """Add value to the rightmost regular number"""
    if val is None:
        return num
    if isinstance(num, int):
        return num + val
    return [num[0], add_to_right(num[1], val)]

def explode(num, depth=0):
    """Try to explode the leftmost pair nested in 4 pairs. Returns (new_num, left_val, right_val, exploded)"""
    if isinstance(num, int):
        return num, None, None, False

    if depth == 4:
        # This pair should explode
        return 0, num[0], num[1], True

    # Try to explode left side
    left, l_val, r_val, exploded = explode(num[0], depth + 1)
    if exploded:
        # Add r_val to the right side
        right = add_to_left(num[1], r_val)
        return [left, right], l_val, None, True

    # Try to explode right side
    right, l_val, r_val, exploded = explode(num[1], depth + 1)
    if exploded:
        # Add l_val to the left side
        left = add_to_right(num[0], l_val)
        return [left, right], None, r_val, True

    return num, None, None, False

def split(num):
    """Try to split the leftmost number >= 10. Returns (new_num, split_occurred)"""
    if isinstance(num, int):
        if num >= 10:
            return [num // 2, (num + 1) // 2], True
        return num, False

    left, split_occurred = split(num[0])
    if split_occurred:
        return [left, num[1]], True

    right, split_occurred = split(num[1])
    if split_occurred:
        return [num[0], right], True

    return num, False

def reduce_snailfish(num):
    """Fully reduce a snailfish number"""
    while True:
        # Try to explode
        num, _, _, exploded = explode(num)
        if exploded:
            continue

        # Try to split
        num, split_occurred = split(num)
        if split_occurred:
            continue

        # No more reductions possible
        break

    return num

def add_snailfish(a, b):
    """Add two snailfish numbers and reduce"""
    return reduce_snailfish([a, b])

def magnitude(num):
    """Calculate magnitude of a snailfish number"""
    if isinstance(num, int):
        return num
    return 3 * magnitude(num[0]) + 2 * magnitude(num[1])

def part1(data):
    numbers = parse_input(data)
    result = numbers[0]
    for num in numbers[1:]:
        result = add_snailfish(result, num)
    return magnitude(result)

def part2(data):
    numbers = parse_input(data)
    max_mag = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j:
                mag = magnitude(add_snailfish(numbers[i], numbers[j]))
                max_mag = max(max_mag, mag)
    return max_mag

# Test with examples
test_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

print("Testing Part 1...")
test_result = part1(test_input)
print(f"Test result: {test_result}")
assert test_result == 4140, f"Expected 4140, got {test_result}"
print("Test Part 1 passed!")

print("\nTesting Part 2...")
test_result2 = part2(test_input)
print(f"Test result: {test_result2}")
assert test_result2 == 3993, f"Expected 3993, got {test_result2}"
print("Test Part 2 passed!")

# Solve Part 1
data = get_data(day=DAY, year=YEAR)
ans1 = part1(data)
print(f"\nPart 1: {ans1}")
# submit(ans1, part="a", day=DAY, year=YEAR)

# Solve Part 2
ans2 = part2(data)
print(f"Part 2: {ans2}")
submit(ans2, part="b", day=DAY, year=YEAR)
