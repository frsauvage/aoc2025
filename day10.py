from aocd import get_data, submit
import re

DAY = 10
YEAR = 2025

def parse_machine(line):
    """Parse a machine line into target state and button configs."""
    # Extract indicator lights [.##.]
    lights_match = re.search(r'\[([.#]+)\]', line)
    target = [1 if c == '#' else 0 for c in lights_match.group(1)]

    # Extract buttons (0,1,3,4)
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', line):
        button_indices = [int(x) for x in match.group(1).split(',')]
        buttons.append(button_indices)

    return target, buttons

def solve_gf2(target, buttons):
    """
    Solve the system over GF(2) to find minimum button presses.
    We need to try all combinations since we want minimum solution.
    """
    n_lights = len(target)
    n_buttons = len(buttons)

    # Try all 2^n_buttons combinations
    min_presses = float('inf')
    lefted_buttons = 1 << n_buttons
    for mask in range(lefted_buttons):
        # Check if this combination works
        state = [0] * n_lights
        presses = 0

        for button_idx in range(n_buttons):
            lefted_button = 1 << button_idx
            if mask & (lefted_button):
                presses += 1
                for light in buttons[button_idx]:
                    state[light] ^= 1

        if state == target:
            min_presses = min(min_presses, presses)

    return min_presses if min_presses != float('inf') else 0

def parse_joltage(line):
    """Parse joltage requirements from a machine line."""
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    return [int(x) for x in joltage_match.group(1).split(',')]

def solve_joltage(target, buttons):
    """
    Find minimum button presses to reach target counters.
    This is a linear combination problem: minimize sum(x_i) subject to sum(x_i * button_i) = target
    Use linear programming relaxation + rounding/search.
    """
    import numpy as np
    from scipy.optimize import linprog

    n_counters = len(target)
    n_buttons = len(buttons)

    # Build coefficient matrix: A @ x = target
    # A[i][j] = 1 if button j affects counter i
    A = np.zeros((n_counters, n_buttons), dtype=int)
    for j, button in enumerate(buttons):
        for i in button:
            A[i][j] = 1

    # LP relaxation: minimize sum(x) subject to A @ x = target, x >= 0
    c = np.ones(n_buttons)  # minimize sum of all variables

    # Equality constraints: A @ x = target
    A_eq = A
    b_eq = np.array(target)

    # Bounds: x >= 0
    bounds = [(0, None) for _ in range(n_buttons)]

    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if not result.success:
        return float('inf')

    # Try rounding strategies
    x_lp = result.x

    # Strategy 1: Round to nearest integer
    x_rounded = np.round(x_lp).astype(int)
    if np.all(A @ x_rounded == b_eq) and np.all(x_rounded >= 0):
        return int(np.sum(x_rounded))

    # Strategy 2: Ceiling
    x_ceil = np.ceil(x_lp).astype(int)
    if np.all(A @ x_ceil == b_eq) and np.all(x_ceil >= 0):
        return int(np.sum(x_ceil))

    # Strategy 3: Floor
    x_floor = np.floor(x_lp).astype(int)
    if np.all(A @ x_floor == b_eq) and np.all(x_floor >= 0):
        return int(np.sum(x_floor))

    # Strategy 4: Search around LP solution
    # Try small adjustments to find integer solution
    base = np.floor(x_lp).astype(int)

    # Use ILP solver for exact solution
    from scipy.optimize import milp, LinearConstraint, Bounds

    integrality = np.ones(n_buttons)  # All variables must be integers
    constraints = LinearConstraint(A, b_eq, b_eq)  # A @ x == b_eq
    bounds_obj = Bounds(lb=np.zeros(n_buttons), ub=np.full(n_buttons, np.inf))

    result_ilp = milp(c, integrality=integrality, constraints=constraints, bounds=bounds_obj)

    if result_ilp.success:
        return int(np.sum(result_ilp.x))

    return float('inf')

def solve_part1(data):
    """Solve part 1: find minimum button presses for all machines."""
    lines = data.strip().split('\n')
    total = 0

    for line in lines:
        target, buttons = parse_machine(line)
        min_presses = solve_gf2(target, buttons)
        total += min_presses

    return total

def solve_part2(data):
    """Solve part 2: find minimum button presses for joltage counters."""
    lines = data.strip().split('\n')
    total = 0

    for line in lines:
        _, buttons = parse_machine(line)
        target = parse_joltage(line)
        min_presses = solve_joltage(target, buttons)
        total += min_presses

    return total

# Test with example
example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

result1 = solve_part1(example)
print(f"Example Part 1: {result1} (expected: 7)")

result2 = solve_part2(example)
print(f"Example Part 2: {result2} (expected: 33)")

if result2 == 33:
    # Solve real input
    data = get_data(day=DAY, year=YEAR)
    ans2 = solve_part2(data)
    print(f"Part 2: {ans2}")
    submit(ans2, part="b", day=DAY, year=YEAR)
else:
    print("Example failed!")
