from aocd import get_data, submit
from aoc_utils import fetch_problem_part1, fetch_problem_part2
import math
from collections import defaultdict

DAY = 8
YEAR = 2025

def parse_input(data):
    """Parse junction box coordinates"""
    boxes = []
    for line in data.strip().split('\n'):
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))
    return boxes

def distance(p1, p2):
    """Calculate Euclidean distance between two 3D points"""
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

class UnionFind:
    """Union-Find data structure for tracking circuits"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already connected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

    def get_circuit_sizes(self):
        """Get sizes of all circuits"""
        circuits = defaultdict(int)
        for i in range(len(self.parent)):
            circuits[self.find(i)] += 1
        return sorted(circuits.values(), reverse=True)

def solve_part1(data, num_pairs):
    """Solve part 1: connect closest pairs and find three largest circuits"""
    boxes = parse_input(data)
    n = len(boxes)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(boxes[i], boxes[j])
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Union-Find to track circuits
    uf = UnionFind(n)

    # Try to connect the closest num_pairs pairs
    for idx in range(num_pairs):
        dist, i, j = distances[idx]
        uf.union(i, j)  # Connect even if already in same circuit

    # Get circuit sizes and multiply three largest
    circuit_sizes = uf.get_circuit_sizes()
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

# Test with example
example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

assert solve_part1(example, 10) == 40

# Solve part 1
data = get_data(day=DAY, year=YEAR)
ans1 = solve_part1(data, 1000)
print(f"Part 1 answer: {ans1}")
submit(ans1, part="a", day=DAY, year=YEAR)

def solve_part2(data):
    """Solve part 2: find the last connection that creates one circuit"""
    boxes = parse_input(data)
    n = len(boxes)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(boxes[i], boxes[j])
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Union-Find to track circuits
    uf = UnionFind(n)

    # Keep connecting until all in one circuit
    last_i, last_j = -1, -1
    for dist, i, j in distances:
        if uf.union(i, j):  # Only if actually connected
            last_i, last_j = i, j
            # Check if all in one circuit
            circuit_sizes = uf.get_circuit_sizes()
            if len(circuit_sizes) == 1:
                break

    # Multiply X coordinates
    x1 = boxes[last_i][0]
    x2 = boxes[last_j][0]
    return x1 * x2

assert solve_part2(example) == 25272

# Solve part 2
ans2 = solve_part2(data)
print(f"Part 2 answer: {ans2}")
submit(ans2, part="b", day=DAY, year=YEAR)
