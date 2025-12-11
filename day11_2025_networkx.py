"""
AoC 2025 Day 11 - Reactor (Solution avec NetworkX)

Problème: Trouver tous les chemins de données entre devices dans un réacteur.
- Part 1: Compter les chemins de 'you' vers 'out' (reactor output)
- Part 2: Compter les chemins de 'svr' (server rack) vers 'out'
          passant par 'dac' (digital-to-analog converter) ET 'fft' (fast Fourier transform)

Note: NetworkX n'a pas de fonction pour COMPTER les chemins sans les énumérer.
      nx.all_simple_paths() génère chaque chemin (inutilisable pour 306 trillions de chemins).
      On utilise donc nx.topological_sort() + DP maison pour compter en O(V+E).
"""
from aocd import get_data
import networkx as nx
from collections import defaultdict

DAY = 11
YEAR = 2025

# Devices spéciaux du problème
YOU = 'you'              # Device de départ (part 1)
SERVER_RACK = 'svr'      # Server rack (part 2)
REACTOR_OUTPUT = 'out'   # Sortie principale du réacteur
DAC = 'dac'              # Digital-to-analog converter
FFT = 'fft'              # Fast Fourier transform


def parse_devices(data):
    """Parse la liste des devices et leurs connexions en graphe dirigé"""
    devices = nx.DiGraph()
    for line in data.strip().split('\n'):
        device, outputs = line.split(': ')
        for output in outputs.split():
            devices.add_edge(device, output)
    return devices


# def count_data_paths(devices, from_device, to_device):
#     """Compte tous les chemins de données entre deux devices (DP sur DAG)"""
#     if from_device not in devices or to_device not in devices:
#         return 0

#     # Ordre topologique (les données ne remontent jamais)
#     data_flow_order = list(nx.topological_sort(devices))

#     # nb_paths[device] = nombre de chemins depuis from_device
#     nb_paths = defaultdict(int)
#     nb_paths[from_device] = 1

#     for device in data_flow_order:
#         if nb_paths[device] > 0:
#             for output in devices.successors(device):
#                 nb_paths[output] += nb_paths[device]

#     return nb_paths[to_device]


def count_data_paths_through(devices, from_device, to_device, must_visit):
    """
    Compte les chemins de données passant par TOUS les devices requis.

    État DP: nb_paths[device][devices_vus] = nombre de chemins

    Exemple avec must_visit = {'dac', 'fft'}:
        nb_paths['svr'][frozenset()] = 1              # départ du server rack
        nb_paths['fft'][frozenset({'fft'})] = 5      # 5 chemins ayant traversé fft
        nb_paths['out'][frozenset({'dac','fft'})] = 42  # chemins valides vers reactor
    """
    if from_device not in devices or to_device not in devices:
        return 0

    must_visit = frozenset(must_visit)

    # Tous les sous-ensembles possibles de devices à visiter
    # Ex: {'dac', 'fft'} -> [set(), {'dac'}, {'fft'}, {'dac', 'fft'}]
    from itertools import combinations
    visit_states = [
        frozenset(subset)
        for size in range(len(must_visit) + 1)
        for subset in combinations(must_visit, size)
    ]

    # Ordre topologique
    data_flow_order = list(nx.topological_sort(devices))

    # nb_paths[device][devices_déjà_vus] = nombre de chemins
    nb_paths = defaultdict(lambda: defaultdict(int))

    # Initialisation depuis le device de départ
    initial_visited = must_visit.intersection({from_device})
    nb_paths[from_device][initial_visited] = 1

    # Propagation dans l'ordre du flux de données
    for device in data_flow_order:
        for visited in visit_states:
            path_count = nb_paths[device][visited]
            if path_count > 0:
                for output in devices.successors(device):
                    # Mise à jour des devices requis traversés
                    new_visited = visited.union(must_visit.intersection({output}))
                    nb_paths[output][new_visited] += path_count

    # Chemins atteignant la sortie ayant visité TOUS les devices requis
    return nb_paths[to_device][must_visit]


def solve_part1(data):
    """Compte les chemins de 'you' vers la sortie du réacteur"""
    devices = parse_devices(data)
    # Part 1: seulement 574 chemins, on peut utiliser all_simple_paths
    # return count_data_paths(devices, YOU, REACTOR_OUTPUT)
    return sum(1 for _ in nx.all_simple_paths(devices, YOU, REACTOR_OUTPUT))


def solve_part2(data):
    """Compte les chemins du server rack vers le réacteur passant par dac ET fft"""
    devices = parse_devices(data)
    return count_data_paths_through(devices, SERVER_RACK, REACTOR_OUTPUT, {DAC, FFT})


if __name__ == "__main__":
    # Test Part 1
    example1 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

    assert solve_part1(example1) == 5, "Part 1 example failed"
    print("Part 1 example: OK")

    # Test Part 2
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

    assert solve_part2(example2) == 2, "Part 2 example failed"
    print("Part 2 example: OK")

    # Solve
    data = get_data(day=DAY, year=YEAR)

    ans1 = solve_part1(data)
    print(f"Part 1: {ans1}")

    ans2 = solve_part2(data)
    print(f"Part 2: {ans2}")
