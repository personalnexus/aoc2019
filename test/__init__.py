import unittest
from abc import ABC
from typing import List, Iterable


def split(items, cast):
    result = [cast(x) for x in items.split(',')]
    return result


def join(items):
    result = ','.join(str(x) for x in items)
    return result


def processWithIntCodeComputer(line: str, inputs: List[int]):
    from intcode import IntCodeComputer
    originalProgram = split(line, int)
    initialProgramLength = len(originalProgram)
    computer = IntCodeComputer(originalProgram)
    outputs = computer.executeAll(inputs)
    program = (value for (key, value) in computer.program.items() if key < initialProgramLength)
    return join(program), outputs


class TestBase(unittest.TestCase):
    """Base class for each day's task which is to be implemented by overriding process() and test()"""

    @classmethod
    def setUpClass(cls):
        if cls is TestBase:
            raise unittest.SkipTest("Skip TestBase tests, it's a base class")
        super(TestBase, cls).setUpClass()

    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)
        self._day = self.__class__.__name__[3:]

    def processAll(self, inputs: Iterable[str]) -> Iterable[str]:
        raise NotImplementedError("must override processAll()")

    def test(self):
        raise NotImplementedError("must override test()")

    def testGenerateOutput(self):
        with open(r'..\data\day{0}in.txt'.format(self._day), 'r') as file:
            inputs = [s.strip() for s in file.readlines()]
        outputs = self.processAll(inputs)
        with open(r'..\data\day{0}out.txt'.format(self._day), 'w') as file:
            file.writelines(outputs)

    def checkIntCodeComputerOutput0(self, expectedOutput: int, line: str, inputs: List[int]):
        self.assertEqual(expectedOutput, processWithIntCodeComputer(line, inputs)[1][0])

    def checkIntCodeComputerProgram(self, expectedProgram: str, line: str, inputs: List[int]):
        self.assertEqual(expectedProgram, processWithIntCodeComputer(line, inputs)[0])


class LineByLineTestBase(TestBase, ABC):
    """Base class for tasks processing one line at a time with one output per input line"""

    def processAll(self, inputs):
        outputs = (str(self.process(line)) + '\n' for line in inputs)
        return outputs

    def process(self, line: str):
        raise NotImplementedError("must override process()")


class AllLinesTestBase(TestBase, ABC):
    """Base class for tasks processing all lines at once returning a single output"""

    def processAll(self, inputs):
        output = list(str(self.process(list(inputs))))
        return output

    def process(self, lines: List[str]):
        raise NotImplementedError("must override process()")
