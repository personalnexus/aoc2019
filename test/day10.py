from typing import List
import itertools

from test import AllLinesTestBase as TestBase


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

    def __init__(self, a: Asteroid, b: Asteroid):
        self.a = a
        self.b = b

        self._minX = min(self.a.x, self.b.x)
        self._maxX = max(self.a.x, self.b.x)
        self._minY = min(self.a.y, self.b.y)
        self._maxY = max(self.a.y, self.b.y)

        if a.x == b.x:
            # vertical line cannot be expressed as a linear function
            self._slope = None
            self._intersect = None
        else:
            self._slope = float(a.y - b.y) / float(a.x - b.x)
            self._intersect = a.y - (self._slope * a.x)

    def isClear(self, allAsteroids: List[Asteroid]):
        for asteroid in allAsteroids:
            if asteroid != self.a and asteroid != self.b and self.isObstructedBy(asteroid):
                result = False
                break
        else:
            result = True
        return result

    def isObstructedBy(self, c: Asteroid):
        if self._slope is None:
            isInLine = c.x == self.a.x
        else:
            isInLine = self._slope * c.x + self._intersect == c.y
        result = (isInLine and
                  self._minX <= c.x <= self._maxX and
                  self._minY <= c.y <= self._maxY)
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

        for los in (LineOfSight(a, b) for (a, b) in itertools.combinations(allAsteroids, 2)):
            if los.isClear(allAsteroids):
                los.a.clearLinesOfSight.append(los)
                los.b.clearLinesOfSight.append(los)

        bestMonitoringStation = max(allAsteroids, key=lambda a: a.clearLinesOfSightCount)
        return bestMonitoringStation.clearLinesOfSightCount

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
