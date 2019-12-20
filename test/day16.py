from test import LineByLineTestBase as TestBase
from itertools import repeat


def getPattern(multiplier, patternLength):
    basePattern = [0, 1, 0, -1]
    result = []
    while True:
        for i in range(len(basePattern)):
            result.extend(repeat(basePattern[i], multiplier))
        if len(result) > patternLength:
            break
    return result[1:]


def fft(line: str, phases: int):
    inputLen = len(line)
    patterns = [getPattern(i+1, inputLen) for i in range(inputLen)]

    inputStr = line
    inputInts = list(map(int, inputStr))
    for phase in range(phases):
        outputInts = []
        for pattern in patterns:
            output = sum(ii * p for (ii, p) in zip(inputInts, pattern))
            outputInts.append(abs(output) % 10)
        inputInts = outputInts

    inputStr = ''.join(str(i) for i in inputInts[:8])
    return inputStr


class Day16(TestBase):

    def process(self, line: str):
        result = fft(line, 100)
        return result

    def test(self):
        self.assertEqual('48226158', fft('12345678', 1))
        self.assertEqual('34040438', fft('12345678', 2))
        self.assertEqual('03415518', fft('12345678', 3))
        self.assertEqual('01029498', fft('12345678', 4))
        self.assertEqual('24176176', self.process('80871224585914546619083218645595'))
        self.assertEqual('73745418', self.process('19617804207202209144916044189917'))
        self.assertEqual('52432133', self.process('69317163492948606335995924319873'))
