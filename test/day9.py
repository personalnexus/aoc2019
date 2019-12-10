from test import processWithIntCodeComputer, LineByLineTestBase as TestBase


class Day9(TestBase):

    def process(self, line: str):
        boostKeyCode = processWithIntCodeComputer(line, [1])[1]
        return boostKeyCode

    def test(self):
        self.checkIntCodeComputerProgram('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99',
                                         '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99', [1])
        self.checkIntCodeComputerOutput0(1125899906842624,
                                         '104,1125899906842624,99', [1])
        self.assertEqual(16,
                         len(str(processWithIntCodeComputer('1102,34915192,34915192,7,4,7,99,0', [1])[1][0])))
