from utils import download
import sys
import copy

if "prod" in sys.argv:
    data = download.read(7)
else:
    data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

operations = dict()
for line in data.splitlines():
    s, operands = line.split(":", 1)
    operations[int(s)] = list(map(int, operands.split()))


# def find_combinations(operands):
#     if not operands:
#         return [0]
#     print(f'operands: {operands}')
#     reminder = find_combinations(operands[1:])
#     ops = [operands[0] + x for x in reminder] + [operands[0] * x for x in reminder]
#     if len(operands) > 1:
#         ops.extend(find_combinations(
#         [int(f'{operands[1]}{operands[0]}')] + operands[2:]
#     ))
#     return  ops


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


total = 0
for s, operands in operations.items():
    x = find_combinations2(operands[0], operands[1:])
    # print(f"{s}: {operands}: {x}")
    if s in x:
        total += s

# test must be 3749
print(f"Part one: {total}")
