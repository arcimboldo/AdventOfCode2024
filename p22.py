from utils import app


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
        pass


myapp = App("""
1
10
100
2024
""")
myapp.run()
