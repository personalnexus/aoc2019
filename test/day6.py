from test import AllLinesTestBase as TestBase
from typing import List, DefaultDict, Set
from collections import defaultdict


class Object:

    def __init__(self):
        self.orbiters: List[Object] = []

    def getOrbiterCount(self, countedObjects: Set['Object']):
        countedObjects.add(self)
        uncountedOrbiters = [o for o in self.orbiters if o not in countedObjects]
        countedObjects.update(uncountedOrbiters)

        directOrbits = len(uncountedOrbiters)
        indirectOrbits = sum(o.getOrbiterCount(countedObjects) for o in uncountedOrbiters)

        result = directOrbits + indirectOrbits
        return result


class Day6(TestBase):

    def process(self, lines: List[str]):
        objectsByName: DefaultDict[str, Object] = defaultdict(Object)
        for orbit in lines:
            orbitedName, orbiterName = orbit.split(')')
            orbited = objectsByName[orbitedName]
            orbiter = objectsByName[orbiterName]
            orbited.orbiters.append(orbiter)

        # protect against infinite recursion by recording the objects we already counted
        orbitCountChecksum = sum(o.getOrbiterCount(set()) for o in objectsByName.values())
        return orbitCountChecksum

    def test(self):
        self.assertEqual(0, self.process(['A)A']))
        self.assertEqual(1, self.process(['A)B']))
        self.assertEqual(3, self.process(['A)B',
                                          'B)C']))
        self.assertEqual(4, self.process(['A)B',
                                          'B)C',
                                          'C)B']))
        self.assertEqual(42, self.process(['COM)B',
                                           'B)C',
                                           'C)D',
                                           'D)E',
                                           'E)F',
                                           'B)G',
                                           'G)H',
                                           'D)I',
                                           'E)J',
                                           'J)K',
                                           'K)L']))
