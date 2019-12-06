from test import split, LineByLineTestBase as TestBase


class Day4(TestBase):

    def process(self, line: str):
        lower, upper = split(line, int)
        lower = max(lower, 111111)
        upper = min(upper, 999999)

        matchCount = 0
        for x in range(lower, upper + 1):
            if self.isMatch(x):
                matchCount += 1

        return matchCount

    @staticmethod
    def isMatch(code: int):
        # six-digits and range checked by process()
        # other criteria:
        twoAdjacentDigitsAreSame = False
        digitsNeverDecrease = True

        codeString = str(code)
        for i in range(1, 6):
            previousDigit = codeString[i-1]
            digit = codeString[i]
            if digit < previousDigit:
                digitsNeverDecrease = False
                break
            elif digit == previousDigit:
                twoAdjacentDigitsAreSame = True

        return twoAdjacentDigitsAreSame and digitsNeverDecrease

    def test(self):
        self.assertFalse(self.isMatch(101234))
        self.assertTrue(self.isMatch(111111))
        self.assertTrue(self.isMatch(111112))
        self.assertTrue(self.isMatch(111123))
        self.assertTrue(self.isMatch(122345))
        self.assertFalse(self.isMatch(123789))
        self.assertTrue(self.isMatch(155679))
        self.assertFalse(self.isMatch(223450))
        self.assertTrue(self.isMatch(999999))
