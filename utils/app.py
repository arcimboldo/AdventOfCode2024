from utils import download
import re
import sys

reday = re.compile(r"p?([\d]+).*\.py")


class App:
    def __init__(self, testdata, day=None):
        self._testdata = testdata.strip()
        self.day = day if day is not None else int(reday.match(sys.argv[0]).group(1))
        self._data = download.read(self.day)
        self.debug = "-d" in sys.argv
        self.prod = "prod" in map(lambda x: x.lower(), sys.argv)

    def log(self, *args, **kw):
        if self.debug:
            print(*args, **kw)

    def part_one(self):
        pass

    def part_two(self):
        pass

    @property
    def data(self):
        return self._data if self.prod else self._testdata

    def run(self):
        print(f'Day {self.day} {"PROD" if self.prod else "TEST"}')
        print(f"  part one: {self.part_one()}")
        print(f"  part two: {self.part_two()}")

    def _test(self, method, want_test, want_prod):
        oldprod = self.prod
        self.prod = False
        got_test = method()
        if got_test != want_test:
            print(f'ERROR: TEST run of {method.__name__}: got {got_test}, expected {want_test} instead')
        self.prod = True
        got_prod = method()
        if got_prod != want_prod:
            print(f'ERROR: TEST run of {method.__name__}: got {got_test}, expected {want_prod} instead')
        self.prod = oldprod
        return got_test == want_test and got_prod == want_prod

    def test_one(self, *args, **kw):
        return self._test(self.part_one, *args, **kw)

    def test_two(self, *args, **kw):
        return self._test(self.part_two, *args, **kw)
