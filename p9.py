from utils import app
from itertools import starmap
from functools import reduce


class App(app.App):
    def parse(self):
        data = [self.data[i] for i in range(0, len(self.data), 2)]
        empty = [self.data[i] for i in range(1, len(self.data), 2)]

        def _str(i, c):
            n = int(c)
            if i % 2 == 0:
                return str(i // 2) * n
            else:
                return "." * n

        line = list(starmap(_str, enumerate(self.data)))
        self._strline = str.join('', line)
        self._line = list(self._strline)

    @property
    def line(self):
        if not self._line:
            self.parse()
        return self._line
    
    @property
    def strline(self):
        if not self._strline:
            self.parse()
        return self._strline
    
    def hash(self, stringline):
        return sum(
            starmap(
                lambda i, d: int(d) * i,
                filter(lambda x: x[1] != ".", enumerate(stringline)),
            )
        )

    def part_one(self, debug=True):
        self.parse()
        self.log(f'Line: {self.strline}')
        self.log(f'Hash: {self.hash(self.line)}')

        line = self.line[:]
        left, right = 0, len(line)-1
        curhash = self.hash(line)
        
        while left < right:
            # self.log(f'left: {left}, right: {right}, line[{left}]: {line[left]}, line[{right}]: {line[right]}')
            if line[left] != '.':
                # no empty space to move to, skip
                left += 1
                continue
            if line[right] == '.':
                # no data to move, skip
                right -= 1
                continue
            # move block from line[right] to line[left]
            # This changes the hash by adding left*line[right] and removing right*line[right]
            curhash = curhash + left*int(line[right]) - right*int(line[right])
            line[left], line[right] = line[right], line[left]
            left, right = left+1, right-1
        self.log(f'line: {str.join("", line)}')
        self.log(f'computed hash: {curhash}, hash: {self.hash(str.join("", line))}')
        return curhash


    def part_two(self, debug=True):
        pass


myapp = App("2333133121414131402")
myapp.run()
# 92349417108 too low