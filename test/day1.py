from test import LineByLineTestBase as TestBase


class Day1(TestBase):

    def process(self, line):
        result = int(float(line)/3.0) - 2
        return result

    def test(self):
        self.check(12, 2)
        self.check(14, 2)
        self.check(1969, 654)
        self.check(100756, 33583)
