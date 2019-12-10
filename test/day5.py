from test import processWithIntCodeComputer, LineByLineTestBase as TestBase


class Day5(TestBase):

    def process(self, line: str):
        diagnosticCode = processWithIntCodeComputer(line, [1])[1]
        return diagnosticCode

    def test(self):
        self.checkIntCodeComputerProgram('1002,4,3,4,99', '1002,4,3,4,33', [1])
