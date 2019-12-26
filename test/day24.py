from test import AllLinesTestBase as TestBase
from typing import List, Iterable
from math import pow


class BugPopulation(object):

    def __init__(self, bugs: Iterable[int]):
        self.bugs = [i for i in bugs]
        # since the bug population is basically an array of 25 bits, we could have fit it into a single 32 bit integer
        # but this is a more maintainable representation

    def __hash__(self):
        return self.getBioDiversity()

    def __eq__(self, other: 'BugPopulation'):
        result = all(self.bugs[i] == other.bugs[i] for i in range(25))
        return result

    def __repr__(self):
        lines = []
        for y in range(5):
            lines.append(''.join('#' if self.bugs[(5 * y) + x] == 1 else '.' for x in range(5)))
        return '\n'.join(lines)

    def evolve(self):
        for i in range(25):
            surrounding = ((self.bugs[i - 1] if i % 5 != 0 else 0) +
                           (self.bugs[i + 1] if i % 5 != 4 else 0) +
                           (self.bugs[i - 5] if i >= 5 else 0) +
                           (self.bugs[i + 5] if i < 20 else 0))
            if self.bugs[i] == 1:
                result = 1 if surrounding == 1 else 0
            else:
                result = 1 if surrounding in (1, 2) else 0
            yield result

    def getBioDiversity(self):
        result = int(sum(self.bugs[i] * pow(2, i) for i in range(25)))
        return result


class Day24(TestBase):

    def process(self, lines: List[str]):
        bugs = BugPopulation(1 if c == '#' else 0 for c in ''.join(lines))
        allBugs = {bugs}
        result = None
        while result is None:
            bugs = BugPopulation(bugs.evolve())
            if bugs in allBugs:
                result = bugs.getBioDiversity()
                break
            allBugs.add(bugs)
        return result

    def test(self):
        self.assertEqual(2129920, self.process(['....#',
                                                '#..#.',
                                                '#..##',
                                                '..#..',
                                                '#....']))
