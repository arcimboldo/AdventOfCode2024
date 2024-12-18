from collections import deque
from utils import app
import sys

# Cost of turning 90degree: 1000
# cost of moving one step forward: 1
# Starting direction: east, that is: 1j

INF = float("inf")
sys.setrecursionlimit(10000)


def search(maze, p, curdir, visited, mycost):
    neighbors = [
        # point, direction, cost
        (p + curdir, curdir, 1),
        (p + curdir * 1j, curdir * 1j, 1001),
        (p + curdir * -1j, curdir * -1j, 1001),
        (p + curdir * -1, curdir * -1, 2001),
    ]
    neighbors = [n for n in neighbors if maze[n[0]] != "#"]
    visited[p] = mycost
    trees = []  # next point, cost of next point, result of the search
    for n, d, c in neighbors:
        if n in visited and visited[n] < c + mycost:
            continue
        if maze[n] == "E":
            trees.append([n, c, 0])
        elif maze[n] == ".":
            trees.append([n, c, search(maze, n, d, visited, mycost + c)])
    cost = INF
    for n, c, s in trees:
        if cost > c + s:
            cost = c + s
    return cost


def search2(maze, p, curdir):
    visited = set()
    cost = {}
    queue = deque()
    queue.append((p, curdir))

    cost[p] = 0
    comefrom = {}

    E = None
    while queue:
        p, curdir = queue.pop()
        if maze[p] == "E":
            E = p

        # If p is the end goal, we are done
        neighbors = [
            # point, direction, cost
            (p + curdir, curdir, 1),
            (p + curdir * 1j, curdir * 1j, 1001),
            (p + curdir * -1j, curdir * -1j, 1001),
            # This is unlikely to ever happen, it means we go backwards
            (p + curdir * -1, curdir * -1, 2001),
        ]
        # These are the neighbors I can actually visit
        neighbors = [n for n in neighbors if maze[n[0]] != "#"]
        # For each neighbor, check if the cost to get there is lower than the
        # current cost
        for n, d, c in neighbors:
            if n not in cost or cost[n] >= cost[p] + c:
                cost[n] = cost[p] + c
                comefrom[n] = (p, d)
                queue.append((n, d))
    # print where are you coming from
    if E is None:
        raise Exception(f"Unable to solve maze. comefrom: {comefrom}")
    path = []
    x = comefrom[E]
    while x:
        char = {1: "v", 1j: ">", -1j: "<", -1: "^"}
        path.append((x[0], char[x[1]]))
        x = comefrom.get(x[0], None)
    return cost[E], path


def parse(data):
    maze = {}
    S = 0
    for row, line in enumerate(data.splitlines()):
        for col, c in enumerate(line.strip()):
            maze[row + col * 1j] = c
            if c == "S":
                S = row + col * 1j
    return maze, S


def print_maze(maze):
    maxrow = int(max(i.real for i in maze)) + 1
    maxcol = int(max(i.imag for i in maze)) + 1
    for row in range(maxrow):
        print(
            f"{row:02} " + str.join("", [maze[row + col * 1j] for col in range(maxcol)])
        )


class App(app.App):
    def part_one(self):
        maze, S = parse(self.data)
        if self.debug:
            print_maze(maze)
        cost, path = search2(maze, S, -1j)
        for p in path:
            maze[p[0]] = p[1]
        if self.debug:
            print_maze(maze)
        return cost

    def part_two(self):
        pass


myapp = App(
    """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
)

myapp.test_one(7036, None)

myapp = App(
    """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""
)
myapp.test_one(11048, 123540)


myapp.run()
