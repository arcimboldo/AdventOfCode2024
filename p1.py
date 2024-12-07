import collections
from utils import app

class App(app.App):
    def part_one(self, data, debug=False):
        data = [i.split() for i in data.splitlines()]
        data = [(int(i), int(j)) for i, j in data]
        left = [i[0] for i in data]
        right = [i[1] for i in data]
        left.sort()
        right.sort()
        diff = [abs(j-i) for i, j in zip(left, right)]
        if debug:
            print(left, right, diff)
        return sum(diff)
        
    def part_two(self, data, debug=False):
        data = [i.split() for i in data.splitlines()]
        data = [(int(i), int(j)) for i, j in data]
        left = [i[0] for i in data]
        right = [i[1] for i in data]
        leftCounter = collections.Counter(left)
        rightCounter = collections.Counter(right)

        left = [i*rightCounter[i] for i in left]
        return sum(left)

myapp = App(
'''
3   4
4   3
2   5
1   3
3   9
3   3
'''.strip()
)

myapp.run()