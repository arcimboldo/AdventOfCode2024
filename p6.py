from utils import download
import sys

if "prod" in sys.argv:
    data = download.read(6)
else:
    data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


# Find the coordinates of the obstacles
# find the coordinate of the guard
# fill the visited coordinates

guardpath = set()
guard = None
direction = None
obstacles = set()
xmax = len(data.splitlines()[0].strip())
ymax = len(data.strip().splitlines())

# Note: y directions are inverted: negative means up, positive means down
directions = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}
rev_directions = {v:k for k,v in directions.items()}

rotate = {
    # up -> right
    (0, -1): (1, 0),
    # right -> down
    (1, 0): (0, 1),
    # down -> left
    (0, 1): (-1, 0),
    # left -> up
    (-1, 0): (0, -1),
}

lab = []
for y, line in enumerate(data.strip().splitlines()):
    lab.append(list(line.strip()))

for y in range(ymax):
    for x in range(xmax):
        c = lab[y][x]
        if c == "#":
            obstacles.add((x, y))
        elif c in directions:
            direction = directions[c]
            guard = (x, y)
            guardpath.add(guard)


def inside_lab(pos):
    x, y = pos
    if x < 0 or x >= xmax:
        return False
    if y < 0 or y >= ymax:
        return False
    return True


def print_lab(lab):
    print(str.join("\n", [str.join("", line) for line in lab]))


while inside_lab(guard):
    x, y = guard
    newx, newy = x + direction[0], y + direction[1]
    if not inside_lab((newx, newy)):
        # Exit!
        break
    if lab[newy][newx] == "#":
        direction = rotate[direction]
        lab[y][x] = rev_directions[direction]
    else:
        guard = newx, newy
        guardpath.add(guard)
        lab[y][x] = 'X'
        if inside_lab((newx, newy)):
            lab[newy][newx] = rev_directions[direction]

print(f"Part one: exited after {len(guardpath)} steps")
print_lab(lab)
