from test import LineByLineTestBase


class Day1(LineByLineTestBase):

    def process(self, line):
        result = int(float(line)/3.0) - 2
        return result

    def testOne(self):
        self.check(12, 2)
        self.check(14, 2)
        self.check(1969, 654)
        self.check(100756, 33583)
