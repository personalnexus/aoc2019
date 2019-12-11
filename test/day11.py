from intcode import IntCodeComputer
from test import split, LineByLineTestBase as TestBase
from collections import defaultdict
from typing import List


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
        # after a full move, we're facing up again
        if not Direction.up <= self.direction <= Direction.left:
            self.direction = Direction.up
        return Direction._movementsByDirection[self.direction](x, y)


class HullPaintingRobot(object):

    def __init__(self, program: List[int]):
        self.computer = IntCodeComputer(program)

    def paint(self):
        (x, y) = (0, 0)
        direction = Direction()
        panelColorByXy = defaultdict(int)  # black = 0 (conveniently default(int) == default panel color), white = 1
        while not self.computer.halted:
            oldPanelColor = panelColorByXy[(x, y)]
            newPanelColor = self.computer.execute([oldPanelColor])
            panelColorByXy[(x, y)] = newPanelColor
            turn = self.computer.execute([])
            x, y = direction.move(x, y, turn)
        return panelColorByXy


class Day11(TestBase):

    def process(self, line: str):
        robot = HullPaintingRobot(split(line, int))
        paintedPanels = robot.paint()
        return len(paintedPanels)

    def test(self):
        pass
