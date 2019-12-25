from test import split, LineByLineTestBase as TestBase
from intcode import IntCodeComputer
from typing import List, Callable
from itertools import cycle


class Nic(object):

    def __init__(self, address: int, program: List[int]):
        self.inputQueue = [address]
        self._computer = IntCodeComputer(program)
        self._computer.inputsProvider = lambda: self.inputQueue.pop(0) if self.inputQueue else -1

    def execute(self, send: Callable[[int, int, int], None]):
        send(self._computer.execute(),
             self._computer.execute(),
             self._computer.execute())


class Day23(TestBase):

    def process(self, line: str):
        result = None
        program = split(line, int)
        nics = [Nic(i, program) for i in range(50)]

        def send(address: int, x: int, y: int):
            if address == 255:
                nonlocal result
                result = y
            else:
                q = nics[address].inputQueue
                q.append(x)
                q.append(y)

        while result is None:
            next(cycle(nics)).execute(send)
        return result

    def test(self):
        self.assertEqual(2019, self.process('104,255,104,0,104,2019,99'))
