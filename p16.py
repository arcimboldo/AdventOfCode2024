from collections import deque, defaultdict
from functools import reduce
from utils import app
import sys
import colorama  as cr

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
    min_cost = float('inf')

    # path_costs dictionary node -> cost    
    # Default cost for all nodes is inf
    path_costs = defaultdict(lambda: float('inf')) | {start:0}

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
            new_cost = cost+c
            # do we need strict less?
            if new_cost <= path_costs[n]:
                path_costs[n] = new_cost
                queue.append((n, d, new_cost, path+[n]))
    # print where are you coming from
    if E is None:
        raise Exception(f"Unable to solve maze.")
    return min_cost, all_shortest_paths
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

# OK TEST run of part_one: 7036
# 00 ###############
# 01 #.......#....O#
# 02 #.#.###.#.###O#
# 03 #.....#.#...#O#
# 04 #.###.#####.#O#
# 05 #.#.#.......#O#
# 06 #.#.#####.###O#
# 07 #..OOOOOOOOO#O#
# 08 ###O#O#####O#O#
# 09 #..O#O....#O#O#
# 10 #.#O#O###.#O#O#
# 11 #OOOOO#...#O#O#
# 12 #O###.#.#.#O#O#
# 13 #O..#.....#OOO#
# 14 ###############
# ERROR: TEST run of part_two: got 42, expected 45 instead
#
# ARGH! It's missing path 13+1j -> 12+1j -> 11+1j -> 10+1j -> 9+1j -> 9+2j -> ...

# myapp.test_one(7036, None)
myapp.test_two(45, None)
# myapp = App(
#     """
# #################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################
# """
# )
# myapp.test_one(11048, 123540)
# myapp.test_two(64, 665)

# myapp.run()
