from utils import download
import re
import sys

reday = re.compile(r'p?([\d]+).*\.py')


class App:
    def __init__(self, testdata, day=None):
        self.testdata = testdata
        self.day = day if day is not None else int(reday.match(sys.argv[0]).group(1))
        self.data = download.read(self.day)
        self.debug = '-d' in sys.argv

    def part_one(self, data, debug=False):
        pass

    def part_two(self, data, debug=False):
        pass
    
    def run(self):
        data = self.testdata
        if 'prod' in sys.argv:
            data = self.data
        print(f'Day {self.day}')
        print(f'  part one: {self.part_one(data, self.debug)}')
        print(f'  part two: {self.part_two(data, self.debug)}')