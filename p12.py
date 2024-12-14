from utils import app
from collections import defaultdict
import sys
from colorama import Fore, Style, ansi


def UP(row, col):
    return row-1, col
def DOWN(row, col):
    return row+1, col
def LEFT(row, col):
    return row, col-1
def RIGHT(row, col):
    return row, col+1

def neigh_in_line(a, b):
    return a[0] == b[0] or a[1] == b[1]

def exdir(dr, dc):
    return {
        (0, 1): "→ right",
        (0,-1): "← left",
        (-1, 0): "↑ up",
        (1, 0): "↓ down",
    }[(dr,dc)]

class App(app.App):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.curdata = [i.strip() for i in self.data.splitlines()]
        self.numcols = len(self.curdata[0].strip())
        self.numrows = len(self.curdata)
        # fucking hack
        self._data = self.curdata
        self._testdata = self.curdata

    def inbound(self, row, col):
        return 0 <= row < self.numrows and 0 <= col < self.numcols

    def is_neigh(self, row, col, row2, col2):
        return self.inbound(row2, col2) and self.inbound(row, col) and self.data[row][col] == self.data[row2][col2]

    def neighbors(self, row, col):
        c = self.curdata[row][col]
        coords = [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]
        return list(
            filter(
                lambda x: c == self.curdata[x[0]][x[1]],
                filter(lambda x: self.inbound(x[0], x[1]), coords),
            )
        )
        
    def visit(self, row, col, plot):
        """Visit all the plot close to this of the same type and returns the total perimeter"""
        c = self.curdata[row][col]
        if (row, col) in plot:
            return (0, 0)  # Done visiting
        plot.add((row, col))
        # Visit the neighbor places
        neighb = self.neighbors(row, col)
        # Perimeter extended by this dot is 4 minus the neighbor plots of the same type
        P = 4 - len(neighb)
        E = 0
        # Counting the corners, because they will be the same as the edges

        if len(neighb) == 1:
            # only one neighbor: count 2 corners
            E = 2
        elif len(neighb) == 0:
            # No neighbors, isolated square
            E = 4
        elif len(neighb) == 2 and neigh_in_line(*neighb):
            # Two neighbors in the same line
            E = 0
        else: # This is an L or a cross situation
            if len(neighb) == 2:
                E += 1
            if self.is_neigh(row, col, *UP(row, col)) and self.is_neigh(row, col, *RIGHT(row, col)):
                if not self.is_neigh(row, col, *UP(*RIGHT(row, col))):
                    E += 1
            if self.is_neigh(row, col, *RIGHT(row, col)) and self.is_neigh(row, col, *DOWN(row, col)):
                if not self.is_neigh(row, col, *RIGHT(*DOWN(row, col))):
                    E += 1
            if self.is_neigh(row, col, *DOWN(row, col)) and self.is_neigh(row, col, *LEFT(row, col)):
                if not self.is_neigh(row, col, *DOWN(*LEFT(row, col))):
                    E += 1
            if self.is_neigh(row, col, *LEFT(row, col)) and self.is_neigh(row, col, *UP(row, col)):
                if not self.is_neigh(row, col, *LEFT(*UP(row, col))):
                    E += 1
                
        self.log(f" visiting {row},{col} ({c}) - neighbors: {neighb}, P: {P}, E: {E}")
        visits = [self.visit(n[0], n[1], plot) for n in neighb]
        
        if visits:
            perimeters, edges = list(zip(*visits))
            return (P+sum(perimeters), E+sum(edges))
        return P, E

    def print_cursor(self, row, col, visited, plot=None):
        s = []
        print('-'*self.numcols)
        print(ansi.clear_screen(), end='')
        for r, line in enumerate(self.data):
            for c in range(len(line)):
                char = self.data[r][c]
                if (r, c) == (row, col):
                    print(Fore.RED + char + Style.RESET_ALL, end='')
                elif (r,c) in plot:
                    print(Fore.LIGHTRED_EX + char + Style.RESET_ALL, end='')
                elif (r,c) in visited:
                    print(Fore.LIGHTGREEN_EX + char + Style.RESET_ALL, end='')
                else:
                    print(char, end='')
            print()

    def _run(self):

        cost1 = defaultdict(int)
        cost2 = defaultdict(int)
        visited = set()

        for row in range(self.numrows):
            for col in range(self.numcols):
                if (row, col) in visited:
                    continue
                c = self.curdata[row][col]
                # Contiguous elements in the plot
                plot = set()
                perimeter, edges = self.visit(row, col, plot)
                area = len(plot)
                cost1[c] += area * perimeter
                cost2[c] += area*edges
                visited.update(plot)
                if self.debug:
                    self.print_cursor(row, col, visited, plot)
                self.log(f'{c}: cur area: {area}, perimeter: {perimeter}, edges: {edges}')
                # self.log(f" Cur Per: {perimeter}, cur Area: {area}")
        return sum(cost1.values()), sum(cost2.values())
    def part_one(self):
        cost, _ = self._run()
        return cost
    
    def part_two(self):
        _, cost = self._run()
        return cost

# A   = 4 (no neighbors)
#

# AAA = 4 (3: 1 neighbor, no visit + 0 (neighbors on left and right, so up and down do not count), 1: neighbor on left only and visited (so up and down do not count))
#
# start: 4 - neighbors
# next: 4 - len(neighbors) - 2 (up/down) if left and right - (left/right) if up and down was visited
# 3, 2-1=1,

# AA  = 6 ()
#  A
#
# AA  = 4 (2 90d turn)
# AA
#
# A A A = 12 ()
#   A
# A A A
#
# A A A = 8 2 + 1 + 2
# A
# A A A
#
# A A A = 8
# A   A
# A A A

# 4 - len(neieghbors) - len(neighbors visited) || 0 if last

# Tests
tests = [
    (
        App(
            """
AAAA
BBCD
BBCC
EEEC
"""
        ),
        140,
        80,
    ),
    (
        App(
            """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
        ),
        772,
        436,
    ),
    (
        App(
            """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""
        ),
        None,
        236,
    ),
    (
        App(
            """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""
        ),
        None,
        368,
    ),
    (
        App(
            """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
        ),
        1930,
        1206,
    ),
]

for i, (t, r1, r2) in enumerate(tests):
    if t.prod:
        continue
    if r1:
        got = t.part_one()
        if got is None:
            continue
        if got != r1:
            print(f"ERROR: Test {i}: part ONE got {got}, expected {r1}")
            # sys.exit(1)
        else:
            print(f"OK Test {i} part one")
    if r1:
        got = t.part_two()
        if got is None:
            continue
        if got != r2:
            print(f"ERROR: Test {i}: part TWO got {got}, expected {r2}")
        else:
            print(f"OK Test {i} part two")

myapp = App(
    """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
)
# price 1930
# price part two: 1206
myapp.run()
