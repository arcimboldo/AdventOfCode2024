
data  ='''
3   4
4   3
2   5
1   3
3   9
3   3
'''.strip().splitlines()

with open('p1data.txt') as f:
    data = f.readlines()

data = [i.split() for i in data]
data = [(int(i), int(j)) for i, j in data]
left = [i[0] for i in data]
right = [i[1] for i in data]
left.sort()
right.sort()
diff = [abs(j-i) for i, j in zip(left, right)]
print(left, right, diff)
print(sum(diff) )