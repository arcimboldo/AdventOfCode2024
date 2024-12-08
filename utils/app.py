from utils import download
import re
import sys

reday = re.compile(r'p?([\d]+).*\.py')


class App:
    def __init__(self, testdata, day=None):
        self._testdata = testdata
        self.day = day if day is not None else int(reday.match(sys.argv[0]).group(1))
        self._data = download.read(self.day)
        self.debug = '-d' in sys.argv

    def part_one(self, debug=False):
        pass

    def part_two(self, debug=False):
        pass
    
    @property
    def data(self):
        return self._data if 'prod' in sys.argv else self._testdata
        
    def run(self):
        print(f'Day {self.day}')
        print(f'  part one: {self.part_one(self.debug)}')
        print(f'  part two: {self.part_two(self.debug)}')