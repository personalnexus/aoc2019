from test import split, join, LineByLineTestBase as TestBase


class Day2(TestBase):

    def process(self, line):
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

    def testOne(self):
        self.check('1,0,0,0,99', '2,0,0,0,99')
        self.check('2,3,0,3,99', '2,3,0,6,99')
        self.check('2,4,4,5,99,0', '2,4,4,5,99,9801')
        self.check('1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99')
