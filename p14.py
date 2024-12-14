import colorama as cr
import imageio.v3 as iio
import numpy
import os
import re
import subprocess
import sys

from collections import defaultdict
from itertools import product, batched
from utils import app

rerobot = re.compile(r"p=(-?[0-9]+),(-?[0-9]+) v=(-?[0-9]+),(-?[0-9]+)")


class Robot:
    def __init__(self, line, xmax, ymax):
        m = rerobot.search(line)
        self.xmax, self.ymax = xmax, ymax
        self.px = int(m.group(1))
        self.py = int(m.group(2))
        self.vx = int(m.group(3))
        self.vy = int(m.group(4))

    @property
    def p(self):
        return (self.px, self.py)

    @property
    def v(self):
        return (self.vx, self.vy)

    def move(self, n=1):
        self.px = (self.px + self.vx*n) % self.xmax
        self.py = (self.py + self.vy*n) % self.ymax


class App(app.App):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.xmax = 101 if self.prod else 11
        self.ymax = 103 if self.prod else 7
    
    def parse(self):
        self.robots = [
            Robot(line, self.xmax, self.ymax) for line in self.data.splitlines()
        ]

    def print_robots(self):
        """Print robot positions"""
        roboloc = {}
        for r in self.robots:
            if r.p not in roboloc:
                roboloc[r.p] = 0
            roboloc[r.p] += 1
        for y in range(self.ymax):
            for x in range(self.xmax):
                p = (x, y)
                print(f'{roboloc.get(p, ".")}', end="")
            print("\n", end="")

    def save_img(self, path):
        # scale = 2
        img = numpy.zeros((self.xmax, self.ymax, 3), dtype=numpy.uint8)
        for r in self.robots:
            img[r.px, r.py] = (0xFF, 0, 0)
        iio.imwrite(path, img)

    def safety_factor(self):
        roboloc = defaultdict(int)
        for r in self.robots:
            roboloc[r.p] += 1
        # Count the robots
        # Quadrants are 0-xmax//2, xmax//2+1-xmax
        # and 0-ymax//2, ymax//2+1 - ymax
        factor = 1
        for q in product(
            [
                # x start, end
                (0, self.xmax // 2),
                (self.xmax // 2 + 1, self.xmax),
            ],
            [
                # y start end
                (0, self.ymax // 2),
                (self.ymax // 2 + 1, self.ymax),
            ],
        ):
            # find how many in the quadrant
            count = 0
            for x in range(q[0][0], q[0][1]):
                for y in range(q[1][0], q[1][1]):
                    count += roboloc[(x, y)]
            # self.log(f'Quadrant, count: {count}')
            factor *= count

        return factor

    def part_one(self):
        self.parse()
        for r in self.robots:
            r.move(100)
        self.print_robots()
        return self.safety_factor()

    def part_two(self):
        self.parse()
        safety = []
        m = self.safety_factor()

        for i in range(15000):
            if i % 100 == 0:
                    print(f'{i}')
            for r in self.robots:
                r.move()
            safety.append(self.safety_factor())
            path = f'img/part_two_{i:05}.png'
            if not os.path.exists(path) or os.path.getsize(path) < 600:
                self.save_img(path)
                subprocess.call(['mogrify', '-label', path, path])
        idx=0
        for i, s in enumerate(safety):
            if s < m:
                m = s
                idx = i
        return idx+1
myapp = App(
    """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
)

# Visual search done using imagemagick
if 'montage' in sys.argv:
    for i, batch in enumerate(batched([f'img/part_two_{i:05}.png' for i in range(10000)], 120)):
        out = f'out_{i:04}.png'
        if not os.path.exists(out) or os.path.getsize(out) < 250000:
            subprocess.call(['montage', '-label', '%l', '-tile', '15x8']+ list(batch) + [out])
else:
    myapp.run()

### WTF 7502 is the solution, why the fuck?