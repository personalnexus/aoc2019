from test import processWithIntCodeComputer, LineByLineTestBase as TestBase


class DayX(TestBase):

    def process(self, line: str):
        result = sum(processWithIntCodeComputer(line, [x, y])[1][0] for x in range(50) for y in range(50))
        return result

    def test(self):
        pass
