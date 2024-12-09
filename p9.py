from utils import app
from itertools import starmap
from functools import reduce


class App(app.App):
    def parse(self):
        """Parse compressed representation and produces the block representation"""

        def _str(i, c):
            """Given the index 'i' and the character 'c', returns the string
            representing the correct sequence of blocks.

            For even indices: a sequence of digits equal to the current file ID and 'c' long
            For odd indices: a sequence of . 'c' long

            For instance: 12345 produces:
            0..111....22222
            """
            n = int(c)
            if i % 2 == 0:
                return str(i // 2) * n
            else:
                return "." * n

        blocks = starmap(_str, enumerate(self.data))
        self._strblocks = str.join("", blocks)
        self._blocks = list(self._strblocks)
        return self._blocks, self._strblocks

    @property
    def blocks(self):
        """A list representing the blocks of the underlying data"""
        if not hasattr(self, "_blocks"):
            self.parse()
        return self._blocks

    @property
    def strblocks(self):
        """Same as blocks, but as a single string"""
        if not hasattr(self, "_strblocks"):
            self.parse()
        return self._strblocks

    def hash(self, blocks):
        """Compute the hash of the blocks"""
        return sum(
            starmap(
                lambda i, d: int(d) * i,
                filter(lambda x: x[1] != ".", enumerate(blocks)),
            )
        )

    def part_one(self, debug=True):
        self.log(f"blocks: {self.strblocks}")
        self.log(f"hash: {self.hash(self.blocks)}")

        # make a copy. Only needed for representation
        blocks = self.blocks[:]

        left, right = 0, len(blocks) - 1
        # compute current hash: we will adjust it while "moving" blocks
        curhash = self.hash(blocks)

        while left < right:
            self.log(
                f"left: {left}, right: {right}, blocks[{left}]: {blocks[left]}, blocks[{right}]: {blocks[right]}"
            )
            if blocks[left] != ".":
                # no empty space to move to, skip
                left += 1
                continue
            if blocks[right] == ".":
                # no data to move, skip
                right -= 1
                continue
            # swap blocks blocks[right] and blocks[left]
            # This changes the hash by adding left*blocks[right] and removing right*blocks[right]
            curhash = curhash + left * int(blocks[right]) - right * int(blocks[right])
            # only useful for representation
            blocks[left], blocks[right] = blocks[right], blocks[left]
            # move indices right and left
            left, right = left + 1, right - 1
        self.log(f'blocks: {str.join("", blocks)}')
        self.log(f'computed hash: {curhash}, hash: {self.hash(str.join("", blocks))}')
        return curhash

    def part_two(self, debug=True):
        pass


myapp = App("2333133121414131402")
myapp.run()
# got 92349417108 but it's too low
