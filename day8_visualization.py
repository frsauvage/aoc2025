import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import networkx as nx
from scipy.spatial.distance import euclidean
import numpy as np

def parse_input(data):
    """Parse junction box coordinates"""
    boxes = []
    for line in data.strip().split('\n'):
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))
    return boxes

# Test data
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

boxes = parse_input(example)
n = len(boxes)

# Calculate all pairwise distances
distances = []
for i in range(n):
    for j in range(i + 1, n):
        dist = euclidean(boxes[i], boxes[j])
        distances.append((dist, i, j))

# Sort by distance
distances.sort()

# ============================================================
# PARTIE 1: Visualisation des 10 premières connexions
# ============================================================

fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(121, projection='3d')
ax_info = fig.add_subplot(122)

# Extract coordinates
xs = [b[0] for b in boxes]
ys = [b[1] for b in boxes]
zs = [b[2] for b in boxes]

# Initialize graph
G = nx.Graph()
G.add_nodes_from(range(n))

# Colors for different circuits
colors = plt.cm.tab20(np.linspace(0, 1, 20))

def update_part1(frame):
    ax.clear()
    ax_info.clear()

    if frame > 0:
        # Add edge
        dist, i, j = distances[frame - 1]
        G.add_edge(i, j)

    # Get connected components
    components = list(nx.connected_components(G))
    component_map = {}
    for idx, comp in enumerate(components):
        for node in comp:
            component_map[node] = idx

    # Plot nodes colored by component
    for i in range(n):
        color_idx = component_map.get(i, i) % 20
        ax.scatter(boxes[i][0], boxes[i][1], boxes[i][2],
                  c=[colors[color_idx]], s=100, alpha=0.8, edgecolors='black')
        ax.text(boxes[i][0], boxes[i][1], boxes[i][2], str(i),
               fontsize=8, ha='center', va='center')

    # Plot edges
    for edge in G.edges():
        i, j = edge
        ax.plot([boxes[i][0], boxes[j][0]],
               [boxes[i][1], boxes[j][1]],
               [boxes[i][2], boxes[j][2]],
               'b-', alpha=0.3, linewidth=1)

    # Highlight last added edge
    if frame > 0:
        dist, i, j = distances[frame - 1]
        ax.plot([boxes[i][0], boxes[j][0]],
               [boxes[i][1], boxes[j][1]],
               [boxes[i][2], boxes[j][2]],
               'r-', linewidth=3, alpha=0.8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Partie 1: Connexion {frame}/10')

    # Info panel
    ax_info.axis('off')
    info_text = f"Étape {frame}/10\n\n"

    if frame > 0:
        dist, i, j = distances[frame - 1]
        info_text += f"Dernière connexion:\n"
        info_text += f"  Boîtes {i} ↔ {j}\n"
        info_text += f"  Distance: {dist:.2f}\n\n"

    # Circuit sizes
    circuit_sizes = sorted([len(c) for c in components], reverse=True)
    info_text += f"Circuits actuels: {len(components)}\n"
    info_text += f"Tailles: {circuit_sizes}\n\n"

    if frame == 10:
        product = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
        info_text += f"\nResultat:\n"
        info_text += f"3 plus grands: {circuit_sizes[0]} x {circuit_sizes[1]} x {circuit_sizes[2]}\n"
        info_text += f"= {product}"

    ax_info.text(0.1, 0.5, info_text, fontsize=12, family='monospace',
                verticalalignment='center')

# Create animation for part 1
print("Creation de l'animation pour la partie 1...")
anim1 = FuncAnimation(fig, update_part1, frames=11, interval=1000, repeat=True)
anim1.save('c:\\aoc2025\\day8_part1_animation.gif', writer=PillowWriter(fps=1))
print("Animation partie 1 sauvegardee: day8_part1_animation.gif")

plt.close()

# ============================================================
# PARTIE 2: Visualisation jusqu'a un seul circuit
# ============================================================

fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(121, projection='3d')
ax_info = fig.add_subplot(122)

# Reset graph
G2 = nx.Graph()
G2.add_nodes_from(range(n))

# Find how many connections needed for one circuit
connections_for_part2 = []
for dist, i, j in distances:
    G2.add_edge(i, j)
    connections_for_part2.append((dist, i, j))
    if nx.number_connected_components(G2) == 1:
        break

num_frames = len(connections_for_part2)

# Reset for animation
G2 = nx.Graph()
G2.add_nodes_from(range(n))

def update_part2(frame):
    ax.clear()
    ax_info.clear()

    # Add edges up to current frame
    for idx in range(frame):
        dist, i, j = connections_for_part2[idx]
        G2.add_edge(i, j)

    # Get connected components
    components = list(nx.connected_components(G2))
    component_map = {}
    for idx, comp in enumerate(components):
        for node in comp:
            component_map[node] = idx

    # Plot nodes colored by component
    for i in range(n):
        color_idx = component_map.get(i, i) % 20
        ax.scatter(boxes[i][0], boxes[i][1], boxes[i][2],
                  c=[colors[color_idx]], s=100, alpha=0.8, edgecolors='black')
        ax.text(boxes[i][0], boxes[i][1], boxes[i][2], str(i),
               fontsize=8, ha='center', va='center')

    # Plot all edges
    for edge in G2.edges():
        i, j = edge
        ax.plot([boxes[i][0], boxes[j][0]],
               [boxes[i][1], boxes[j][1]],
               [boxes[i][2], boxes[j][2]],
               'b-', alpha=0.2, linewidth=1)

    # Highlight last added edge
    if frame > 0:
        dist, i, j = connections_for_part2[frame - 1]
        ax.plot([boxes[i][0], boxes[j][0]],
               [boxes[i][1], boxes[j][1]],
               [boxes[i][2], boxes[j][2]],
               'r-', linewidth=3, alpha=0.8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Partie 2: Connexion {frame}/{num_frames}')

    # Info panel
    ax_info.axis('off')
    info_text = f"Étape {frame}/{num_frames}\n\n"

    if frame > 0:
        dist, i, j = connections_for_part2[frame - 1]
        info_text += f"Dernière connexion:\n"
        info_text += f"  Boîtes {i} ↔ {j}\n"
        info_text += f"  Distance: {dist:.2f}\n"
        info_text += f"  Coords: ({boxes[i][0]},{boxes[i][1]},{boxes[i][2]})\n"
        info_text += f"          ({boxes[j][0]},{boxes[j][1]},{boxes[j][2]})\n\n"

    # Circuit count
    num_circuits = len(components)
    info_text += f"Circuits actuels: {num_circuits}\n"

    if num_circuits == 1:
        dist, last_i, last_j = connections_for_part2[frame - 1]
        x1 = boxes[last_i][0]
        x2 = boxes[last_j][0]
        product = x1 * x2
        info_text += f"\nUN SEUL CIRCUIT!\n\n"
        info_text += f"Derniere connexion:\n"
        info_text += f"  Boites {last_i} <-> {last_j}\n"
        info_text += f"  X coords: {x1} x {x2}\n"
        info_text += f"  = {product}"

    ax_info.text(0.1, 0.5, info_text, fontsize=12, family='monospace',
                verticalalignment='center')

# Create animation for part 2
print("Creation de l'animation pour la partie 2...")
anim2 = FuncAnimation(fig, update_part2, frames=num_frames + 1, interval=500, repeat=True)
anim2.save('c:\\aoc2025\\day8_part2_animation.gif', writer=PillowWriter(fps=2))
print("Animation partie 2 sauvegardee: day8_part2_animation.gif")

plt.close()

print("\nToutes les animations ont ete creees avec succes!")
print("  - day8_part1_animation.gif: Visualise les 10 premieres connexions")
print("  - day8_part2_animation.gif: Visualise jusqu'a obtenir un seul circuit")
