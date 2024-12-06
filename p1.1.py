import collections

data  ='''
3   4
4   3
2   5
1   3
3   9
3   3
'''.strip().splitlines()

if True:
    with open('p1.input.txt') as f:
        data = f.readlines()

data = [i.split() for i in data]
data = [(int(i), int(j)) for i, j in data]
left = [i[0] for i in data]
right = [i[1] for i in data]
leftCounter = collections.Counter(left)
rightCounter = collections.Counter(right)

left = [i*rightCounter[i] for i in left]
print(sum(left))

