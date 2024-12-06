import re

ss = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
ss = '''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))'''
with open('p3.input.txt') as f:
    s = f.read()

# s = ss
m = re.compile(r'(mul\(([0-9]+),([0-9]+)\)|do\(\)|don\'t\(\))')

print(m.findall(s))
tot = 0
do = True
for match, a, b in m.findall(s):
    if match.startswith('don'):
        do = False
    elif match.startswith('do'):
        do = True
    elif do:
        tot += int(a)*int(b)
print(tot)


#print(sum(map(lambda x: int(x[0])*int(x[1]), m.findall(s))))