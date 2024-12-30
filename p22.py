from utils import app
from collections import defaultdict

def calculate(s, n ):
    for i in range(n):
        s = ((s <<6) ^ s) % 16777216

        s = ((s >> 5) ^ s) % 16777216

        s = ((s << 11) ^ s) % 16777216
        yield s


class App(app.App):
    def part_one(self):
        numbers = list(map(int, self.data.splitlines()))
        s = 0
        for n in numbers:
            for last in calculate(n, 2000):
                continue
            s += last
        return s

    def part_two(self):
        numbers = list(map(int, self.data.splitlines()))
        # Map secret number -> list of deltas
        deltas = {}
        # map secret number -> list of prices (only the last digit)
        prices = {}
        for n in numbers:
            prev = 0
            changes = []
            delta = []
            for last in calculate(n, 2000):
                p = last%10
                changes.append(p-prev)
                delta.append(p)
                prev = p
            deltas[n] = changes
            prices[n] = delta + [prev]

        # slices: map 4-tuple -> {number -> max price}
        slices = defaultdict(dict)
        for n, delta in deltas.items():
            # for each number, get the slices and add them as tuple to slices.
            for i in range(2000):
                s = delta[i:i+4]
                if len(s) != 4:
                    break
                t = tuple(delta[i:i+4]) 
                # This 
                if n not in slices[t]:
                    slices[t][n] = prices[n][i+3]

        best = {}
        for t in slices:
            best[t] = sum(slices[t].values())

        m = max(best.values())

        return m



myapp = App("""
1
10
100
2024
""")
myapp.test_one(None, 20411980517)
myapp.test_two(24, None)
myapp = App('''1
2
3
2024
''')
myapp.test_two(23, 2362)
myapp.run()
