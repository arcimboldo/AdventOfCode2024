from utils import app
from matplotlib import pyplot as plt
from itertools import chain
import sys


WALL = "#"
BOX = "O"
ROBOT = "@"


def parse(data, conv_func=lambda x: x):
    floorplan = []
    directions = ""

    floorplan = [
        list(str.join("", [conv_func(x) for x in line]))
        for line in data.splitlines()
        if WALL in line
    ]
    directions = str.join(
        "",
        [line.strip() for line in data.splitlines() if set(line).intersection("<>^v")],
    )
    robot = (-1, -1)
    for i, line in enumerate(floorplan):
        for j, c in enumerate(line):
            if c == ROBOT:
                robot = (i, j)
                break
        if robot != (-1, -1):
            break

    return floorplan, directions, robot


def parse2(data):
    def conv(x):
        return {
            ".": "..",
            BOX: "[]",
            WALL: WALL * 2,
            ROBOT: ROBOT + ".",
        }[x]

    return parse(data, conv_func=conv)


def cost(floorplan):
    # Cost of a box is:
    # 100 * distance from top edge + distance from left edge
    cost = 0
    return sum(
        (100 * i + j)
        for i, line in enumerate(floorplan)
        for j, c in enumerate(line)
        if c in (BOX, "[")
    )
    # for i, line in enumerate(floorplan):
    #     for j, c in enumerate(line):
    #         if c == BOX:
    #             cost += (100 * i + j)
    # return cost


def move(floorplan, r, d):
    """Move the robot"""
    dr, dc = 0, 0
    match d:
        case "<":
            dc = -1
        case ">":
            dc = +1
        case "^":
            dr = -1
        case "v":
            dr = +1

    if dr == 0:
        # move left/right
        line = floorplan[r[0]]
        for i in range(r[1], 0 if dc == -1 else len(line), dc):
            if line[i] == "#":
                break
            if line[i] == ".":
                for j in range(i, r[1], -dc):
                    line[j] = line[j - dc]
                line[r[1]] = "."
                return floorplan, (r[0] + dr, r[1] + dc)
    else:
        # Move up/down
        i = first_empty_space(floorplan, r[1], r[0], dr)
        if i != -1:
            move_vertically(floorplan, r[1], r[0], dr)
            return floorplan, (r[0] + dr, r[1])
    return floorplan, (r[0], r[1])


def first_empty_space(floorplan, col, start, direction):
    """Find the first empty space of a column col, starting from start.

    Returns the index of the empty space or -1 if we cannot move this column."""
    for j in range(start, 0 if direction < 0 else len(floorplan), direction):
        if floorplan[j][col] == "[":
            left, right = (
                first_empty_space(floorplan, col, j + direction, direction),
                first_empty_space(floorplan, col + 1, j + direction, direction),
            )
            if -1 in (left, right):
                return -1
            if direction < 0:  # going up
                return max(left, right)
            else:
                return min(left, right)
        elif floorplan[j][col] == "]":
            left, right = (
                first_empty_space(floorplan, col, j + direction, direction),
                first_empty_space(floorplan, col - 1, j + direction, direction),
            )
            if -1 in (left, right):
                return -1
            if direction < 0:  # going up
                return max(left, right)
            else:
                return min(left, right)
        elif floorplan[j][col] == ".":
            return j
        elif floorplan[j][col] == "#":
            return -1
    return -1


def move_vertically(floorplan, col, row, direction):
    # We move this piece if we can, otherwise we move first whatever we can move
    next = floorplan[row + direction][col]
    if next == ".":
        # Good, let's just move
        floorplan[row + direction][col] = floorplan[row][col]
        # Let's put an empty space, it might be overwritten by the caller if necessary
        floorplan[row][col] = "."
    elif next == "O":
        move_vertically(floorplan, col, row + direction, direction)
        floorplan[row + direction][col] = floorplan[row][col]
        floorplan[row][col] = "."
    elif next == "[":
        # Move the next and the one to the right of the next
        move_vertically(floorplan, col, row + direction, direction)
        move_vertically(floorplan, col + 1, row + direction, direction)
        floorplan[row + direction][col] = floorplan[row][col]
        floorplan[row][col] = "."
    elif next == "]":
        # Move the next and the one to the left of the next
        move_vertically(floorplan, col, row + direction, direction)
        move_vertically(floorplan, col - 1, row + direction, direction)
        floorplan[row + direction][col] = floorplan[row][col]
        floorplan[row][col] = "."
    return


def print_map(floorplan):
    for i, line in enumerate(floorplan):
        print(str.join("", line))


class App(app.App):
    def part_one(self):
        floorplan, directions, robot = parse(self.data)
        if self.debug:
            print_map(floorplan)
        for d in directions:
            floorplan, robot = move(floorplan, robot, d)
            if self.debug:
                print(f"Move: {d}")
                print_map(floorplan)
        self.log("=" * len(floorplan[0]))
        if self.debug:
            print("=== end run ===")
            print_map(floorplan)
        return cost(floorplan)

    def part_two(self):
        floorplan, directions, robot = parse2(self.data)
        if self.debug:
            print_map(floorplan)
        for d in directions:
            floorplan, robot = move(floorplan, robot, d)
            if self.debug:
                print(f"Move: {d}")
                print_map(floorplan)
        self.log("-" * len(floorplan[0]))
        if self.debug:
            print_map(floorplan)
        return cost(floorplan)


myapp = App(
    ""
    """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
)

if not myapp.test_one(10092, 1577255) or not myapp.test_two(9021, 1597035):
    sys.exit(1)

myapp.run()


# Day 15 TEST
#   part one: 10092
#   part two: 0
# Day 15 PROD
#   part one: 1577255
#   part two: 0
