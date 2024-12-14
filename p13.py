from utils import app
import re

reb = re.compile(r"Button (?P<button>A|B): X\+(?P<X>[0-9]+), Y\+(?P<Y>[0-9]+)")
rep = re.compile(r"Prize: X=(?P<X>[0-9]+), Y=(?P<Y>[0-9]+)")


class App(app.App):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._data = self.parse(self._data)
        self._testdata = self.parse(self._testdata)

    def parse(self, data):
        machines = []
        d = {}
        for line in data.splitlines():
            m = reb.match(line)
            mp = rep.match(line)
            if m:
                d[m.group("button").lower()] = (int(m.group("X")), int(m.group("Y")))
            elif mp:
                d["prize"] = (int(mp.group("X")), int(mp.group("Y")))
                machines.append(d)
                d = {}
        return machines

    def solve_one(self, machine):
        return self.solve(machine, lambda na, nb: 0 <= na <= 100 and 0 <= nb <= 100)

    def solve_two(self, machine):
        return self.solve(machine, lambda na, nb: True)

    def solve(self, machine, exit_condition):
        px, py = machine["prize"]
        ax, ay = machine["a"]
        bx, by = machine["b"]

        # This is a system of equations
        # na*ax + nb*bx = px
        # na*ay + nb*by = px
        #
        # In matrix representation, this is
        #
        # |ax bx|  |na|  = |px|
        # |ay by|  |nb|    |py|
        #
        # Or you can use substitution
        #
        # na*ax + nb*bx = px
        # => na = (px-nb*bx)/ax
        # na*ay + nb*by = px
        # => (px-nb*bx)*ay/ax + nb*by = py
        # => px*ay/ax - nb*bx*ay/ax + nb*by = py
        # => nb(by - bx*ay/ax) = px-px*ay/ax
        # => nb = (py-px*ay/ax)/(by-bx*ay/ax)
        # => nb = (py*ax-px*ay)/(by*ax-bx*ay)
        nb = (py * ax - px * ay) / (by * ax - bx * ay)
        na = (px - nb * bx) / ax
        if nb.is_integer() and na.is_integer() and exit_condition(na, nb):
            return int(3 * na + nb)
        return 0

    def _run(self, data, solver):
        tokens = 0
        prizes = 0
        for i, machine in enumerate(data):
            t = solver(machine)
            if t > 0:
                self.log(f"Machine {i}, tokens: {t}")
                prizes += 1
            else:
                self.log(f"Machine {i} does not have solution")
            tokens += t
        return tokens

    def part_one(self):
        return self._run(self.data, self.solve_one)

    def part_two(self):
        data = self.data[:]
        big = 10000000000000
        for m in data:
            x, y = m["prize"]
            m["prize"] = (x + big, y + big)
        return self._run(data, self.solve_two)


myapp = App(
    """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
)
myapp.run()

# Day 13 TEST
#   part one: 480
#   part two: None
# Day 13 PROD
#   part one: 29023
#   part two: None
