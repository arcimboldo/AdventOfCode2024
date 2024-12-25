from collections import defaultdict
import heapq
from utils import app


def dijstra(maze, xmax, ymax):
    # Find minimum path

    h = []
    start = (0,0)
    # Use the cost dictionary also as a list of visited nodes
    cost = defaultdict(lambda: float('inf'))
    heapq.heappush(h, (0, start))

    predecessor = {}
    END = (xmax-1, ymax-1)
    while h:
        c, p = heapq.heappop(h)
        if p == END:
            break
        # if cost[p] < float('inf'):
        #     continue
        for n in [
            (p[0]+1, p[1]),
            (p[0]-1, p[1]),
            (p[0], p[1]+1),
            (p[0], p[1]-1),
        ]:
            if 0 <= p[0] < xmax and 0 <= p[1] < ymax and maze[p] == '.' and cost[n] > c+1:
                heapq.heappush(h, (c+1, n))
                cost[n] = c+1
                predecessor[n] = p
    path = []
    p = END
    while p in predecessor and p != start:
        path.append(p)
        p = predecessor[p]
    return list(reversed(path))

def print_maze(maze, xmax, ymax):
    for j in range(ymax):
        print(str.join("", [maze[(i, j)] for i in range(xmax)]))


class App(app.App):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.bytes = list(
            map(
                lambda x: (int(x.split(",")[0]), int(x.split(",")[1])),
                self.data.splitlines(),
            )
        )

    @property
    def xmax(self):
        return 71 if self.prod else 7

    @property
    def ymax(self):
        return self.xmax

    def part_one(self):
        numbytes = 1<<10 if self.prod else 12
        bytes = {i: "#" for i in self.bytes[:numbytes]}
        maze = defaultdict(lambda: ".") | bytes
        path = dijstra(maze, self.xmax, self.ymax)
        if self.debug:
            for p in path:
                maze[p] = 'O'
            print_maze(maze, self.xmax, self.ymax)
        return len(path)

    def part_two(self):
        # Brute force
        maze = defaultdict(lambda: ".")
        low = 1024 # we know there is a solution for this value
        high = len(self.bytes)
        tested = defaultdict(list)
        while high > low:
            mid = low + (high-low)//2
            if mid in (low, high):
                # we are done here
                break
            curmaze = maze | {i:"#" for i in self.bytes[:mid]}
            has_solution = bool(dijstra(curmaze, self.xmax, self.ymax))
            tested[has_solution].append(mid)
            if has_solution:
                low = mid
            else:
                high = mid
        # -1 because we used numbytes, i.e. the lenght and not the index
        return self.bytes[min(tested[False])-1]


myapp = App(
    """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
)
myapp.test_one(12, 296)
myapp.test_two(None, (28,44))
myapp.run()
