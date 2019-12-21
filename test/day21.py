from test import LineByLineTestBase as TestBase, processWithIntCodeComputer
from intcode import springScriptToIntCodeInputs


class Day21(TestBase):

    def process(self, line: str):
        springScript = []  # TODO
        intCodeInputs = springScriptToIntCodeInputs(springScript)
        return processWithIntCodeComputer(line, intCodeInputs)[1][0]

    def test(self):
        self.assertEqual([78, 79, 84, 32, 68, 32, 74, 10,
                          87, 65, 76, 75, 10], springScriptToIntCodeInputs(['NOT D J']))
        self.assertEqual(1, self.process('104,1,99'))
