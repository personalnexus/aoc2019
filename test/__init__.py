import unittest


def split(items, cast):
    result = [cast(x) for x in items.split(',')]
    return result


def join(items):
    result = ','.join(str(x) for x in items)
    return result


class TestBase(unittest.TestCase):
    """base class for each day's task which is to be implemented by overriding execute() and testOne()"""

    @classmethod
    def setUpClass(cls):
        if cls is TestBase:
            raise unittest.SkipTest("Skip TestBase tests, it's a base class")
        super(TestBase, cls).setUpClass()

    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)
        day = self.__class__.__name__[3:]
        self._day = day

    def check(self, line, expectedOutput):
        actualOutput = self.execute(line)
        self.assertEqual(expectedOutput, actualOutput)

    def execute(self, line):
        self.fail("must override execute()")

    def testOne(self):
        self.fail("must override testOne()")

    def testAll(self):
        with open(r'..\data\day{0}in.txt'.format(self._day), 'r') as file:
            inputs = file.readlines()
        outputs = (str(self.execute(line)) + '\n' for line in inputs)
        with open(r'..\data\day{0}out.txt'.format(self._day), 'w') as file:
            file.writelines(outputs)
