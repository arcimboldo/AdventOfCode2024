from collections import deque, defaultdict
from functools import reduce
from utils import app
import sys
import colorama  as cr

# Cost of turning 90degree: 1000
# cost of moving one step forward: 1
# Starting direction: east, that is: 1j

INF = float("inf")
sys.setrecursionlimit(10000)

DIRECTIONS = {1: "v", 1j: ">", -1j: "<", -1: "^"}
EAST = 1j
WEST = -1j
NORTH = -1
SOUTH = 1


def search_recursive(maze, p, curdir, visited, mycost):
    neighbors = [
        # point, direction, cost
        # Same direction
        (p + curdir, curdir, 1),
        # Turning right
        (p + curdir * 1j, curdir * 1j, 1001),
        # turning left
        (p + curdir * -1j, curdir * -1j, 1001),
        # going backwards
        # (p + curdir * -1, curdir * -1, 2001),
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
            trees.append([n, c, search_recursive(maze, n, d, visited, mycost + c)])
    cost = INF
    for n, c, s in trees:
        if cost > c + s:
            cost = c + s
    return cost


def search_with_queue(maze, p, curdir):
    visited = set()
    cost = {}
    # Stores the next point, the directory we come from, and the whole path we did to get there
    queue = deque()
    queue.append((p, curdir, [(p, 0, DIRECTIONS[EAST])]))

    cost[p] = 0
    comefrom = {}
    exit_paths = []
    E = None

    breakpoint = False
    while queue:
        p, curdir, path = queue.pop()
        if maze[p] == "E":
            E = p
            exit_paths.append(path)
            continue

        # If p is the end goal, we are done
        neighbors = [
            # point, direction, cost
            (p + curdir, curdir, 1),
            (p + curdir * 1j, curdir * 1j, 1001),
            (p + curdir * -1j, curdir * -1j, 1001),
            # This is unlikely to ever happen, it means we go backwards
            # (p + curdir * -1, curdir * -1, 2001),
        ]
        # These are the neighbors I can actually visit
        neighbors = [n for n in neighbors if maze[n[0]] != "#"]
        # For each neighbor, check if the cost to get there is lower than the
        # current cost
        tmp = maze.copy()
        tmp[p] = DIRECTIONS[curdir]

        for n, d, c in neighbors:
            tmp[n] = 'n'
            if n not in cost or cost[n] >= cost[p] + c:
                cost[n] = cost[p] + c
                comefrom[n] = (p, d)
                queue.append((n, d, path + [(n, c, DIRECTIONS[d])]))
        print(cr.ansi.clear_screen(), end='')
        print_maze(tmp)
        input()
    # print where are you coming from
    if E is None:
        raise Exception(f"Unable to solve maze. comefrom: {comefrom}")
    mincost = cost[E]
    paths = []

    for p in exit_paths:
        paths.append(
            (
                list(reduce(lambda acc, x: acc + [x[0]], p, [])),
                sum([x[1] for x in p]),
                list(reduce(lambda acc, x: acc + [x[2]], p, [])),
            ),
        )
    optimal_paths = list(filter(lambda x: x[1] == mincost, paths))
    
    x = comefrom[E]
    while x:
        char = {1: "v", 1j: ">", -1j: "<", -1: "^"}
        path.append((x[0], char[x[1]]))
        x = comefrom.get(x[0], None)
    return cost[E], optimal_paths
   # return cost[E], paths


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
        cost, paths = search_with_queue(maze, S, -1j)
        return cost

    def part_two(self):
        maze, S = parse(self.data)
        if self.debug:
            print_maze(maze)
        cost, paths = search_with_queue(maze, S, -1j)
        restpoints = set()
        for path in paths:
            self.log(f'Printing path {path}')
            maze, _ = parse(self.data)
            for p in path[0]:
                maze[p] = 'O'
            print_maze(maze)
            restpoints.update(path[0])
        # for p in restpoints:
            # maze[p] = "O"
        # print_maze(maze)
        return len(restpoints)


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

# TODO: Why when X is # we don't find the path that goes all the way up first? The cost is the same!
# TEST
myapp = App(
    """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.###########.#
#.#.........#.#
###.#######.#.#
#...#.....#.#.#
#.#.#######.#.#
#.....#...#.#.#
#.#####.#.#.#.#
#S#.#.....#...#
###############
"""
)

myapp.test_one(7036, None)
myapp.test_two(45, None)
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
# myapp.test_one(11048, 123540)
# myapp.test_two(64, None)

# myapp.run()
