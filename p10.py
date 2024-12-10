from utils import app
import itertools as it
from collections import defaultdict


class App(app.App):
    @property
    def topo(self):
        if not hasattr(self, "_topo"):
            self._topo = [
                list(map(int, line.strip())) for line in self.data.splitlines()
            ]
        return self._topo

    def visit(self, head, topo, idx):
        x, y = head
        nhead = topo[y][x]
        paths = []
        self.log(f"{idx}: visited head {head} ({nhead})")
        for dx, dy in [[0, 1], [1, 0], [-1, 0], [0, -1]]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(topo) and 0 <= nx < len(topo[0]):
                if nhead + 1 != topo[ny][nx]:
                    continue
                self.log(f"{idx} next: {nx},{ny}:  {topo[ny][nx]}")
                for p in self.visit((nx, ny), topo, idx + 1):
                    paths.append([head] + p)
        if not paths:
            return [[head, nhead]]
            self.log(f"  {head}: End of the trail")
        else:
            self.log(f"  {head}: paths: {paths}")
        return paths

    def visit_topo(self):
        # Find the first 0
        paths = []
        for line in self.topo:
            self.log(line)
        visited = set()
        for i, j in it.product(range(len(self.topo[0])), range(len(self.topo))):
            if self.topo[j][i] == 0:
                self.log(f"Starting to visit from {i},{j}")
                paths.extend(self.visit((i, j), self.topo, 0))
        self.log(paths)
        return paths
    
    def part_one(self):
        # probably unnecessary
        paths = self.visit_topo()
        score = defaultdict(int)
        visited = defaultdict(set)
    
        for p in paths:
            head = tuple(p[0])
            tail = tuple(p[-2])
            if p[-1] != 9:
                continue
            if tail not in visited[head]:
                score[head] += 1
                visited[head].add(tail)
        return sum(score.values())

    def part_two(self):
        all_paths = self.visit_topo()
        score = defaultdict(set)
        for path in all_paths:
            if path[-1] != 9: continue
            score[tuple(path[0])].add(tuple(path))
        
        return sum(len(p) for p in score.values())
        


# Visit from 9 and go backwards, if you find some point you visited already with
# a bigger number, then you already visited the hwole graph. Is that correct?

myapp = App(
    """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""",
    day=10,
)

# myapp = App('''
#             019
#             124
#             544''')
myapp.run()

# Part one
#  test: 36
#  prod: 624
# Part two
#  test: 81
#  prod: 1483
