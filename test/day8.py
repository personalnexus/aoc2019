from test import LineByLineTestBase as TestBase


class Day8(TestBase):

    def process(self, line: str):
        return self.processCore(line, 25*6)

    def processCore(self, line: str, pixelCount):
        if len(line) == 0:
            raise ValueError("length of line must be greater than 0")
        if len(line) % pixelCount != 0:
            raise ValueError("length of line must be multiple of pixel count")

        # Reduce memory footprint by iterating over layers as individual substrings of the input
        # one at a time without building up lists of layers for sorting them

        minimumLayer = line[0:pixelCount]
        minimumCountOf0 = minimumLayer.count('0')

        for i in range(pixelCount, len(line), pixelCount):
            layer = line[i:i+pixelCount]
            layerCountOf0 = layer.count('0')
            if layerCountOf0 < minimumCountOf0:
                minimumLayer = layer

        # Q: would it be faster to count 0,1,2 during the one iteration over all layers instead
        # of calling count() on the minimumLayer three times?

        return minimumLayer.count('1') * minimumLayer.count('2')

    def test(self):
        self.assertRaises(ValueError, self.processCore, '', 17)
        self.assertRaises(ValueError, self.processCore, '1234567', 3)
        self.assertEqual(1, self.processCore('123456'+'789012', 3*2))
        self.assertEqual(2, self.processCore('122100'+'782012', 3*2))
        self.assertEqual(4, self.processCore('122100', 3*2))
