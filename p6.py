from utils import download
import sys
import copy

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
def build_lab(data):
    lab = []
    for y, line in enumerate(data.strip().splitlines()):
        lab.append(list(line.strip()))
    return lab

lab = build_lab(data)

def parse_lab(lab):
    guard = None
    direction = None
    obstacles = set()
    guardpath = set()
    loops = set()
    for y in range(ymax):
        for x in range(xmax):
            c = lab[y][x]
            if c == "#":
                obstacles.add((x, y))
            elif c in directions:
                direction = directions[c]
                guard = (x, y)
                guardpath.add(guard)
                loops.add((guard, direction))
    return guard, direction, guardpath, loops

def inside_lab(pos):
    x, y = pos
    if x < 0 or x >= xmax:
        return False
    if y < 0 or y >= ymax:
        return False
    return True


def print_lab(lab):
    print(str.join("\n", [str.join("", line) for line in lab]))

def walk(lab, guard, direction, guardpath, loops):
    while inside_lab(guard):
        x, y = guard
        newx, newy = x + direction[0], y + direction[1]
        if not inside_lab((newx, newy)):
            # Exit!
            return "exited"
        if lab[newy][newx] == "#":
            direction = rotate[direction]
            lab[y][x] = rev_directions[direction]
        else:
            guard = newx, newy
            guardpath.add(guard)
            if (guard, direction) in loops:
                return "found loop"
            loops.add((guard, direction))
            lab[y][x] = 'X'
            if inside_lab((newx, newy)):
                lab[newy][newx] = rev_directions[direction]

# print_lab(lab)
newlab = copy.deepcopy(lab)
guard, direction, guardpath, loops = parse_lab(lab)

walk(newlab, guard, direction, guardpath, loops)
print(f"Part one: exited after {len(guardpath)} steps")
# 41 for test
# 4663 for prod

# Is it loop?
lab = build_lab(data)

good_obstructions = set()
# for pos in guardpath:
guardpath.remove(guard)
for pos in guardpath:
    newlab = copy.deepcopy(lab)
    newlab[pos[1]][pos[0]] = "#"
    guard, direction, curguardpath, loops = parse_lab(newlab)
    ret = walk(newlab, guard, direction, curguardpath, loops)
    if ret == "found loop":
        good_obstructions.add(pos)

print(f'Path two: num good obstructions: {len(good_obstructions)}')