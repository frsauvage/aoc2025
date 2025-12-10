import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
import numpy as np
import re

# Example data
example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

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

    # Extract joltage
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage = [int(x) for x in joltage_match.group(1).split(',')]

    return target, buttons, joltage

def visualize_part1_machine(machine_idx, line):
    """Visualize Part 1: Toggle lights system"""
    target, buttons, _ = parse_machine(line)
    n_lights = len(target)
    n_buttons = len(buttons)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Button-Light mapping
    ax1.set_xlim(-0.5, n_buttons - 0.5)
    ax1.set_ylim(-0.5, n_lights - 0.5)
    ax1.set_aspect('equal')
    ax1.invert_yaxis()
    ax1.set_title(f'Machine {machine_idx + 1}: Button-Light Connections', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Buttons', fontsize=12)
    ax1.set_ylabel('Lights', fontsize=12)

    # Draw grid
    for i in range(n_lights):
        for j in range(n_buttons):
            if i in buttons[j]:
                # Button j toggles light i
                circle = plt.Circle((j, i), 0.35, color='orange', alpha=0.7)
                ax1.add_patch(circle)
                ax1.text(j, i, '⚡', ha='center', va='center', fontsize=16)
            else:
                circle = plt.Circle((j, i), 0.35, color='lightgray', alpha=0.3)
                ax1.add_patch(circle)

    # Labels
    ax1.set_xticks(range(n_buttons))
    ax1.set_xticklabels([f'B{i}\n{buttons[i]}' for i in range(n_buttons)], fontsize=9)
    ax1.set_yticks(range(n_lights))
    ax1.set_yticklabels([f'L{i}' for i in range(n_lights)], fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Right: Initial vs Target state
    ax2.set_xlim(-0.5, 1.5)
    ax2.set_ylim(-0.5, n_lights - 0.5)
    ax2.set_aspect('equal')
    ax2.invert_yaxis()
    ax2.set_title('Initial State → Target State', fontsize=14, fontweight='bold')
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['Initial\n(all OFF)', 'Target'], fontsize=11)
    ax2.set_yticks(range(n_lights))
    ax2.set_yticklabels([f'L{i}' for i in range(n_lights)], fontsize=10)

    # Draw initial state (all OFF)
    for i in range(n_lights):
        circle = plt.Circle((0, i), 0.35, color='gray', alpha=0.5)
        ax2.add_patch(circle)
        ax2.text(0, i, '○', ha='center', va='center', fontsize=20, color='black')

    # Draw target state
    for i in range(n_lights):
        if target[i] == 1:
            circle = plt.Circle((1, i), 0.35, color='yellow', alpha=0.9)
            ax2.add_patch(circle)
            ax2.text(1, i, '●', ha='center', va='center', fontsize=20, color='red')
        else:
            circle = plt.Circle((1, i), 0.35, color='gray', alpha=0.5)
            ax2.add_patch(circle)
            ax2.text(1, i, '○', ha='center', va='center', fontsize=20, color='black')

    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(f'day10_part1_machine{machine_idx + 1}.png', dpi=150, bbox_inches='tight')
    print(f"Saved: day10_part1_machine{machine_idx + 1}.png")
    plt.close()

def visualize_part2_machine(machine_idx, line):
    """Visualize Part 2: Increment counters system"""
    _, buttons, joltage = parse_machine(line)
    n_counters = len(joltage)
    n_buttons = len(buttons)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Button-Counter mapping
    ax1.set_xlim(-0.5, n_buttons - 0.5)
    ax1.set_ylim(-0.5, n_counters - 0.5)
    ax1.set_aspect('equal')
    ax1.invert_yaxis()
    ax1.set_title(f'Machine {machine_idx + 1}: Button-Counter Connections', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Buttons', fontsize=12)
    ax1.set_ylabel('Counters', fontsize=12)

    # Draw grid
    for i in range(n_counters):
        for j in range(n_buttons):
            if i in buttons[j]:
                # Button j increments counter i
                circle = plt.Circle((j, i), 0.35, color='lightgreen', alpha=0.7)
                ax1.add_patch(circle)
                ax1.text(j, i, '+1', ha='center', va='center', fontsize=12, fontweight='bold')
            else:
                circle = plt.Circle((j, i), 0.35, color='lightgray', alpha=0.3)
                ax1.add_patch(circle)

    # Labels
    ax1.set_xticks(range(n_buttons))
    ax1.set_xticklabels([f'B{i}\n{buttons[i]}' for i in range(n_buttons)], fontsize=9)
    ax1.set_yticks(range(n_counters))
    ax1.set_yticklabels([f'C{i}' for i in range(n_counters)], fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Right: Target values bar chart
    ax2.barh(range(n_counters), joltage, color='steelblue', alpha=0.7, edgecolor='black')
    ax2.set_ylim(-0.5, n_counters - 0.5)
    ax2.invert_yaxis()
    ax2.set_title('Target Joltage Values', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Joltage Level', fontsize=12)
    ax2.set_ylabel('Counter', fontsize=12)
    ax2.set_yticks(range(n_counters))
    ax2.set_yticklabels([f'C{i}' for i in range(n_counters)], fontsize=10)
    ax2.grid(True, alpha=0.3, axis='x')

    # Add value labels
    for i, val in enumerate(joltage):
        ax2.text(val + 0.3, i, str(val), va='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'day10_part2_machine{machine_idx + 1}.png', dpi=150, bbox_inches='tight')
    print(f"Saved: day10_part2_machine{machine_idx + 1}.png")
    plt.close()

def visualize_solution_process(line):
    """Visualize the solution process for machine 1"""
    target, buttons, joltage = parse_machine(line)
    n_lights = len(target)

    # Solution for Part 1: Press (0,2) and (0,1)
    solution = [(4, buttons[4]), (5, buttons[5])]  # buttons (0,2) and (0,1)

    fig, axes = plt.subplots(1, len(solution) + 2, figsize=(16, 4))

    # Initial state
    ax = axes[0]
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.5, n_lights - 0.5)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_title('Initial State\n(all OFF)', fontsize=11, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks(range(n_lights))
    ax.set_yticklabels([f'L{i}' for i in range(n_lights)], fontsize=10)

    state = [0] * n_lights
    for i in range(n_lights):
        circle = plt.Circle((0, i), 0.35, color='gray', alpha=0.5)
        ax.add_patch(circle)
        ax.text(0, i, '○', ha='center', va='center', fontsize=20, color='black')

    # Apply each button press
    for step, (btn_idx, btn_lights) in enumerate(solution):
        ax = axes[step + 1]
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(-0.5, n_lights - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.set_title(f'Press button {btn_idx}\n{btn_lights}', fontsize=11, fontweight='bold', color='blue')
        ax.set_xticks([])
        ax.set_yticks(range(n_lights))
        if step == 0:
            ax.set_yticklabels([f'L{i}' for i in range(n_lights)], fontsize=10)
        else:
            ax.set_yticklabels([])

        # Toggle lights
        for light in btn_lights:
            state[light] ^= 1

        for i in range(n_lights):
            if state[i] == 1:
                circle = plt.Circle((0, i), 0.35, color='yellow', alpha=0.9)
                ax.add_patch(circle)
                ax.text(0, i, '●', ha='center', va='center', fontsize=20, color='red')
            else:
                circle = plt.Circle((0, i), 0.35, color='gray', alpha=0.5)
                ax.add_patch(circle)
                ax.text(0, i, '○', ha='center', va='center', fontsize=20, color='black')

    # Final state
    ax = axes[-1]
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.5, n_lights - 0.5)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_title('Target State\n✓ Achieved!', fontsize=11, fontweight='bold', color='green')
    ax.set_xticks([])
    ax.set_yticks(range(n_lights))
    ax.set_yticklabels([])

    for i in range(n_lights):
        if target[i] == 1:
            circle = plt.Circle((0, i), 0.35, color='yellow', alpha=0.9)
            ax.add_patch(circle)
            ax.text(0, i, '●', ha='center', va='center', fontsize=20, color='red')
        else:
            circle = plt.Circle((0, i), 0.35, color='gray', alpha=0.5)
            ax.add_patch(circle)
            ax.text(0, i, '○', ha='center', va='center', fontsize=20, color='black')

    plt.suptitle('Part 1: Solution Process (2 button presses)', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('day10_solution_process.png', dpi=150, bbox_inches='tight')
    print("Saved: day10_solution_process.png")
    plt.close()

# Generate visualizations
lines = example.strip().split('\n')

print("Generating Part 1 visualizations...")
for i, line in enumerate(lines):
    visualize_part1_machine(i, line)

print("\nGenerating Part 2 visualizations...")
for i, line in enumerate(lines):
    visualize_part2_machine(i, line)

print("\nGenerating solution process...")
visualize_solution_process(lines[0])

print("\n✓ All visualizations generated!")
