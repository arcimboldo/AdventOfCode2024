data = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''.splitlines()

if True:
    with open('p2.input.txt') as f:
        data = f.readlines()

lines = list(
    map(lambda line: [int(i) for i in line.split()],   data))


def _isSafeWithSkip(line, swap: bool=False) -> bool:
    if _isSafe(line, swap):
        return True
    for i in range(len(line)):
        newline = line[:i] + line[i+1:]
        if _isSafe(newline, swap):
            return True
    return False


def _isSafe(line, swap=False) -> bool:
    def _cond(prev, next):
        return prev>next and 1 <= prev-next <= 3
    if swap:
        cond = lambda x,y: _cond(y, x)
    else:
        cond = _cond
    prev = line[0]
    for i in line[1:]:
        if not cond(prev, i):
            return False
        prev = i
    return True


def isSafe(line) -> bool:
    return (
        _isSafeWithSkip(line) or _isSafeWithSkip(line, True)
    )

# print(lines)
for line in lines:
    print(f'{line} -> {isSafe(line)}')

print(len([line for line in lines if isSafe(line)]))