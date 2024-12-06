from functools import cmp_to_key
import os
from utils import download

data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

data = download.read(5)


def parse_data(data):
    rules = set()
    updates = []
    lines = data.splitlines()

    rules = list(
        map(
            lambda x: (int(x[0]), int(x[1])),
            map(lambda x: x.split("|"), [l for l in lines if "|" in l]),
        )
    )
    updates = list(
        list(
            map(
                lambda x: list(int(i) for i in x),
                map(lambda x: x.split(","), [line for line in lines if "," in line]),
            )
        )
    )
    return rules, updates


def cmp(rules):
    def _cmp(x, y):
        if (x, y) in rules:
            return -1
        elif (y, x) in rules:
            return 1
        else:
            return -1 if x < y else 1

    return _cmp


rules, updates = parse_data(data)
correct = []
for update in updates:
    ordered = list(sorted(update, key=cmp_to_key(cmp(rules))))
    if ordered == update:
        correct.append(update)

def find_middle(l):
    return l[len(l)//2]

part1 = sum(map(find_middle, correct))
print(f'Part one: {part1}')