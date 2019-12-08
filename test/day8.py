from test import LineByLineTestBase as TestBase


class Day8(TestBase):

    def process(self, line: str, pixelsPerLayer=25*6):
        # Some parameter validation because today's problem is so short
        lineLength = len(line)
        if lineLength == 0:
            raise ValueError("length of line must be greater than 0")
        if lineLength % pixelsPerLayer != 0:
            raise ValueError("length of line {0} must be multiple of the number of pixels per layer {1}"
                             .format(lineLength, pixelsPerLayer))

        # Bonus challenge: reduce memory footprint by iterating over the line only once and saving relevant indexes
        # instead of building up lists of layers for sorting
        minimumCountOf0 = pixelsPerLayer + 1
        minimumStartIndex = 0
        minimumEndIndex = endIndex = lineLength

        # iterate in reverse because I read somewhere that comparing a number against zero is slightly faster than
        # comparing it against a non-zero value
        while endIndex > 0:
            startIndex = endIndex - pixelsPerLayer
            layerCountOf0 = line.count('0', startIndex, endIndex)
            if layerCountOf0 < minimumCountOf0:
                minimumCountOf0 = layerCountOf0
                minimumStartIndex = startIndex
                minimumEndIndex = endIndex
            endIndex = startIndex

        return line.count('1', minimumStartIndex, minimumEndIndex) * line.count('2', minimumStartIndex, minimumEndIndex)

    def test(self):
        self.assertRaises(ValueError, self.process, '', 17)
        self.assertRaises(ValueError, self.process, '1234567', 3)
        self.assertEqual(1, self.process('123456' + '789012', 3 * 2))
        self.assertEqual(2, self.process('122100' + '782012', 3 * 2))
        self.assertEqual(4, self.process('122100', 3 * 2))
        self.assertEqual(0, self.process('111111', 3 * 2))
        self.assertEqual(0, self.process('222222', 3 * 2))
        self.assertEqual(0, self.process('333333', 3 * 2))
