from collections import deque, defaultdict
from functools import reduce
from utils import app
import sys
import colorama as cr

# Cost of turning 90degree: 1000
# cost of moving one step forward: 1
# Starting direction: east, that is: 1j

INF = float("inf")

DIRECTIONS = {1: "v", 1j: ">", -1j: "<", -1: "^"}
EAST = 1j
WEST = -1j
NORTH = -1
SOUTH = 1


def search_with_queue(maze, start, curdir):
    # list all the shortest paths
    all_shortest_paths = []

    # Current minimum cost
    min_cost = float("inf")

    # path_costs dictionary node -> cost
    # Default cost for all nodes is inf
    path_costs = defaultdict(lambda: float("inf")) | {(start, curdir): 0}

    # Current queue of nodes
    # (node, current_direction, cost, [path as list of nodes to get here, including the node])
    # Initialize to the start node
    queue = deque(((start, curdir, 0, [start]),))

    # We don't really know the position of the exit point yet but we will
    E = None

    while queue:
        p, curdir, cost, path = queue.pop()
        if maze[p] == "E":
            E = p
            if cost < min_cost:
                # reset all shortest paths and minimum cost
                min_cost = cost
                all_shortest_paths = [path]
            elif cost == min_cost:
                # simply add this to the list of shortest paths
                all_shortest_paths.append(path)
            continue

        # Add the neighbors to the queue
        neighbors = [
            # point, direction, cost
            (p + curdir, curdir, 1),
            (p + curdir * 1j, curdir * 1j, 1001),
            (p + curdir * -1j, curdir * -1j, 1001),
            # NEVER GO BACK!
            # (p + curdir * -1, curdir * -1, 2001),
        ]
        # Filter out walls
        neighbors = [n for n in neighbors if maze[n[0]] != "#"]

        # For each neighbor, check if the cost to get there is lower than the
        # current cost
        for n, d, c in neighbors:
            new_cost = cost + c
            # do we need strict less?
            if new_cost <= path_costs[(n, d)]:
                path_costs[(n, d)] = new_cost
                queue.append((n, d, new_cost, path + [n]))
    # print where are you coming from
    if E is None:
        raise Exception(f"Unable to solve maze.")
    return min_cost, all_shortest_paths


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
    header = []
    zeronine = "0123456789"

    if maxcol > 10:
        header.append(
            " " * 14
            + str.join("", [i * 10 for i in zeronine[1:]] + [i * 10 for i in zeronine])[
                : maxcol - 10
            ]
        )
    header.append(" " * 4 + zeronine * (maxcol // 10) + zeronine[: maxcol % 10])
    print(str.join("\n", header))
    # '    ' + '123456789' + '123456789' maxcol//10 times + maxcol%10

    for row in range(maxrow):
        print(
            f"{row:03} " + str.join("", [maze[row + col * 1j] for col in range(maxcol)])
        )


class App(app.App):
    def part_one(self):
        maze, S = parse(self.data)
        if self.debug:
            print_maze(maze)
        cost, _ = search_with_queue(maze, S, EAST)
        return cost

    def part_two(self):
        maze, S = parse(self.data)
        if self.debug:
            print_maze(maze)
        _, paths = search_with_queue(maze, S, EAST)
        restpoints = set()
        for path in paths:
            restpoints.update(path)
        for p in restpoints:
            maze[p] = "O"
        print_maze(maze)
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
# Test runs
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
# Test runs
myapp.test_one(11048, None)
myapp.test_two(64, None)

# Prod runs
myapp.test_one(None, 123540)
myapp.test_two(None, 665)

# myapp.run()
