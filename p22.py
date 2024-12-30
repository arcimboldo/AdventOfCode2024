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
        prices = {}
        for n in numbers:
            prev = 0
            changes = []
            for last in calculate(n, 2000):
                d = last%10
                changes.append(d-prev)
                prev = d
            prices[n] = changes
        slices = defaultdict(dict)
        for n, p in prices.items():
            for i in range(0, 2000):
                s = p[i:i+4]
                if len(s) != 4:
                    break
                t = tuple(p[i:i+4]) 
                slices[t][n] = max(slices[t].get(n, 0), s[i+3])
        best = {}
        for t in slices:
            s = sum(t.values())
            best[t] = s
        m = max(best.values())
        return [t for t in best if best[t] == m][0]


myapp = App("""
1
10
100
2024
""")
myapp.test_one(None, 20411980517)
myapp = App('''1
2
3
2024
''')
myapp.test_two([-2,1,-1,3], None)
# myapp.run()
