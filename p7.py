from utils import app
import copy


def find_combinations(cur, operands):
    # pick the first two and do some operation
    if not operands:
        return [cur]
    return find_combinations(cur + operands[0], operands[1:]) + find_combinations(
        cur * operands[0], operands[1:]
    )


def find_combinations2(cur, operands):
    if not operands:
        return [cur]
    return (
        find_combinations2(cur + operands[0], operands[1:])
        + find_combinations2(cur * operands[0], operands[1:])
        + find_combinations2(int(f"{cur}{operands[0]}"), operands[1:])
    )


class App(app.App):
    def fill_operations(self, data):
        operations = dict()
        for line in data.splitlines():
            s, operands = line.split(":", 1)
            operations[int(s)] = list(map(int, operands.split()))
        return operations

    def _runme(self, data, find_combinations_func, debug=False):
        total = 0
        operations = self.fill_operations(data)
        for s, operands in operations.items():
            x = find_combinations_func(operands[0], operands[1:])
            if debug:
                print(f"{s}: {operands}: {x}")
            if s in x:
                total += s
        return total

    def part_one(self, data, debug=False):
        return self._runme(data, find_combinations, debug)

    def part_two(self, data, debug=False):
        return self._runme(data, find_combinations2, debug)


myapp = App(
    """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
)
myapp.run()
