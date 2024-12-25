from utils import app
from collections import deque
from functools import cache

@cache
def can_make(design, patterns):
    if not design:
        return 1
    return sum(can_make(design[len(p):], patterns) for p in patterns if design.startswith(p))


class App(app.App):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        lines = self.data.splitlines()
        self.patterns = tuple(map(str.strip, lines[0].split(",")))
        self.designs = tuple(map(str.strip, lines[2:]))

    def part_one(self):
        return list(map(lambda design: bool(can_make(design, self.patterns)), self.designs)).count(True)
        count = 0
        for design in self.designs:
            if can_make(design, self.patterns):
                count += 1
        return count

    def part_two(self):
        pass


myapp = App(
    """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
)
myapp.run()
