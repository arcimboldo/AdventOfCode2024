from pprint import pprint
from utils import app
from collections import defaultdict


class App(app.App):
    def part_one(self):
        graph = defaultdict(list)
        for line in self.data.splitlines():
            a, b = line.split('-')
            graph[a].append(b)
            graph[b].append(a)
        print(graph)
        valid = set()
        for node, nodes in graph.items():
            if not node.startswith('t'):
                continue
            # first node is node, let's find the next 2
            for n in graph[node]:
                if n == node:
                    continue
                for nn in graph[n]:
                    # select nn only if node is in graph[nn]
                    if nn != node and node in graph[nn]: 
                        valid.add(tuple(sorted((node, n, nn))))
        out = [tuple(sorted(x)) for x in valid]
        out.sort()
        print(str.join('\n', [str.join(',', i) for i in out]))
        return len(valid)

    def part_two(self):
        pass
        
myapp = App('''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
''')
myapp.test_one(7, 1184)
myapp.run()
