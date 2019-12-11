from test import AllLinesTestBase as TestBase
from math import isclose
from typing import List
from itertools import combinations


class Asteroid(object):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.clearLinesOfSight: List[LineOfSight] = []

    @property
    def xy(self):
        return self.x, self.y

    @property
    def clearLinesOfSightCount(self):
        return len(self.clearLinesOfSight)

    def __repr__(self):
        return f'{self.xy} clearLoS={len(self.clearLinesOfSight)}'


class LineOfSight(object):
    """
    Represents the line between two asteroids. Had I remembered more about trig functions, I might have gone with the
    tangent instead.
    """

    def __init__(self, a: Asteroid, b: Asteroid):
        self.a = a
        self.b = b

        self._minX = min(a.x, b.x)
        self._maxX = max(a.x, b.x)
        self._minY = min(a.y, b.y)
        self._maxY = max(a.y, b.y)

        if a.x == b.x:
            # vertical line cannot be expressed as a linear function
            self._slope = None
            self._intersect = None
        else:
            self._slope = (a.y - b.y) / (a.x - b.x)
            self._intersect = a.y - (self._slope * a.x)

    def isClear(self, allAsteroids: List[Asteroid]):
        for asteroid in allAsteroids:
            if asteroid != self.a and asteroid != self.b and self._isObstructedBy(asteroid):
                result = False
                break
        else:
            result = True
        return result

    def _isObstructedBy(self, other: Asteroid):
        if self._slope is None:
            isInLine = other.x == self.a.x
        else:
            isInLine = isclose(self._slope * other.x + self._intersect, other.y)
        result = (isInLine and
                  self._minX <= other.x <= self._maxX and
                  self._minY <= other.y <= self._maxY)
        return result

    def __repr__(self):
        return f'{self.a.xy}->{self.b.xy} y={self._slope}*x+{self._intersect}'


def parseAsteroidMap(lines) -> List[Asteroid]:
    allAsteroids: List[Asteroid] = []
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            point = line[x]
            if point == '#':
                asteroid = Asteroid(x, y)
                allAsteroids.append(asteroid)
    return allAsteroids


class Day10(TestBase):

    def process(self, lines: List[str]):
        allAsteroids = parseAsteroidMap(lines)

        for (asteroidA, asteroidB) in combinations(allAsteroids, 2):
            los = LineOfSight(asteroidA, asteroidB)
            if los.isClear(allAsteroids):
                asteroidA.clearLinesOfSight.append(los)
                asteroidB.clearLinesOfSight.append(los)

        bestMonitoringStations = sorted(allAsteroids, key=lambda x: x.clearLinesOfSightCount, reverse=True)
        return bestMonitoringStations[0].clearLinesOfSightCount

    def test(self):
        self.assertEqual(8, self.process(['.#..#',
                                          '.....',
                                          '#####',
                                          '....#',
                                          '...##']))
        self.assertEqual(33, self.process(['......#.#.',
                                           '#..#.#....',
                                           '..#######.',
                                           '.#.#.###..',
                                           '.#..#.....',
                                           '..#....#.#',
                                           '#..#....#.',
                                           '.##.#..###',
                                           '##...#..#.',
                                           '.#....####']))
        self.assertEqual(35, self.process(['#.#...#.#.',
                                           '.###....#.',
                                           '.#....#...',
                                           '##.#.#.#.#',
                                           '....#.#.#.',
                                           '.##..###.#',
                                           '..#...##..',
                                           '..##....##',
                                           '......#...',
                                           '.####.###.']))
        self.assertEqual(41, self.process(['.#..#..###',
                                           '####.###.#',
                                           '....###.#.',
                                           '..###.##.#',
                                           '##.##.#.#.',
                                           '....###..#',
                                           '..#.#..#.#',
                                           '#..#.#.###',
                                           '.##...##.#',
                                           '.....#.#..']))
        self.assertEqual(210, self.process(['.#..##.###...#######',
                                            '##.############..##.',
                                            '.#.######.########.#',
                                            '.###.#######.####.#.',
                                            '#####.##.#.##.###.##',
                                            '..#####..#.#########',
                                            '####################',
                                            '#.####....###.#.#.##',
                                            '##.#################',
                                            '#####.##.###..####..',
                                            '..######..##.#######',
                                            '####.##.####...##..#',
                                            '.#####..#.######.###',
                                            '##...#.##########...',
                                            '#.##########.#######',
                                            '.####.#.###.###.#.##',
                                            '....##.##.###..#####',
                                            '.#.#.###########.###',
                                            '#.#.#.#####.####.###',
                                            '###.##.####.##.#..##']))
