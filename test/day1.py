from test import LineByLineTestBase as TestBase


class Day1(TestBase):

    def process(self, line):
        result = int(float(line)/3.0) - 2
        return result

    def test(self):
        self.assertEqual(2, self.process(12))
        self.assertEqual(2, self.process(14))
        self.assertEqual(654, self.process(1969))
        self.assertEqual(33583, self.process(100756))
