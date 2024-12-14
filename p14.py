from utils import app
import re
from collections import defaultdict
from itertools import product

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

    def move(self):
        self.px = (self.px + self.vx) % self.xmax
        self.py = (self.py + self.vy) % self.ymax


class App(app.App):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.xmax = 101 if self.prod else 11
        self.ymax = 103 if self.prod else 7

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

    def safety_factor(self):
        roboloc = defaultdict(int)
        for r in self.robots:
            roboloc[r.p] += 1
        # Count the robots
        # Quadrants are 0-xmax//2, xmax//2+1-xmax
        # and 0-ymax//2, ymax//2+1 - ymax
        factor = 1
        for q in product([
            # x start, end
            (0, self.xmax//2), (self.xmax//2+1, self.xmax),
        ], [
            # y start end
            (0, self.ymax//2), (self.ymax//2+1, self.ymax)
        ]):
            # find how many in the quadrant
            count = 0
            for x in range(q[0][0], q[0][1]):
                for y in range(q[1][0],q[1][1] ):
                    count += roboloc[(x,y)]    
            self.log(f'Quadrant, count: {count}')   
            factor *= count    
            
        return factor

    def part_one(self):

        # self.print_robots(self.robots)
        for i in range(100):
            for r in self.robots:
                r.move()
        self.print_robots()
        return self.safety_factor()

    def part_two(self):
        pass


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
myapp.run()
