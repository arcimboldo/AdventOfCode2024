from utils import app
from matplotlib import pyplot as plt
from itertools import chain

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
        if c == BOX
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
        for i in range(r[0], 0 if dr == -1 else len(floorplan), dr):
            if floorplan[i][r[1]] == "#":
                break
            if floorplan[i][r[1]] == ".":
                # For Part two, we need to check if we are moving boxes.
                # Go up/down until you reach a box. If it's [, then check from r[0] to i if r[1]+1 can move
                # If it's ] then check r[1]-1.
                # Check again if if you find boxes, and re-apply
                # Basically call recursively a function first_empty_slot(column, startrow) with x either the robot, or the box we found
                # Then move the boxes independently, from up to down when moving up, down to up when moving up   
                for j in range(i, r[0], -dr):
                    floorplan[j][r[1]] = floorplan[j - dr][r[1]]
                floorplan[r[0]][r[1]] = "."
                return floorplan, (r[0] + dr, r[1] + dc)
    return floorplan, (r[0], r[1])


def print_map(floorplan):
    for i, line in enumerate(floorplan):
        print(str.join("", line))


class App(app.App):
    def part_one(self):
        floorplan, directions, robot = parse(self.data)
        print_map(floorplan)
        for d in directions:
            floorplan, robot = move(floorplan, robot, d)
            # print(f'Move: {d}')
            # print_map(floorplan)
        print("-" * len(floorplan[0]))
        print_map(floorplan)
        return cost(floorplan)

    def part_two(self):
        floorplan, directions, robot = parse2(self.data)
        print_map(floorplan)
        for d in directions:
            print(f"Move: {d} robot: {robot}")
            floorplan, robot = move(floorplan, robot, d)
            print_map(floorplan)


myapp = App(
    """##########
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

myapp.run()
