from aocd import get_data, submit

DAY = 11
YEAR = 2025

def parse_graph(data):
    """Parse input into adjacency list graph"""
    graph = {}
    for line in data.strip().split('\n'):
        source, targets = line.split(': ')
        graph[source] = targets.split()
    return graph

def count_paths(graph, start, end, visited=None):
    """Count all paths from start to end using DFS"""
    if visited is None:
        visited = set()

    if start == end:
        return 1

    if start not in graph:
        return 0

    visited.add(start)
    total_paths = 0

    for neighbor in graph[start]:
        if neighbor not in visited:
            total_paths += count_paths(graph, neighbor, end, visited)

    visited.remove(start)  # Backtrack
    return total_paths

def count_paths_dp(graph, start, end, required_nodes):
    """
    Count paths using DP with memoization.
    State: (current_node, visited_path as bitmask, seen_required as bitmask)

    Key insight: We need to track visited nodes to avoid cycles, but
    the number of paths only depends on:
    - current position
    - which required nodes we've seen
    - which nodes are in our current path (to avoid cycles)

    Use topological order + DP for DAG, or memoization with visited tracking.
    """
    # Convert required_nodes to tuple for hashing
    required_list = list(required_nodes)
    required_idx = {n: i for i, n in enumerate(required_list)}

    # Get all nodes
    all_nodes = set(graph.keys())
    for targets in graph.values():
        all_nodes.update(targets)
    node_list = list(all_nodes)
    node_idx = {n: i for i, n in enumerate(node_list)}

    # Memoization: cache[node][required_mask] = count of paths from node to end
    # that visit the remaining required nodes
    # BUT we also need visited path... this is the challenge

    # Alternative: Use inclusion-exclusion
    # paths(svr->out through dac AND fft) =
    #   paths(svr->dac->fft->out) + paths(svr->fft->dac->out)
    # where -> means "eventually reaches"

    # Count paths: svr -> dac -> fft -> out (dac before fft)
    # + Count paths: svr -> fft -> dac -> out (fft before dac)

    # But nodes can be visited in paths between these checkpoints...
    # This is tricky because visited state matters

    # Simpler approach: memoize by (node, visited_bitmask, required_seen_mask)
    # But visited_bitmask is too large (2^600+)

    # Better: Count paths segment by segment
    # For "dac before fft": count(svr->dac) * count(dac->fft) * count(fft->out)
    # But this overcounts because paths might share nodes!

    # Actually for DAGs, we can use DP:
    # dp[node][mask] = number of paths from 'start' to 'node' that have visited
    # the required nodes indicated by 'mask'

    # Then answer = dp[end][full_mask]

    # For paths in a DAG, we do topological sort and process nodes in order
    # But this graph might have cycles? Let's check by doing DFS

    # Actually, looking at the problem: data flows from device through outputs,
    # can't flow backwards. This suggests a DAG!

    # Let's compute topological order
    from collections import deque

    # Build in-degree
    in_degree = {n: 0 for n in all_nodes}
    for src, targets in graph.items():
        for t in targets:
            in_degree[t] += 1

    # Kahn's algorithm
    queue = deque([n for n in all_nodes if in_degree[n] == 0])
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        if node in graph:
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    # DP: dp[node][mask] = number of paths from start to node with required_mask = mask
    num_required = len(required_list)
    full_mask = (1 << num_required) - 1

    # Initialize
    dp = {n: [0] * (full_mask + 1) for n in all_nodes}

    # Start node
    start_mask = 0
    
    dp[start][start_mask] = 1

    # Process in topological order
    for node in topo_order:
        if node not in graph:
            continue
        for neighbor in graph[node]:
            # Compute new mask when going to neighbor
            add_mask = 0
            if neighbor in required_idx:
                add_mask = 1 << required_idx[neighbor]

            for mask in range(full_mask + 1):
                if dp[node][mask] > 0:
                    new_mask = mask | add_mask
                    dp[neighbor][new_mask] += dp[node][mask]

    return dp[end][full_mask]

def solve_part1(data):
    graph = parse_graph(data)
    return count_paths(graph, 'you', 'out')

def solve_part2(data):
    graph = parse_graph(data)
    required = {'dac', 'fft'}
    return count_paths_dp(graph, 'svr', 'out', required)

# Test with example
example = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

test_result = solve_part1(example)
print(f"Example result: {test_result}")
assert test_result == 5, f"Expected 5, got {test_result}"

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

# Solve part 1
data = get_data(day=DAY, year=YEAR)
ans1 = solve_part1(data)
print(f"Part 1: {ans1}")

# Solve part 2
ans2 = solve_part2(data)
print(f"Part 2: {ans2}")
# submit(ans2, part="b", day=DAY, year=YEAR)
