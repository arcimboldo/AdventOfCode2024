from pprint import pprint
from utils import app
from collections import defaultdict, deque


class App(app.App):
    def part_one(self):
        graph = defaultdict(set)
        for line in self.data.splitlines():
            a, b = line.split('-')
            graph[a].add(b)
            graph[b].add(a)

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
        graph = defaultdict(set)
        for line in self.data.splitlines():
            a, b = line.split('-')
            graph[a].add(b)
            graph[b].add(a)
        # Sane as part one but without limit
        max_loops = set()
        for node in graph:
            # This is the start of the loop
            loop = set()
            loop.add(node)
            q = deque(graph[node])
            while q:
                n = q.popleft()

                if n in loop:
                    continue
                # Find if this is a clique. graph[n] needs to have connections to all the nodes in the loop
                # In set term, it means that the loop needs to be a subset of all the visited nodes
                if loop.issubset(graph[n]):
                    loop.add(n)
            # We should have found the biggest clique for 'node'
            sloop = tuple(sorted(loop))

            max_loops.add(sloop)
        
        max_len, max_loop = 0, None
        for loop in max_loops:
            if len(loop) > max_len:
                max_len = len(loop)
                max_loop = loop
        return str.join(',', max_loop)
        
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
