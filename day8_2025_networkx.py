from aocd import get_data, submit
import networkx as nx
from scipy.spatial.distance import euclidean

DAY = 8
YEAR = 2025

def parse_input(data):
    """Parse junction box coordinates"""
    boxes = []
    for line in data.strip().split('\n'):
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))
    return boxes

def solve_part1(data, num_pairs):
    """Solve part 1: connect closest pairs and find three largest circuits"""
    boxes = parse_input(data)
    n = len(boxes)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean(boxes[i], boxes[j])
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Create graph and add closest edges
    G = nx.Graph()
    G.add_nodes_from(range(n))

    for idx in range(num_pairs):
        dist, i, j = distances[idx]
        G.add_edge(i, j)

    # Get connected components (circuits) and their sizes
    circuit_sizes = sorted([len(c) for c in nx.connected_components(G)], reverse=True)

    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

def solve_part2(data):
    """Solve part 2: find the last connection that creates one circuit"""
    boxes = parse_input(data)
    n = len(boxes)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean(boxes[i], boxes[j])
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Create graph
    G = nx.Graph()
    G.add_nodes_from(range(n))

    # Keep connecting until all in one circuit
    last_i, last_j = -1, -1
    for dist, i, j in distances:
        G.add_edge(i, j)
        last_i, last_j = i, j

        # Check if all in one circuit (one connected component)
        if nx.number_connected_components(G) == 1:
            break

    # Multiply X coordinates
    x1 = boxes[last_i][0]
    x2 = boxes[last_j][0]
    return x1 * x2

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

assert solve_part2(example) == 25272

# Solve part 2
ans2 = solve_part2(data)
print(f"Part 2 answer: {ans2}")
submit(ans2, part="b", day=DAY, year=YEAR)
