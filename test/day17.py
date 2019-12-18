from test import processWithIntCodeComputer, split, LineByLineTestBase as TestBase
from typing import List


def getAlignmentParameters(allPoints: List[int]):
    """Assumption: lines are all of the same length."""
    maxX = allPoints.index(10)
    points = [p for p in allPoints if p != 10]
    for i in range(maxX, len(points) - maxX):  # skip top and bottom rows that cannot have intersections
        x = i % maxX
        y = i // maxX
        if ((x != 0) and        # not in left-most column
           (x != maxX - 1) and  # not in right-most column
           (points[i - 1] == points[i] == points[i + 1] == points[i - maxX] == points[i + maxX] == 35)):
            yield x * y


class Day17(TestBase):

    def process(self, line: str):
        intCodeOutput = processWithIntCodeComputer(line, [])[1]
        return sum(getAlignmentParameters(intCodeOutput))

    def test(self):
        self.assertEqual([4, 8, 24, 40], list(getAlignmentParameters(
            [46, 46, 35, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 10,
             46, 46, 35, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 10,
             35, 35, 35, 35, 35, 35, 35, 46, 46, 46, 35, 35, 35, 10,
             35, 46, 35, 46, 46, 46, 35, 46, 46, 46, 35, 46, 35, 10,
             35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 10,
             46, 46, 35, 46, 46, 46, 35, 46, 46, 46, 35, 46, 46, 10,
             46, 46, 35, 35, 35, 35, 35, 46, 46, 46, 35, 46, 46])))
