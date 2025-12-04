"""
Advent of Code 2025 - Day 4: Visual Demonstration with Matplotlib
Beautiful graphical visualization of the removal process.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
import numpy as np
from aocd import get_data

DIRECTIONS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def parse_rolls(data):
    """Parse grid and extract all paper roll positions."""
    lines = data.strip().split('\n')
    return {(r, c) for r, line in enumerate(lines)
            for c, char in enumerate(line) if char == '@'}

def count_neighbors(pos, rolls):
    """Count how many neighbors a position has."""
    r, c = pos
    return sum(1 for dr, dc in DIRECTIONS if (r + dr, c + dc) in rolls)

def find_accessible(rolls):
    """Find all rolls with fewer than 4 neighbors."""
    return {pos for pos in rolls if count_neighbors(pos, rolls) < 4}

def create_grid_image(rolls, accessible, removed, rows, cols):
    """
    Create a color-coded grid image.

    Colors:
    - White (0): Empty space
    - Dark gray (1): Normal roll (>= 4 neighbors)
    - Yellow (2): Accessible roll (< 4 neighbors)
    - Light gray (3): Just removed
    """
    grid = np.zeros((rows, cols))

    for r in range(rows):
        for c in range(cols):
            pos = (r, c)
            if removed and pos in removed:
                grid[r, c] = 3  # Just removed
            elif accessible and pos in accessible:
                grid[r, c] = 2  # Accessible
            elif pos in rolls:
                grid[r, c] = 1  # Normal roll
            else:
                grid[r, c] = 0  # Empty

    return grid

def visualize_static(data, save_path='day4_visualization.png'):
    """Create static visualization showing Part 1 and final state of Part 2."""
    rolls_initial = parse_rolls(data)
    lines = data.strip().split('\n')
    rows, cols = len(lines), len(lines[0])

    # Part 1: Initial state
    accessible_part1 = find_accessible(rolls_initial)

    # Part 2: Simulate to get final state
    rolls_part2 = rolls_initial.copy()
    rounds = []

    while True:
        accessible = find_accessible(rolls_part2)
        if not accessible:
            break
        rounds.append((rolls_part2.copy(), accessible))
        rolls_part2 -= accessible

    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Advent of Code 2025 - Day 4: Paper Roll Accessibility',
                 fontsize=16, fontweight='bold')

    # Custom colormap
    colors = ['white', 'darkgray', 'gold', 'lightgray']
    cmap = plt.matplotlib.colors.ListedColormap(colors)

    # Part 1: Initial state with accessible highlighted
    ax1 = axes[0, 0]
    grid1 = create_grid_image(rolls_initial, accessible_part1, None, rows, cols)
    im1 = ax1.imshow(grid1, cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
    ax1.set_title(f'Part 1: Initial State\n{len(accessible_part1)} accessible rolls', fontweight='bold')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.grid(True, which='both', color='black', linewidth=0.5, alpha=0.3)

    # Add neighbor count overlay
    for r in range(rows):
        for c in range(cols):
            if (r, c) in rolls_initial:
                neighbors = count_neighbors((r, c), rolls_initial)
                color = 'white' if neighbors >= 4 else 'black'
                ax1.text(c, r, str(neighbors), ha='center', va='center',
                        fontsize=8, color=color, fontweight='bold')

    # Part 2: Show first 2 rounds
    for i, (rolls, accessible) in enumerate(rounds[:2]):
        ax = axes[0, i+1]
        grid = create_grid_image(rolls, accessible, None, rows, cols)
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
        ax.set_title(f'Round {i+1}\nRemoving {len(accessible)} rolls', fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(True, which='both', color='black', linewidth=0.5, alpha=0.3)

    # Final state
    ax_final = axes[1, 0]
    grid_final = create_grid_image(rolls_part2, None, None, rows, cols)
    ax_final.imshow(grid_final, cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
    ax_final.set_title(f'Final State\n{len(rolls_part2)} rolls remain', fontweight='bold')
    ax_final.set_xticks([])
    ax_final.set_yticks([])
    ax_final.grid(True, which='both', color='black', linewidth=0.5, alpha=0.3)

    # Add neighbor count overlay for final
    for r in range(rows):
        for c in range(cols):
            if (r, c) in rolls_part2:
                neighbors = count_neighbors((r, c), rolls_part2)
                ax_final.text(c, r, str(neighbors), ha='center', va='center',
                            fontsize=8, color='white', fontweight='bold')

    # Statistics
    ax_stats = axes[1, 1]
    ax_stats.axis('off')

    total_removed = len(rolls_initial) - len(rolls_part2)
    stats_text = f"""
    STATISTICS
    ═══════════════════════

    Part 1:
      • Total rolls: {len(rolls_initial)}
      • Accessible: {len(accessible_part1)}
      • Percentage: {len(accessible_part1)/len(rolls_initial)*100:.1f}%

    Part 2:
      • Total rounds: {len(rounds)}
      • Total removed: {total_removed}
      • Remaining: {len(rolls_part2)}
      • Removal rate: {total_removed/len(rolls_initial)*100:.1f}%

    Removal per round:
    """

    for i, (_, accessible) in enumerate(rounds, 1):
        stats_text += f"\n      Round {i}: {len(accessible)} rolls"

    ax_stats.text(0.1, 0.95, stats_text, transform=ax_stats.transAxes,
                 fontsize=10, verticalalignment='top', fontfamily='monospace')

    # Legend
    ax_legend = axes[1, 2]
    ax_legend.axis('off')

    legend_elements = [
        mpatches.Patch(facecolor='white', edgecolor='black', label='Empty space'),
        mpatches.Patch(facecolor='darkgray', label='Roll (≥4 neighbors)'),
        mpatches.Patch(facecolor='gold', label='Accessible (< 4 neighbors)'),
        mpatches.Patch(facecolor='lightgray', label='Just removed')
    ]

    ax_legend.legend(handles=legend_elements, loc='center', fontsize=12,
                    title='Legend', title_fontsize=14)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"[OK] Visualization saved to {save_path}")
    plt.close()

def visualize_heatmap(data, save_path='day4_heatmap.png'):
    """Create neighbor count heatmap."""
    rolls = parse_rolls(data)
    lines = data.strip().split('\n')
    rows, cols = len(lines), len(lines[0])

    # Create neighbor count grid
    neighbor_grid = np.full((rows, cols), -1.0)  # -1 for empty

    for r in range(rows):
        for c in range(cols):
            if (r, c) in rolls:
                neighbor_grid[r, c] = count_neighbors((r, c), rolls)

    fig, ax = plt.subplots(figsize=(12, 10))

    # Create custom colormap: white for -1, viridis for 0-8
    cmap = plt.cm.get_cmap('RdYlGn_r', 9)
    cmap.set_under('white')

    im = ax.imshow(neighbor_grid, cmap=cmap, vmin=0, vmax=8, interpolation='nearest')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, ticks=range(9))
    cbar.set_label('Number of Neighbors', rotation=270, labelpad=20, fontsize=12)

    # Add text annotations
    for r in range(rows):
        for c in range(cols):
            if (r, c) in rolls:
                neighbors = int(neighbor_grid[r, c])
                color = 'white' if neighbors >= 5 else 'black'
                ax.text(c, r, str(neighbors), ha='center', va='center',
                       fontsize=9, color=color, fontweight='bold')

    ax.set_title('Paper Roll Neighbor Count Heatmap\n(Accessible rolls have < 4 neighbors)',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(True, which='both', color='black', linewidth=0.5, alpha=0.2)

    # Add threshold line indicator
    accessible = find_accessible(rolls)
    ax.text(0.02, 0.98, f'Accessible rolls (< 4 neighbors): {len(accessible)}',
           transform=ax.transAxes, fontsize=12, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='gold', alpha=0.8))

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"[OK] Heatmap saved to {save_path}")
    plt.close()

def visualize_progression(data, save_path='day4_progression.png'):
    """Show the progression of removal rounds."""
    rolls = parse_rolls(data)
    lines = data.strip().split('\n')
    rows, cols = len(lines), len(lines[0])

    # Simulate and collect all rounds
    rounds_data = []
    current_rolls = rolls.copy()

    while True:
        accessible = find_accessible(current_rolls)
        if not accessible:
            break
        rounds_data.append((current_rolls.copy(), accessible))
        current_rolls -= accessible

    # Show up to 9 rounds
    num_rounds = min(len(rounds_data), 9)

    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    fig.suptitle('Paper Roll Removal Progression', fontsize=16, fontweight='bold')

    colors = ['white', 'darkgray', 'gold', 'lightgray']
    cmap = plt.matplotlib.colors.ListedColormap(colors)

    for i in range(9):
        ax = axes[i // 3, i % 3]

        if i < num_rounds:
            rolls_state, accessible = rounds_data[i]
            grid = create_grid_image(rolls_state, accessible, None, rows, cols)
            ax.imshow(grid, cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
            ax.set_title(f'Round {i+1}\n{len(rolls_state)} total, {len(accessible)} accessible',
                        fontweight='bold')
        else:
            ax.axis('off')
            if i == num_rounds:
                # Show final state
                grid = create_grid_image(current_rolls, None, None, rows, cols)
                ax.imshow(grid, cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
                ax.set_title(f'Final State\n{len(current_rolls)} rolls remain',
                           fontweight='bold')
                ax.axis('on')

        ax.set_xticks([])
        ax.set_yticks([])
        if ax.axison:
            ax.grid(True, which='both', color='black', linewidth=0.5, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"[OK] Progression saved to {save_path}")
    plt.close()

if __name__ == "__main__":
    # Use example data
    example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

    print("ADVENT OF CODE 2025 - DAY 4")
    print("Matplotlib Visualization\n")

    print("Generating visualizations...")
    print()

    # Generate all visualizations
    visualize_static(example, 'day4_visualization.png')
    visualize_heatmap(example, 'day4_heatmap.png')
    visualize_progression(example, 'day4_progression.png')

    print("\n[OK] All visualizations complete!")
    print("\nGenerated files:")
    print("  - day4_visualization.png - Overview with statistics")
    print("  - day4_heatmap.png - Neighbor count heatmap")
    print("  - day4_progression.png - Round-by-round progression")
