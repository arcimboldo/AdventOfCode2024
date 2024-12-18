from collections import deque
from utils import app
import sys

# Cost of turning 90degree: 1000
# cost of moving one step forward: 1
# Starting direction: east, that is: 1j

INF = float('inf')

def search(maze, p, curdir, visited, mycost):
    # for each rotation, check if we can go
    # then we call search on that node
    # if we hit a visited node with higher cost, we update it
    neighbors = [
        # point, direction, cost
        (p+curdir, curdir, 1),
        (p+curdir*1j, curdir*1j, 1001),
        (p+curdir*-1j, curdir*-1j, 1001),
        (p+curdir*-1, curdir*-1, 2001),
    ]
    neighbors = [n for n in neighbors if maze[n[0]] != '#']
    visited[p] = mycost
    trees = [] # next point, cost of next point, result of the search
    for n, d, c in neighbors:
        if n in visited and visited[n] < c+mycost:
            continue
        if maze[n] == 'E':
            trees.append([n, c, 0])
        elif maze[n] != '#':
            trees.append([n, c, search(maze, n, d, visited, mycost+c)])
        elif maze[n] == '#':
            trees.append([n, c, INF])
    cost = INF
    for n, c, s in trees:
        if cost > c+s:
            cost = c+s
    return cost
        
def parse(data):
    maze = {}
    S = 0
    for row, line in enumerate(data.splitlines()):
        for col, c in enumerate(line.strip()):
            maze[row+col*1j] = c
            if c == 'S':
                S = row+col*1j
    return maze, S

class App(app.App):
    def part_one(self):
        maze, S = parse(self.data)
        return search(maze, S, 1j, dict(), 0)
        

    def part_two(self):
        pass



# myapp = App('''
# ###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############
# ''')

# myapp.test_one(7036, None)

myapp = App('''
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
''')
# myapp.run()
myapp.test_one(11048, None)

