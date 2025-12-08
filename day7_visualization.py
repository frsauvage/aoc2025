import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import defaultdict

# Example from AoC Day 7
example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

lines = example.strip().split('\n')
grid = [list(line) for line in lines]
rows = len(grid)
cols = len(grid[0])

# Find starting position
start_col = next(c for c in range(cols) if grid[0][c] == 'S')

# Run DP and track timeline counts at each row
timeline_history = []
current_row_counts = {start_col: 1}
timeline_history.append(dict(current_row_counts))

for row in range(rows):
    next_row_counts = {}

    for col, count in current_row_counts.items():
        cell = grid[row][col]

        if cell == '^':
            # Split into two timelines
            left_col = col - 1
            right_col = col + 1

            if left_col >= 0:
                next_row_counts[left_col] = next_row_counts.get(left_col, 0) + count
            if right_col < cols:
                next_row_counts[right_col] = next_row_counts.get(right_col, 0) + count
        else:
            # Continue downward
            next_row_counts[col] = next_row_counts.get(col, 0) + count

    current_row_counts = next_row_counts
    timeline_history.append(dict(current_row_counts))

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))

# Left plot: Grid with timeline propagation
ax1.set_xlim(-0.5, cols - 0.5)
ax1.set_ylim(-0.5, rows - 0.5)
ax1.invert_yaxis()
ax1.set_aspect('equal')
ax1.set_title('Timeline Propagation (DP Visualization)', fontsize=16, fontweight='bold')
ax1.set_xlabel('Column', fontsize=12)
ax1.set_ylabel('Row', fontsize=12)

# Draw grid
for row in range(rows):
    for col in range(cols):
        cell = grid[row][col]

        # Background
        if cell == 'S':
            rect = patches.Rectangle((col-0.4, row-0.4), 0.8, 0.8,
                                     linewidth=2, edgecolor='green', facecolor='lightgreen')
            ax1.add_patch(rect)
            ax1.text(col, row, 'S', ha='center', va='center',
                    fontsize=14, fontweight='bold', color='darkgreen')
        elif cell == '^':
            rect = patches.Rectangle((col-0.4, row-0.4), 0.8, 0.8,
                                     linewidth=2, edgecolor='red', facecolor='lightcoral')
            ax1.add_patch(rect)
            ax1.text(col, row, '^', ha='center', va='center',
                    fontsize=14, fontweight='bold', color='darkred')
        else:
            rect = patches.Rectangle((col-0.45, row-0.45), 0.9, 0.9,
                                     linewidth=0.5, edgecolor='gray', facecolor='white', alpha=0.3)
            ax1.add_patch(rect)

# Draw timeline counts at key rows
key_rows = [0, 2, 4, 6, 8, 10, 12, 14]
for row_idx in key_rows:
    if row_idx < len(timeline_history):
        counts = timeline_history[row_idx]
        for col, count in counts.items():
            if count > 0:
                # Draw circle with count
                circle_size = min(300 + count * 20, 800)
                ax1.scatter(col, row_idx, s=circle_size, c='blue', alpha=0.5, zorder=5)
                ax1.text(col, row_idx, str(count), ha='center', va='center',
                        fontsize=10, fontweight='bold', color='white', zorder=6)

# Add legend
ax1.text(cols + 1, 2, 'Legend:', fontsize=12, fontweight='bold')
ax1.text(cols + 1, 3, 'S = Start', fontsize=10)
ax1.text(cols + 1, 4, '^ = Splitter', fontsize=10)
ax1.text(cols + 1, 5, 'Blue circles = Timeline count', fontsize=10)

# Right plot: Timeline count evolution
ax2.set_title('Total Timelines per Row', fontsize=16, fontweight='bold')
ax2.set_xlabel('Row', fontsize=12)
ax2.set_ylabel('Number of Active Timelines', fontsize=12)
ax2.grid(True, alpha=0.3)

total_timelines_per_row = [sum(counts.values()) for counts in timeline_history]
ax2.plot(range(len(total_timelines_per_row)), total_timelines_per_row,
         marker='o', linewidth=2, markersize=8, color='blue', label='Total timelines')
ax2.fill_between(range(len(total_timelines_per_row)), total_timelines_per_row, alpha=0.3)

# Annotate final count
final_count = total_timelines_per_row[-1]
ax2.annotate(f'Final: {final_count} timelines',
            xy=(len(total_timelines_per_row)-1, final_count),
            xytext=(-50, 20), textcoords='offset points',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2))

# Add text box with DP explanation
textstr = 'DP Algorithm:\n' \
          '1. Start: 1 timeline at S\n' \
          '2. Each row: propagate timelines\n' \
          '3. Splitter (^): count × 2 (left + right)\n' \
          '4. Empty (.): continue down\n' \
          f'5. Final: {final_count} timelines exit'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax2.text(0.05, 0.95, textstr, transform=ax2.transAxes, fontsize=11,
        verticalalignment='top', bbox=props, family='monospace')

plt.tight_layout()
plt.savefig('c:/aoc2025/day7_dp_visualization.png', dpi=300, bbox_inches='tight')
print("Visualization saved to: c:/aoc2025/day7_dp_visualization.png")
print(f"Final timeline count: {final_count}")

# Create a second detailed view showing timeline merging
fig2, axes = plt.subplots(2, 2, figsize=(16, 12))

# Show timeline evolution at specific key moments
key_moments = [
    (0, "Start: Row 0\n1 timeline at position 7"),
    (2, "After 1st split: Row 2\n2 timelines (left + right)"),
    (4, "After 2nd split: Row 4\n4 → 3 timelines (merging!)"),
    (14, f"Final: Row 14\n{total_timelines_per_row[14]} timelines exit")
]

for idx, (row_num, title) in enumerate(key_moments):
    ax = axes[idx // 2, idx % 2]
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-1, 2)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Column position')
    ax.set_yticks([])

    # Draw timeline counts
    if row_num < len(timeline_history):
        counts = timeline_history[row_num]
        for col, count in counts.items():
            circle_size = 500 + count * 100
            ax.scatter(col, 0, s=circle_size, c='blue', alpha=0.6)
            ax.text(col, 0, str(count), ha='center', va='center',
                   fontsize=14, fontweight='bold', color='white')
            ax.text(col, -0.5, f'col {col}', ha='center', va='top', fontsize=9, color='gray')

    # Highlight merging in row 4
    if row_num == 4:
        ax.annotate('Merging!\n2 paths meet here',
                   xy=(7, 0), xytext=(9, 1),
                   fontsize=10, color='red', fontweight='bold',
                   arrowprops=dict(arrowstyle='->', color='red', lw=2))

plt.tight_layout()
plt.savefig('c:/aoc2025/day7_timeline_evolution.png', dpi=300, bbox_inches='tight')
print("Timeline evolution saved to: c:/aoc2025/day7_timeline_evolution.png")

# plt.show()  # Commented out to avoid blocking
print("\nVisualization complete! Check the PNG files.")
