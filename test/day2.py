from test import split, join, LineByLineTestBase as TestBase, processWithIntCodeComputer
from intcode import IntCodeComputer


class Day2(TestBase):

    def process(self, line: str):
        codes = split(line, int)
        for i in range(0, len(codes), 4):
            operationCode = codes[i]
            if operationCode == 1:
                operation = lambda x, y: x+y
            elif operationCode == 2:
                operation = lambda x, y: x * y
            elif operationCode == 99:
                break
            else:
                raise Exception('Invalid operationCode {0} in position {1}'.format(operationCode, i))

            # check operationCode before reading on, because after 99 there are no more codes
            paramPos1 = codes[i+1]
            paramPos2 = codes[i+2]
            resultPos = codes[i+3]
            result = operation(codes[paramPos1], codes[paramPos2])
            codes[resultPos] = result
        return join(codes)

    def test(self):
        self.coreTest(self.process)
        self.coreTest(lambda line: processWithIntCodeComputer(line, 0)[0])  # general solution from day 5 works, too

    def coreTest(self, process):
        self.assertEqual('2,0,0,0,99', process('1,0,0,0,99'))
        self.assertEqual('2,3,0,6,99', process('2,3,0,3,99'))
        self.assertEqual('2,4,4,5,99,9801', process('2,4,4,5,99,0'))
        self.assertEqual('30,1,1,4,2,5,6,0,99', process('1,1,1,4,99,5,6,0,99'))
