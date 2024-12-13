from utils import app
from collections import defaultdict
import sys


def inbound(row, col, numrows, numcols):
    return 0 <= row < numrows and 0 <= col < numcols


class App(app.App):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # import pdb; pdb.set_trace()
        self.curdata = [i.strip() for i in self.data.splitlines()]
        self.numcols = len(self.curdata[0].strip())
        self.numrows = len(self.curdata)

    def neighbors(self, row, col):
        c = self.curdata[row][col]
        coords = [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]
        return list(
            filter(
                lambda x: c == self.curdata[x[0]][x[1]],
                filter(
                    lambda x: inbound(x[0], x[1], self.numrows, self.numcols), coords
                ),
            )
        )

    def visit(self, row, col, plot):
        """Visit all the plot close to this of the same type and returns the total perimeter"""
        c = self.curdata[row][col]
        if (row, col) in plot:
            return 0  # Done visiting
        plot.add((row, col))
        # Visit the neighbor places
        neighb = self.neighbors(row, col)
        # Perimeter extended by this dot is 4 minus the neighbor plots of the same type
        P = 4 - len(neighb)
        self.log(f" visiting {row},{col} ({c}) - neighbors: {neighb}, P: {P}")
        return P + sum([self.visit(n[0], n[1], plot) for n in neighb])

    def part_one(self):

        cost = defaultdict(int)
        visited = set()

        self.log(
            f"Data: \n{str.join("\n", self.curdata)}\n rows: {self.numrows}, cols: {self.numcols}"
        )
        # TODO: This is all wrong: you need to do this only for contiguous regions!
        for row in range(self.numrows):
            for col in range(self.numcols):
                if (row, col) in visited:
                    continue
                c = self.curdata[row][col]
                # Contiguous elements in the plot
                plot = set()
                perimeter = self.visit(row, col, plot)
                area = len(plot)
                cost[c] += area * perimeter
                visited.update(plot)
                self.log(
                    f"Visited {row},{col} ({c}).\n  Plot: {list(sorted(plot))}\n  visited: {visited}"
                )
                self.log(f" Cur Per: {perimeter}, cur Area: {area}")
        return sum(cost.values())

    def part_two(self):
        pass


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
        if got != r1:
            print(f"ERROR: Test {i}: part ONE got {got}, expected {r1}")
            # sys.exit(1)
        else:
            print(f"OK Test {i} part one")
    if r1:
        got = t.part_two()
        if got != r2:
            print(f"ERROR: Test {i}: part TWO got {got}, expected {r2}")
            # sys.exit(1)
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
