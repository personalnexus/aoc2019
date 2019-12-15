from intcode import IntCodeComputer
from test import split, LineByLineTestBase as TestBase
from collections import defaultdict
from typing import List


class Color:
    """Just a namespace for colors that results in a syntax similar to C# enums"""
    black = 0
    white = 1


class Direction:
    """
    Adapted from day 3, the Direction class provides a namespace for named direction constants and related functionality
    """

    up = 0
    right = 1
    down = 2
    left = 3

    _movementsByDirection = {up: lambda x, y: (x, y + 1),
                             right: lambda x, y: (x + 1, y),
                             down: lambda x, y: (x, y - 1),
                             left: lambda x, y: (x - 1, y)}

    def __init__(self):
        self.direction = Direction.up

    def move(self, x: int, y: int, turn: int):
        self.direction += 1 if turn == 1 else -1
        # after a full turn, we're facing up again.
        self.direction = (self.direction + 4) % 4
        x, y = Direction._movementsByDirection[self.direction](x, y)
        return x, y


class HullPaintingRobot(object):

    def __init__(self, program: List[int], defaultPanelColor=Color.black):
        self.computer = IntCodeComputer(program)
        self.direction = Direction()
        self.panelColorByXy = defaultdict(lambda: defaultPanelColor)
        (self.x, self.y) = (0, 0)
        # don't access dict for the initial panel color, as it would create an entry for a panel that was not colored
        oldPanelColor = defaultPanelColor
        while not self.computer.halted:
            newPanelColor = self.computer.execute([oldPanelColor])
            oldPanelColor = self.panelColorByXy[(self.x, self.y)]
            self.panelColorByXy[(self.x, self.y)] = newPanelColor
            turn = self.computer.execute([])
            self.x, self.y = self.direction.move(self.x, self.y, turn)


class Day11(TestBase):

    def process(self, line: str):
        paintedPanels = HullPaintingRobot(split(line, int)).panelColorByXy
        return len(paintedPanels)

    def test(self):
        self.assertEqual(0, len(HullPaintingRobot([99]).panelColorByXy))
        # Paint white, turn left
        paintBot1 = HullPaintingRobot([104, 1, 104, 0, 99])
        self.assertEqual(1, len(paintBot1.panelColorByXy))
        self.assertEqual(((0, 0), Color.white), paintBot1.panelColorByXy.popitem())
        self.assertEqual(Direction.left, paintBot1.direction.direction)
        self.assertEqual(-1, paintBot1.x)
        self.assertEqual(0, paintBot1.y)
