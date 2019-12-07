from test import split, AllLinesTestBase as TestBase
from typing import Iterable, List


class Point:
    """
    An immutable representation of a point on a path. Two points at the same coordinates are
    considered equal. Points are ordered by their Manhattan distance from the origin (0,0).
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.distanceFromOrigin = abs(self.x) + abs(self.y)

    def __eq__(self, other: 'Point'):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: 'Point'):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return self.distanceFromOrigin

    def __repr__(self):
        return '[{0}, {1}] {2}'.format(self.x, self.y, self.distanceFromOrigin)

    def __lt__(self, other: 'Point'):
        return self.distanceFromOrigin < other.distanceFromOrigin

    def __gt__(self, other: 'Point'):
        return self.distanceFromOrigin > other.distanceFromOrigin


class Day3(TestBase):

    _movementsByDirection = {'R': lambda p: Point(p.x + 1, p.y),
                             'L': lambda p: Point(p.x - 1, p.y),
                             'U': lambda p: Point(p.x, p.y + 1),
                             'D': lambda p: Point(p.x, p.y - 1)}

    def process(self, lines):
        path1 = set(self.getPath(lines[0]))
        path2 = self.getPath(lines[1])
        intersections = [point for point in path2 if point.distanceFromOrigin != 0 and point in path1]
        minimum = min(intersections)
        return minimum.distanceFromOrigin

    @classmethod
    def getPath(cls, line) -> Iterable[Point]:
        point = Point(0, 0)
        steps = split(line, str)
        for step in steps:
            distance = int(step[1:])
            if distance != 0:
                direction = step[0].upper()
                for _ in range(distance):
                    point = cls._movementsByDirection[direction](point)
                    yield point

    def test(self):
        self.assertEqual(6, self.process(['R8,U5,L5,D3',
                                          'U7,R6,D4,L4']))
        self.assertEqual(159, self.process(['R75,D30,R83,U83,L12,D49,R71,U7,L72',
                                            'U62,R66,U55,R34,D71,R55,D58,R83']))
        self.assertEqual(135, self.process(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
                                            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']))
