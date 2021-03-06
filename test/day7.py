from test import processWithIntCodeComputer, LineByLineTestBase as TestBase
from typing import Iterable, List
from itertools import permutations


class Day7(TestBase):

    def process(self, line: str):
        allOutputs = (self.getAmpOutput(line, phases) for phases in permutations(range(5)))
        maxOutput = max(allOutputs)
        return maxOutput

    def getAmpOutput(self, line: str, phases: Iterable[int]):
        io = [0]
        for phase in phases:
            inputs = [phase]
            inputs.extend(io)
            io = processWithIntCodeComputer(line, inputs)[1]
        return io.pop(0)

    def test(self):
        self.assertEqual(43210, self.getAmpOutput('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', [4, 3, 2, 1, 0]))
        self.assertEqual(54321, self.getAmpOutput('3,23,3,24,1002,24,10,24,1002,23,-1,23,'
                                                  '101,5,23,23,1,24,23,23,4,23,99,0,0', [0, 1, 2, 3, 4]))
        self.assertEqual(65210, self.getAmpOutput('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,'
                                                  '1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0', [1, 0, 4, 3, 2]))
