from aocd import get_data, submit

DAY = 9
YEAR = 2025


# determine boundaries formed by the red/green tiles
def get_boundaries(red_tiles):
    boundaries = {}
    for i in range(len(red_tiles)):
        tile1 = red_tiles[i]
        tile2 = red_tiles[(i + 1) % len(red_tiles)]
        x1, y1 = tile1
        x2, y2 = tile2

        # vertical edge
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if y not in boundaries:
                    boundaries[y] = [x1, x1]
                else:
                    boundaries[y][0] = min(boundaries[y][0], x1)
                    boundaries[y][1] = max(boundaries[y][1], x1)

        # horizontal edge
        elif y1 == y2:
            if y1 not in boundaries:
                boundaries[y1] = [min(x1, x2), max(x1, x2)]
            else:
                boundaries[y1][0] = min(boundaries[y1][0], x1, x2)
                boundaries[y1][1] = max(boundaries[y1][1], x1, x2)
    return boundaries

# checks if a rectangle is within the boundaries
def is_rectangle_valid(tile1, tile2, boundaries):
    min_x = min(tile1[0], tile2[0])
    max_x = max(tile1[0], tile2[0])
    min_y = min(tile1[1], tile2[1])
    max_y = max(tile1[1], tile2[1])

    for y in range(min_y, max_y + 1):
        if y not in boundaries:
            return False
        bound_min_x, bound_max_x = boundaries[y]
        if min_x < bound_min_x or max_x > bound_max_x:
            return False
    return True

def find_max_area(red_tiles, boundaries):
    max_area = 0
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            if is_rectangle_valid(red_tiles[i], red_tiles[j], boundaries):
                area = calculate_area(red_tiles[i], red_tiles[j])
                if area > max_area:
                    max_area = area
    return max_area

def calculate_area(tile1, tile2):
    x_dist = abs(tile1[0] - tile2[0])
    y_dist = abs(tile1[1] - tile2[1])
    return (x_dist + 1) * (y_dist + 1)

if __name__ == "__main__":

    # Fetch input from AoC
    data = get_data(day=DAY, year=YEAR)
    red_tiles = []
    for line in data.strip().splitlines():
        x, y = map(int, line.strip().split(","))
        red_tiles.append((x, y))

    # Part 2: largest rectangle using red and green tiles
    boundaries = get_boundaries(red_tiles)
    max_area_part2 = find_max_area(red_tiles, boundaries)
    print("Part 2:", max_area_part2)
    submit(max_area_part2, part="b", day=DAY, year=YEAR)
