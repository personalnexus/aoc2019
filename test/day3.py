from test import split, AllLinesTestBase
from typing import List, Set


class Day3(AllLinesTestBase):

    def process(self, lines):

        def getPath(line) -> Set[Point]:
            startingPoint = Point(0, 0)
            turns = split(line)
            result = []
            for turn in turns:
                pathSegment = startingPoint.move(turn)
                result.extend(pathSegment)
                startingPoint = result[-1]
            return set(result)

        path1 = getPath(lines[0])
        path2 = getPath(lines[1])
        intersections = [point for point in path2 if point.distanceFromOrigin != 0 and path1.__contains__(point)]
        minimum = min(intersections)
        return minimum.distanceFromOrigin

    def testOne(self):
        self.assertEqual(6, self.process(['R8,U5,L5,D3',
                                          'U7,R6,D4,L4']))
        self.assertEqual(159, self.process(['R75,D30,R83,U83,L12,D49,R71,U7,L72',
                                            'U62,R66,U55,R34,D71,R55,D58,R83']))
        self.assertEqual(135, self.process(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
                                            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']))


class Point:
    def __init__(self, x: int, y: int):
        self.X = x
        self.Y = y

    def move(self, turn: str) -> List:
        direction = turn[0].upper()
        distance = int(turn[1:])
        if distance == 0:
            pointsInPath = [self]
        else:
            if direction == 'R':
                operation = lambda d: Point(self.X + d, self.Y)
            elif direction == 'U':
                operation = lambda d: Point(self.X, self.Y + d)
            elif direction == 'D':
                operation = lambda d: Point(self.X, self.Y - d)
            elif direction == 'L':
                operation = lambda d: Point(self.X - d, self.Y)
            else:
                raise Exception('Invalid direction {0}'.format(direction))
            pointsInPath = [operation(d) for d in range(1, distance+1)]
        return pointsInPath

    @property
    def distanceFromOrigin(self):
        return abs(self.X) + abs(self.Y)

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def __ne__(self, other):
        return self.X != other.X or self.Y != other.Y

    def __hash__(self):
        return self.distanceFromOrigin

    def __str__(self):
        return '[{0}, {1}] {2}'.format(self.X, self.Y, self.distanceFromOrigin)

    def __lt__(self, other):
        return self.distanceFromOrigin < other.distanceFromOrigin

    def __gt__(self, other):
        return self.distanceFromOrigin > other.distanceFromOrigin