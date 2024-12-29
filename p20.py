from utils import app
from collections import deque, defaultdict
import heapq


def dfs(maze, start, end):
    q = deque()
    q.append(start)
    previous = {}

    while q:
        x, y = p = q.popleft()
        # find neighbors
        if maze[p] == end:
            break
        for n in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if maze.get(n, "#") != "#" and n not in previous:
                q.append(n)
                previous[n] = p
    path = []

    p = end
    while p != start:
        path.append(p)
        p = previous[p]
    return list(reversed(path))

def find_track(maze, start, end):
    path = [start]
    # micro optimization
    paset = set()
    p = start
    oldp = p
    while p != end:
        x,y = p
        if p == end:
            break
        for n in [(x+1, y), (x-1, y), (x,y+1), (x,y-1)]:
            if n == end or (maze.get(n) == '.' and n not in paset):
                path.append(n)
                paset.add(n)
                p = n
                break
    return path

def find_cheats(maze, path, save_at_least, max_cheat=1):
    count = 0
    for si, s in enumerate(path):
        for ei, e in enumerate(path[si+1:]):
            d = abs(e[0]-s[0]) + abs(e[1]-s[1])
            if d <=  max_cheat and abs(ei-si)-d >= save_at_least:
                count += 1
    return count

def find_cheat(maze, path, save_at_least, max_cheat=1):
    start, end = path[0], path[-1]
    cost = len(path)
    shorter = []

    # For each p in path, find the points that are less or equal than max_cheat distant, distance computed as:
    # distance(a, b) = abs(b[0]-a[0]) + abs(b[1]-a[1])
    # also known as manhattan distance
    # Then check the length of the new path and see if it saves at least save_at_least
    for i, p in enumerate(path):
        # find shortcuts that save 100 picoseconds
        x, y = p

        # p is our start node. For each point in path that is at least
        # save_at_least away (the steps we want to save), find a path that is
        # *only* within the whall, and is max_cheat long.
        #
        # Use 

        q = deque()
        q.append((p, p, 0))
        while q:
            p, lastp, c = q.popleft()
            for n in [
                (x+2, y),
                (x-2, y),
                (x, y+2),
                (x, y-2),
            ]:
                if c >= 20:
                    continue
                if maze[n] == '#':
                    q.append((n, lastp, c+1))
                elif n in path:
                    # measure the shortened path
                    newpath = path[:path.index(lastp)] + path[path.index(n):]
                    newcost = len(newpath)+c
                    # -1 because cheating cost one extra picosecond
                    if newcost <= cost-save_at_least-1:
                        shorter.append(newpath)
                

                    
    return shorter

def create_maze(data):
    maze = {}
    start = None
    end = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            maze[(x, y)] = c
            if c == "S":
                start = (x, y)
            elif c == "E":
                end = (x, y)
    return maze, start, end, len(data.splitlines()), len(data.splitlines()[0].strip())


def print_maze(maze, xmax, ymax):
    for y in range(ymax):
        print(str.join("", [maze[(y, x)] for x in range(xmax)]))


class App(app.App):
    def part_one(self):
        maze, start, end, xmax, ymax = create_maze(self.data)

        path = find_track(maze, start, end)

        count = find_cheats(maze, path, 100 if self.prod else 10, 2)
        return count

    def part_two(self):
        maze, start, end, xmax, ymax = create_maze(self.data)
        path = find_track(maze, start, end)
        count = find_cheats(maze, path, 100 if self.prod else 50, 20)
        return count


myapp = App(
    """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
)
myapp.test_one(10, 1521)
# 1192423 too high
# 1056371 too high
# Myst beL 1013106
myapp.test_two(285, 1013106)
myapp.run()
