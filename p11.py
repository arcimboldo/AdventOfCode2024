from utils import app
from itertools import chain
from functools import cache
from collections import defaultdict

import sys

@cache
def blink(stone:int):
    if stone == 0:
        return 1,
    if len(str(stone)) %2 == 0:
        s = str(stone)
        n2 = len(s)//2
        return  int(s[:n2]), int(s[n2:])
    return stone*2024,

class App(app.App):
    def part_one(self):
        stones = list(map(int, self.data.split()))
        self.log(f'Input:\n-> {str.join(" ", map(str, stones))}')
        for i in range(25):
            stones = chain(*map(blink, stones))
        lstones = list(stones)
        return len(lstones)

    def part_two(self):
        stones = defaultdict(int)
        for s in self.data.split():
            stones[int(s)] += 1
        
        for i in range(75):
            newstones = defaultdict(int)
            for k, n in stones.items():
                for i in blink(k):
                    newstones[i] += n
            stones = newstones
        return sum(stones.values())


myapp = App('''0 1 10 99 999''')
# myapp = App('125 17')
myapp.run()

# Day 11 TEST
#   part one: 125681
#   part two: 149161030616311
# Day 11 PROD
#   part one: 183248
#   part two: 218811774248729
