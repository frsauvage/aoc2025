from day11 import solve_part2

# Test part 2 with example
example2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

test_result2 = solve_part2(example2)
print(f"Part 2 Example result: {test_result2}")
assert test_result2 == 2, f"Expected 2, got {test_result2}"
print("Test passed!")
