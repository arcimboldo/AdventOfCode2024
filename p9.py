from utils import app
from itertools import starmap, chain
from functools import reduce
from collections import defaultdict


def hash(blocks):
    """Compute the hash of the blocks"""
    return sum(
        starmap(
            lambda i, d: int(d) * i,
            filter(lambda x: x[1] != ".", enumerate(blocks)),
        )
    )


class App(app.App):
    def parse(self):
        """Parse compressed representation and produces the block representation."""

        def _str(i, c):
            """Given the index 'i' and the character 'c', returns a list
            representing the correct sequence of blocks.

            For even indices: a 'c' long list of digits (as strings) equal to the current file ID
            For odd indices: a 'c' long list of '.'

            For instance: 12345 produces:
            [['0'], ['.','.'], ['1','1','1'], ['.','.','.','.'], ['2','2','2','2','2']]
            """
            n = int(c)
            if i % 2 == 0:
                return [str(i // 2)] * n
            else:
                return ["."] * n

        self._blocks = list(chain(*starmap(_str, enumerate(self.data))))
        self.log(self._blocks)
        return self._blocks

    @property
    def blocks(self):
        """A list representing the blocks of the underlying data"""
        if not hasattr(self, "_blocks"):
            self.parse()
        return self._blocks

    def part_one(self, debug=True):
        # self.log(f"blocks: {self.strblocks}")
        self.log(f"hash: {hash(self.blocks)}")

        # make a copy. Only needed for representation
        blocks = self.blocks[:]

        left, right = 0, len(blocks) - 1
        # compute current hash: we will adjust it while "moving" blocks
        curhash = hash(blocks)

        while left < right:
            # self.log(
            # f"left: {left}, right: {right}, blocks[{left}]: {blocks[left]}, blocks[{right}]: {blocks[right]}"
            # )
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
            blocks[left], blocks[right] = blocks[right], "."
            # move indices right and left
            left, right = left + 1, right - 1
        # self.log(f'blocks: {blocks}')
        self.log(f"computed hash: {curhash}, hash: {hash(blocks)}")
        return curhash

    def part_two(self, debug=True):
        # empty_spaces maps size -> list of indeces where you can find an empty
        # space of that size.
        empty_spaces = defaultdict(list)
        empty = False
        curlen = 0
        # Fill in empty_spaces
        for i, c in enumerate(self.blocks):
            if c == ".":
                empty = True
                curlen += 1
            else:
                empty = False
                if curlen > 0:
                    empty_spaces[curlen].append(i - curlen)
                curlen = 0

        # Make a local copy for printing reasons
        blocks = self.blocks[:] if self.debug else None

        def swap(right, curlen):
            # Find the best spot where to put the file starting at index right
            # return the adjustement for hash
            avail = list(
                filter(lambda x: x >= curlen and empty_spaces[x], empty_spaces)
            )
            if not avail:
                self.log(f"Unable to swap: no empty space big enough")
                return 0
            min_space, min_space_idx = max(empty_spaces), len(self.blocks) + 1
            for d in avail:
                if empty_spaces[d][0] < min_space_idx:
                    min_space_idx = empty_spaces[d][0]
                    min_space = d
            # left is the leftmost empty space where I can move the file at right
            left = empty_spaces[min_space].pop(0)
            if left >= right:
                self.log(
                    f"Leftmost empty block is {left} which is to the right of {right} -> not swapping"
                )
                return 0
            if min_space > curlen:
                empty_spaces[min_space - curlen].append(left + curlen)
                empty_spaces[min_space - curlen].sort()
            if self.debug:
                print(f"Moving {blocks[right]} from {right} to {left} (len {curlen})")
            adjhash = 0
            for i in range(curlen):
                if self.debug:
                    blocks[left + i] = blocks[right + i]
                    blocks[right + i] = "."
                adjhash = (
                    adjhash
                    + int(self.blocks[right + i]) * (left + i)
                    - int(self.blocks[right + i]) * (right + i)
                )
            return adjhash

        # Loop from right to left
        curlen = 0
        curid = "."
        self.log(f'Initial blocks is\n  {str.join("", self.blocks)}')
        curhash = hash(self.blocks)
        for right in range(len(self.blocks) - 1, -1, -1):
            # self.log(f'-> right {right}, blocks[right]: {blocks[right]} curid: {curid}, curlen: {curlen}')
            if self.blocks[right] == curid:
                # We only increment if this is not an empty space, because we
                # use curlen to decide to swap
                if self.blocks[right] != ".":
                    curlen += 1
                continue

            # Change of block type. If the previous was not empty space, we swap
            if curlen > 0:
                curhash += swap(right + 1, curlen)
                # self.log(str.join('', blocks))
            curlen = 1 if self.blocks[right] != "." else 0
            curid = self.blocks[right]
        # We might need to do one more swap
        if curlen > 0:
            if self.debug:
                self.log(
                    f"LAST -> right {right}, blocks[right]: {blocks[right]} curid: {curid}, curlen: {curlen}"
                )
            curhash += swap(right, curlen)

        # We also need to swap the last block if possible
        self.log(str.join("", self.blocks))
        if self.debug:
            print(str.join("", blocks))
            print(f"hash: {hash(blocks)}, curhash: {curhash}")
        return curhash


myapp = App("2333133121414131402", day=9)
myapp.run()
# Part one:
#   test: 1928
#   prod: 6471961544878
# Part two:
#   test: 2858
#   prod:

# got 8705230292234, too hight, should be 6511178035564
