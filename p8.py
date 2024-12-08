from utils import app
from collections import defaultdict
from itertools import combinations


def vdiff(a, b):
    """Return the vector distance of a(x,y) -> b(x,y) in coordinate with
    reversed y (y goes down)"""
    # -2,-1
    # a
    # ..b
    # x = a + distance, y = b -distance
    #  x
    #  ..a
    #     ..b
    #       ..y
    return (a[0] - b[0], a[1] - b[1])


def vsum(a, b):
    """returns the sum of two vectos"""
    return (a[0] + b[0], a[1]+ b[1])

def vprod(a, n):
    return (a[0]*n, a[1]*n)

def minus(a):
    """returns the opposite of the vector"""
    return (-a[0], -a[1])


def antinodes_for(a, b):
    d = vdiff(a, b)
    return (vsum(a, d), vsum(b, minus(d)))

    
def all_antinodes_for(a,b,xmax,ymax):
    d = vdiff(a,b)
    antinodes = set()
    def inbox(a):
        return 0<=a[0]<xmax and 0<=a[1]<ymax
    for i in range(xmax):
        left = vsum(a, vprod(d, i))
        right = vsum(b,vprod(minus(d), i))
        if not inbox(left) and not inbox(right):
            break
        for p in (left, right):
            if inbox(p):
                antinodes.add(p)
    
    return antinodes

class App(app.App):
    def _fill_map(self):
        self.locations = defaultdict(set)
        self.xmax, self.ymax = len(self.data.splitlines()[0].strip()), len(
            self.data.splitlines()
        )
        for y, line in enumerate(self.data.splitlines()):
            for x, c in enumerate(line.strip()):
                if c != ".":
                    self.locations[c].add((x, y))

    def draw_map(self, overlay=None):
        """Return the map with the overlay. Overlay is a map (x,y) -> c the
        character to print on coordinates x,y"""
        lines = []
        data = self.data.splitlines()
        counted = set()
        for y in range(self.ymax):
            line = []
            for x in range(self.xmax):
                if overlay and (x,y) in overlay:
                    line.append(overlay[(x,y)])
                    counted.add((x,y))
                else:
                    line.append(data[y][x])
            lines.append(str.join('', line))
        diff = set(overlay).difference(counted)
        return str.join('\n', lines)


    def inside_map(self, x):
        """Returns True if x is inside the map"""
        return 0 <= x[0] < self.xmax and 0 <= x[1] < self.ymax

    def run(self):
        self._fill_map()
        super().run()

    def _run(self, find_antinodes):
        # For each pair of each type, find the antinodes and check that they are
        # within boundary
        self.log(f'xmax: {self.xmax}, ymax: {self.ymax}')
        antinodes = defaultdict()
        for c, locations in self.locations.items():
            # Find all combinations of pairs, ignoring order
            self.log(f'{c}: {locations}')
            for a, b in combinations(locations, 2):
                anodes = find_antinodes(a,b)
                good = list(filter(self.inside_map, anodes))
                for x in good:
                    antinodes[x] = '#'
                self.log(f' antinodes_for({a}, {b}):\n    {good}')
        self.log(self.draw_map(overlay=antinodes))
        return len(antinodes)

    def part_one(self):
        return self._run(antinodes_for)

    def part_two(self):
        def find_antinodes(a, b):
            return all_antinodes_for(a, b, self.xmax, self.ymax)
        return self._run(find_antinodes)

myapp = App(
    """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
)

# myapp = App('''
# .....
# ..a..
# ..a..
# .....
# ''')
myapp.run()

solution = """
......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
"""
# 14

# NOT 365 - too high
# should be: 357
