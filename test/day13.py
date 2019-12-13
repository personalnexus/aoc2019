from itertools import count
from test import processWithIntCodeComputer, LineByLineTestBase as TestBase


class Day13(TestBase):

    def process(self, line: str):
        tiles = processWithIntCodeComputer(line, [])[1]
        blockCount = count(tile for tile in tiles[::3] if tile == 2)
        return blockCount

    def test(self):
        self.assertEqual(1, self.process('104,2,104,3,104,6,104,5,104,2,104,2,99'))
