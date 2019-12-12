from test import AllLinesTestBase as TestBase, split
from typing import List, Iterable, Callable
from itertools import combinations
from collections import defaultdict
import operator


MoonNames = defaultdict(str, {0: 'Io', 1: 'Europa', 2: 'Ganymede', 3: 'Callisto'})


class Vector(object):
    def __init__(self, elements: Iterable[int]):
        self._elements = list(elements)
        assert len(self._elements) == 3

    def __add__(self, other: 'Vector'):
        return self._combine(other, operator.add)

    def __sub__(self, other: 'Vector'):
        return self._combine(other, operator.sub)

    def __mul__(self, other: 'Vector'):
        return self._combine(other, operator.mul)

    def __repr__(self):
        return f'x={self._elements[0]:3}, ' \
               f'y={self._elements[1]:3}, ' \
               f'z={self._elements[2]:3}'

    def compareTo(self, other: 'Vector'):
        return self._combine(other, lambda s, o: 0 if s == o else (-1 if s < o else 1))

    def _combine(self, other: 'Vector', func: Callable[[int, int], int]):
        return Vector(map(func, self._elements, other._elements))

    @property
    def abs(self):
        return sum(map(operator.abs, self._elements))


class Moon(object):

    def __init__(self, name: str, coordinates: Iterable[int]):
        self.name = name
        self.position = Vector(coordinates)
        self.velocity = Vector((0, 0, 0))

    def getGravitationalPull(self, other: 'Moon') -> Vector:
        return self.position.compareTo(other.position)

    @property
    def totalEnergy(self):
        return self.position.abs * self.velocity.abs

    def __repr__(self):
        return f'pos=<{self.position}>, vel=<{self.velocity}>, energy={self.totalEnergy:3}, name={self.name}'


class JupiterLunarSystem(object):

    def __init__(self, positions: Iterable[Iterable[int]], printStateInterval=0):
        self._moons: List[Moon] = [Moon(MoonNames[i], position) for (i, position) in enumerate(positions)]
        self._timeIndex = 0
        self._printStateInterval = printStateInterval
        self.printState()

    def progress(self, timeSteps: int):
        for i in range(timeSteps):
            self._timeIndex += 1
            # apply gravity
            for (a, b) in combinations(self._moons, 2):
                gravity = a.getGravitationalPull(b)
                a.velocity -= gravity
                b.velocity += gravity
            # apply velocity
            for moon in self._moons:
                moon.position += moon.velocity
            self.printState()

    def printState(self):
        if (self._printStateInterval != 0) and (self._timeIndex % self._printStateInterval == 0):
            print(f'After {self._timeIndex} steps:')
            for moon in self._moons:
                print(moon)
            print(f'Sum of total energy: {" + ".join(str(m.totalEnergy) for m in self._moons)} = {self.totalEnergy}\n')

    @property
    def totalEnergy(self):
        return sum((m.totalEnergy for m in self._moons))


class Day12(TestBase):

    def process(self, lines: List[str]):
        lunarSystem = JupiterLunarSystem((split(line, int) for line in lines))
        lunarSystem.progress(1000)
        return lunarSystem.totalEnergy

    def test(self):
        lunarSystem = JupiterLunarSystem(((-1, 0, 2),
                                         (2, -10, -7),
                                         (4, -8, 8),
                                         (3, 5, -1)), 1)
        lunarSystem.progress(10)
        self.assertEqual(179, lunarSystem.totalEnergy)

        lunarSystem = JupiterLunarSystem(((-8, -10, 0),
                                          (5, 5, 10),
                                          (2, -7, 3),
                                          (9, -8, -3)), 10)
        lunarSystem.progress(100)
        self.assertEqual(1940, lunarSystem.totalEnergy)


