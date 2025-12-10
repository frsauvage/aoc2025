import re
import pulp
import numpy as np
from itertools import product

# ============================================================
# ---------------------- PART 2 -------------------------------
# ============================================================

def parse_line_part2(line):
    # Extract joltage requirements
    req = re.search(r"\{([0-9,]+)\}", line).group(1)
    target = list(map(int, req.split(',')))
    k = len(target)

    # Extract button definitions
    buttons = [tuple(map(int, g.split(',')))
               for g in re.findall(r"\(([\d,]+)\)", line)]
    m = len(buttons)

    A = []
    for btn in buttons:
        row = [0]*k
        for idx in btn:
            row[idx] += 1
        A.append(row)
    return target, A


def solve_machine_minpresses(target, A):
    """
    Solve min sum(x_i) subject to A^T x = target,
    x_i >= 0 integers.
    A is m x k (m buttons, k counters).
    """

    m, k = len(A), len(A[0])

    # ILP model
    model = pulp.LpProblem("machine", pulp.LpMinimize)

    x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer')
         for i in range(m)]

    # Objective
    model += pulp.lpSum(x)

    # Constraints: sum_i x_i * A[i][j] == target[j]
    for j in range(k):
        model += pulp.lpSum(x[i] * A[i][j] for i in range(m)) == target[j]

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[model.status] != "Optimal":
        raise ValueError("No integer solution found")

    return sum(int(v.value()) for v in x)


def compute_total_part2(filename):
    total = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            target, A = parse_line_part2(line)
            total += solve_machine_minpresses(target, A)
    return total


# ============================================================
# ---------------------- PART 1 -------------------------------
# ============================================================

def parse_line_part1(line):
    diag = re.search(r"\[([.#]+)\]", line).group(1)
    target = [1 if c == '#' else 0 for c in diag]
    n = len(target)

    buttons = [tuple(map(int, g.split(',')))
               for g in re.findall(r"\(([\d,]+)\)", line)]

    A = []
    for btn in buttons:
        row = [0]*n
        for idx in btn:
            row[idx] ^= 1
        A.append(row)
    return target, A


def gf2_solve_minweight(target, A):
    """
    Solve A^T x = target over GF(2), minimizing Hamming weight(x).
    A: m x n, unknowns = m buttons.
    """

    A = np.array(A, dtype=int)
    b = np.array(target, dtype=int)
    m, n = A.shape

    M = np.concatenate([A.T, b.reshape(-1,1)], axis=1).copy()
    rows, cols = M.shape

    pivot_cols = [-1]*rows
    r = 0
    for c in range(m):
        pivot = None
        for i in range(r, rows):
            if M[i, c] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            M[[pivot, r]] = M[[r, pivot]]
        pivot_cols[r] = c
        for i in range(rows):
            if i != r and M[i, c] == 1:
                M[i] ^= M[r]
        r += 1
        if r == rows:
            break

    for i in range(rows):
        if pivot_cols[i] == -1 and M[i, -1] == 1:
            return float("inf")

    pivots = set(pc for pc in pivot_cols if pc != -1)
    free = [c for c in range(m) if c not in pivots]

    xp = np.zeros(m, dtype=int)
    for i in range(rows):
        pc = pivot_cols[i]
        if pc != -1:
            xp[pc] = M[i, -1]

    nullvecs = []
    for fc in free:
        v = np.zeros(m, dtype=int)
        v[fc] = 1
        for i in range(rows):
            pc = pivot_cols[i]
            if pc != -1 and M[i, fc] == 1:
                v[pc] ^= 1
        nullvecs.append(v)

    best = float("inf")
    for mask in product([0,1], repeat=len(free)):
        x = xp.copy()
        for bit, v in zip(mask, nullvecs):
            if bit:
                x ^= v
        wt = x.sum()
        if wt < best:
            best = wt

    return best


def compute_total_part1(filename):
    total = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            target, A = parse_line_part1(line)
            total += gf2_solve_minweight(target, A)
    return total


# ============================================================
# ---------------------- TEST & MAIN --------------------------
# ============================================================

# Part 2 example test
example = [
"[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
"[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
"[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
]

expected = 33
got = sum(solve_machine_minpresses(*parse_line_part2(line)) for line in example)
print("Example result:", got, "Expected:", expected)


if __name__ == "__main__":
    print("Part 1:", compute_total_part1("input_day10_2025.txt"))
    print("Part 2:", compute_total_part2("input_day10_2025.txt"))
